#!/usr/bin/env bash
# PreToolUse(Bash) hook: protect the active orchestration's parent issue
# from accidental closure or unauthorized body rewrites.
#
# Decision logic:
#   1. No active state file                                    → allow
#   2. Command is `gh issue close <PARENT>` and any child of
#      the parent is still unmerged                            → deny
#   3. Command is `gh issue edit <PARENT> --body*` and the new
#      body lacks the cstack-collab marker                     → deny
#   4. Otherwise                                                → allow
#
# Escape hatch: CSTACK_COLLAB_OVERRIDE=1 logs a warning and allows.
#
# Why: the orchestrator (and its workers) might cheerfully run
# `gh issue close <parent>` thinking the work is done, or rewrite the
# parent body with a "cleaned-up" version that drops the spec. The
# update-parent-checklist.py script embeds <!-- cstack-collab:checklist -->
# in legitimate body updates so this hook can recognize them.

set -euo pipefail

input="$(cat)"
command="$(printf '%s' "$input" | jq -r '.tool_input.command // empty')"
[ -n "$command" ] || exit 0

# Cheap early filter — only react to gh issue close/edit.
case "$command" in
    *"gh issue close"*|*"gh issue edit"*) ;;
    *) exit 0 ;;
esac

state_file="$("${CLAUDE_PLUGIN_ROOT}/scripts/state.py" find 2>/dev/null || true)"
[ -n "$state_file" ] || exit 0

if [ "${CSTACK_COLLAB_OVERRIDE:-0}" = "1" ]; then
    echo "cstack-collab: CSTACK_COLLAB_OVERRIDE=1 — allowing parent-mutation despite active orchestration." >&2
    exit 0
fi

parent="$(${CLAUDE_PLUGIN_ROOT}/scripts/state.py get parent 2>/dev/null || echo '')"
[ -n "$parent" ] || exit 0

# Extract the issue number argument from the command. Looks for the first
# token that's a number or #N appearing after `issue close|edit`.
target=""
for kw in "gh issue close" "gh issue edit"; do
    case "$command" in
        *"$kw"*)
            tail="${command#*$kw}"
            # shellcheck disable=SC2086
            set -- $tail
            for tok in "$@"; do
                case "$tok" in
                    --*) continue ;;
                    \#[0-9]*|[0-9]*) target="${tok#\#}"; break ;;
                esac
            done
            break
            ;;
    esac
done

[ -n "$target" ] || exit 0

# Only react when the target IS the active parent.
if [ "$target" != "$parent" ]; then
    exit 0
fi

case "$command" in
    *"gh issue close"*)
        pending="$("${CLAUDE_PLUGIN_ROOT}/scripts/state.py" pending-children 2>/dev/null || true)"
        if [ -n "$pending" ]; then
            echo "cstack-collab: refusing \`gh issue close #${parent}\` — children still pending:" >&2
            echo "$pending" | sed 's/^/  - #/' >&2
            echo "Wait for those to merge, or set CSTACK_COLLAB_OVERRIDE=1 to bypass." >&2
            exit 2
        fi
        ;;
    *"gh issue edit"*)
        # Only intercept body rewrites. --add-label / --remove-assignee etc are fine.
        case "$command" in
            *"--body"*) ;;
            *) exit 0 ;;
        esac
        # Read the body argument. Two flavors:
        #   --body "..."       (string)
        #   --body-file <path> (file)
        body_content=""
        if printf '%s' "$command" | grep -q -- '--body-file'; then
            # Capture the path arg.
            path="$(printf '%s' "$command" | sed -n 's/.*--body-file[ =]\(\S\+\).*/\1/p')"
            # `-` means stdin; we cannot inspect stdin here, so play it safe and allow
            # only if the orchestrator's own script is the caller. Heuristic: the
            # update-parent-checklist.py invocation pipes from itself; in practice
            # it does NOT use --body-file (it uses gh's stdin), so a --body-file -
            # invocation here is almost always the model trying something custom.
            if [ "$path" = "-" ]; then
                echo "cstack-collab: refusing \`gh issue edit #${parent} --body-file -\`. Use scripts/update-parent-checklist.py for legitimate updates, or set CSTACK_COLLAB_OVERRIDE=1." >&2
                exit 2
            fi
            if [ -f "$path" ]; then
                body_content="$(cat "$path")"
            fi
        else
            # --body "..." — extract.
            body_content="$(printf '%s' "$command" | sed -n 's/.*--body[ =]"\([^"]*\)".*/\1/p')"
        fi

        if ! printf '%s' "$body_content" | grep -q '<!-- cstack-collab:checklist -->'; then
            echo "cstack-collab: refusing \`gh issue edit #${parent} --body\` — body is missing the cstack-collab:checklist marker." >&2
            echo "Use scripts/update-parent-checklist.py for legitimate updates, or set CSTACK_COLLAB_OVERRIDE=1." >&2
            exit 2
        fi
        ;;
esac

exit 0

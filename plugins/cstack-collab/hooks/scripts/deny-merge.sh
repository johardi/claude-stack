#!/usr/bin/env bash
# PreToolUse(Bash) hook: refuse to merge a PR that belongs to the active
# orchestration. No-op outside an active orchestration so day-to-day
# `gh pr merge` continues to work normally.
#
# Decision logic:
#   1. If no .cstack-collab/state.json in or above $PWD       → exit 0 (allow)
#   2. If the command isn't a `gh pr merge` invocation         → exit 0 (allow)
#   3. If the command targets a PR that is a child of the
#      active orchestration's parent issue                     → exit 2 (deny)
#   4. Otherwise (merging some unrelated PR, --auto on a child) → exit 2 if --auto is on a child, else exit 0
#
# Escape hatch: setting CSTACK_COLLAB_OVERRIDE=1 in the env logs a
# warning and allows the call.

set -euo pipefail

input="$(cat)"
command="$(printf '%s' "$input" | jq -r '.tool_input.command // empty')"

# Not a Bash call with a command, or no command — allow.
[ -n "$command" ] || exit 0

# Not a merge command — allow.
case "$command" in
    *"gh pr merge"*) ;;
    *) exit 0 ;;
esac

# No active orchestration anywhere — allow.
state_file="$("${CLAUDE_PLUGIN_ROOT}/scripts/state.py" find 2>/dev/null || true)"
[ -n "$state_file" ] || exit 0

# Escape hatch.
if [ "${CSTACK_COLLAB_OVERRIDE:-0}" = "1" ]; then
    echo "cstack-collab: CSTACK_COLLAB_OVERRIDE=1 — allowing \`gh pr merge\` despite active orchestration. State file: $state_file" >&2
    exit 0
fi

# Try to identify the PR target. `gh pr merge` accepts a number, URL, or
# branch name. We look for: the first token after `merge` that is a
# number, a URL, or `#N`.
target=""
# Strip everything up to and including "gh pr merge"
tail="${command#*gh pr merge}"
# shellcheck disable=SC2086
set -- $tail
for tok in "$@"; do
    case "$tok" in
        --*) continue ;;
        http*|\#[0-9]*|[0-9]*) target="$tok"; break ;;
    esac
done

# If we cannot determine the target, be conservative: deny while
# orchestration is active. The user can still set the override.
if [ -z "$target" ]; then
    echo "cstack-collab: refusing \`gh pr merge\` without an explicit PR target while orchestration is active (parent #$(${CLAUDE_PLUGIN_ROOT}/scripts/state.py get parent 2>/dev/null || echo '?'))." >&2
    echo "Pass an explicit PR number/URL, or set CSTACK_COLLAB_OVERRIDE=1 to bypass." >&2
    exit 2
fi

if "${CLAUDE_PLUGIN_ROOT}/scripts/state.py" is-child "$target" >/dev/null 2>&1; then
    parent="$(${CLAUDE_PLUGIN_ROOT}/scripts/state.py get parent 2>/dev/null || echo '?')"
    echo "cstack-collab: refusing to merge PR ${target} — it is a child of active orchestration on parent #${parent}." >&2
    echo "The orchestrator never auto-merges. Merge it yourself in the UI, or set CSTACK_COLLAB_OVERRIDE=1 to bypass." >&2
    exit 2
fi

# Unrelated PR — allow even during orchestration.
exit 0

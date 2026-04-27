#!/usr/bin/env bash
# PreToolUse(Bash): refuse `git push --force` (or -f / --force-with-lease)
# to the default branch.
#
# Detects the default branch via `gh repo view` (preferred) or origin/HEAD
# (fallback). Use CSTACK_GUARDRAILS_OVERRIDE=1 to bypass.

set -euo pipefail

input="$(cat)"
command="$(printf '%s' "$input" | jq -r '.tool_input.command // empty')"
[ -n "$command" ] || exit 0

case "$command" in
    *"git push"*) ;;
    *) exit 0 ;;
esac

# Look for force flags. Word-bounded to avoid false matches.
forces=0
for flag in '--force' '--force-with-lease' '-f'; do
    if printf '%s' "$command" | grep -qE "(^|[[:space:]])${flag}([[:space:]=]|$)"; then
        forces=1
        break
    fi
done
[ "$forces" = "1" ] || exit 0

# Detect default branch. Best-effort.
default_branch="$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name 2>/dev/null || true)"
if [ -z "$default_branch" ]; then
    default_branch="$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@' || true)"
fi
[ -n "$default_branch" ] || exit 0  # can't tell — fail open

# Check whether the command targets the default branch. We accept either
# an explicit `<remote> <branch>` pair, or no branch arg at all (in which
# case git pushes the current branch — also check that).
target_default=0
if printf '%s' "$command" | grep -qE "(^|[[:space:]])${default_branch}([[:space:]]|$)"; then
    target_default=1
elif ! printf '%s' "$command" | grep -qE 'git push[[:space:]]+\S+[[:space:]]+\S+'; then
    # No explicit ref — pushing current branch. Compare current to default.
    cur="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
    if [ "$cur" = "$default_branch" ]; then
        target_default=1
    fi
fi
[ "$target_default" = "1" ] || exit 0

if [ "${CSTACK_GUARDRAILS_OVERRIDE:-0}" = "1" ]; then
    echo "cstack-guardrails: CSTACK_GUARDRAILS_OVERRIDE=1 — allowing force-push to ${default_branch}." >&2
    exit 0
fi

echo "cstack-guardrails: refusing \`git push --force\` to default branch (${default_branch})." >&2
echo "Force-push can destroy upstream history. Push to a feature branch and open a PR instead." >&2
echo "Set CSTACK_GUARDRAILS_OVERRIDE=1 to bypass this once." >&2
exit 2

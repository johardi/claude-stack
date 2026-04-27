#!/usr/bin/env bash
# PreToolUse(Bash): refuse `git commit` while on the default branch.
#
# Encourages branch-per-feature workflows. Use CSTACK_GUARDRAILS_OVERRIDE=1
# to bypass when intentionally committing to default (e.g., docs-only repos,
# personal experiments).

set -euo pipefail

input="$(cat)"
command="$(printf '%s' "$input" | jq -r '.tool_input.command // empty')"
[ -n "$command" ] || exit 0

# Match `git commit` but not `git commit-tree` or other lookalikes.
if ! printf '%s' "$command" | grep -qE '(^|[[:space:]])git[[:space:]]+commit([[:space:]]|$)'; then
    exit 0
fi

# Are we in a git repo at all?
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

cur="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
[ -n "$cur" ] || exit 0

default_branch="$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name 2>/dev/null || true)"
if [ -z "$default_branch" ]; then
    default_branch="$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@' || true)"
fi
[ -n "$default_branch" ] || exit 0  # can't tell — fail open

[ "$cur" = "$default_branch" ] || exit 0

if [ "${CSTACK_GUARDRAILS_OVERRIDE:-0}" = "1" ]; then
    echo "cstack-guardrails: CSTACK_GUARDRAILS_OVERRIDE=1 — allowing commit on ${default_branch}." >&2
    exit 0
fi

echo "cstack-guardrails: refusing \`git commit\` on default branch (${default_branch})." >&2
echo "Create a feature branch first: \`git checkout -b feature/<name>\`." >&2
echo "Set CSTACK_GUARDRAILS_OVERRIDE=1 to bypass this once." >&2
exit 2

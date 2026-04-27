#!/usr/bin/env bash
# Preflight checks for orchestrate-tickets.
#
# Runs deterministically (no LLM interpretation). Exit 0 iff every required
# tool, auth state, and repo invariant is satisfied. On success, prints the
# repo's default branch on stdout (so the caller can capture it without an
# extra round-trip).
#
# On failure, prints a single-line reason on stderr and exits non-zero with
# a stable code so the skill / hooks can react:
#
#   1   gh CLI missing
#   2   gh not authenticated
#   3   not inside a git repository
#   4   working tree dirty
#   5   could not detect default branch
#   6   git missing

set -euo pipefail

err() { echo "check-prereqs: $1" >&2; }

command -v git >/dev/null 2>&1 || { err "git not found in PATH"; exit 6; }
command -v gh  >/dev/null 2>&1 || { err "gh CLI not found in PATH"; exit 1; }

if ! gh auth status >/dev/null 2>&1; then
    err "gh CLI is not authenticated (run: gh auth login)"
    exit 2
fi

if ! git rev-parse --git-dir >/dev/null 2>&1; then
    err "not inside a git repository"
    exit 3
fi

if [ -n "$(git status --porcelain)" ]; then
    err "working tree is dirty — commit or stash before orchestrating"
    exit 4
fi

# Default branch detection. Prefer GitHub's reported default, fall back to
# the local symbolic-ref of origin/HEAD if gh returns nothing.
default_branch="$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name 2>/dev/null || true)"
if [ -z "$default_branch" ]; then
    default_branch="$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@' || true)"
fi
if [ -z "$default_branch" ]; then
    err "could not detect default branch (set origin/HEAD or run: gh repo view)"
    exit 5
fi

echo "$default_branch"

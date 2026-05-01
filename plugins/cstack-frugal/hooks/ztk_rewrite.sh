#!/bin/bash
# ztk_rewrite.sh — Selective ztk rewrite hook for Claude Code PreToolUse
#
# Passes bash command output through `ztk rewrite` only for commands where
# trimming is safe (noise-heavy output). Commands that produce output where
# every line matters (test failures, diffs, compiler errors, lint results)
# are exempted so Claude gets full context for coding tasks.

INPUT=$(cat)

CMD=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('tool_input', {}).get('command', ''))
except Exception:
    print('')
" 2>/dev/null)

# Commands exempt from ztk rewriting — full output needed for coding tasks
EXEMPT_PATTERN='^\s*('

# Test runners
EXEMPT_PATTERN+='pytest|python3?\s+-m\s+pytest|'
EXEMPT_PATTERN+='cargo\s+(test|nextest)|'
EXEMPT_PATTERN+='go\s+test|'
EXEMPT_PATTERN+='npm\s+(test|run\s+test)|pnpm\s+test|yarn\s+test|'
EXEMPT_PATTERN+='jest|vitest|npx\s+(jest|vitest)|'
EXEMPT_PATTERN+='playwright|'
EXEMPT_PATTERN+='rspec|'

# Build tools
EXEMPT_PATTERN+='cargo\s+(build|check)|'
EXEMPT_PATTERN+='go\s+build|'
EXEMPT_PATTERN+='tsc(\s|$)|'
EXEMPT_PATTERN+='zig\s+build|'

# Linters / type checkers
EXEMPT_PATTERN+='eslint|'
EXEMPT_PATTERN+='ruff\s+(check|format)|uvx\s+ruff|'
EXEMPT_PATTERN+='mypy|'
EXEMPT_PATTERN+='clippy|cargo\s+clippy|'
EXEMPT_PATTERN+='golangci|'
EXEMPT_PATTERN+='rubocop|'

# Git commands where content matters
EXEMPT_PATTERN+='git\s+diff|'
EXEMPT_PATTERN+='git\s+show|'
EXEMPT_PATTERN+='git\s+log|'

# File reading / search
EXEMPT_PATTERN+='cat\s|'
EXEMPT_PATTERN+='head\s|tail\s|'
EXEMPT_PATTERN+='grep\s|rg\s|'

# API / data output
EXEMPT_PATTERN+='curl\s|'
EXEMPT_PATTERN+='jq\s|'
EXEMPT_PATTERN+='psql\s|'

# CI / infra logs
EXEMPT_PATTERN+='gh\s+checks|'
EXEMPT_PATTERN+='kubectl\s+logs|'
EXEMPT_PATTERN+='docker\s+logs'

EXEMPT_PATTERN+=')'

if echo "$CMD" | grep -qE "$EXEMPT_PATTERN"; then
    # Exempt: pass through unchanged so Claude gets full output
    echo "$INPUT"
else
    # Safe to compress: run through ztk rewrite
    echo "$INPUT" | ztk rewrite
fi

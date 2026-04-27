#!/usr/bin/env bash
# PreToolUse(Bash): refuse to skip git hooks or signing.
#
# Blocks --no-verify, --no-gpg-sign, and -c commit.gpgsign=false on any
# git or gh command. Use CSTACK_GUARDRAILS_OVERRIDE=1 to bypass.

set -euo pipefail

input="$(cat)"
command="$(printf '%s' "$input" | jq -r '.tool_input.command // empty')"
[ -n "$command" ] || exit 0

# Word-boundary checks so we don't false-match on "--no-verify-ssl" etc.
matched=""
for flag in '--no-verify' '--no-gpg-sign' 'commit.gpgsign=false'; do
    if printf '%s' "$command" | grep -qE "(^|[[:space:]=])${flag}([[:space:]=]|$)"; then
        matched="$flag"
        break
    fi
done
[ -n "$matched" ] || exit 0

if [ "${CSTACK_GUARDRAILS_OVERRIDE:-0}" = "1" ]; then
    echo "cstack-guardrails: CSTACK_GUARDRAILS_OVERRIDE=1 — allowing ${matched}." >&2
    exit 0
fi

echo "cstack-guardrails: refusing to skip hooks/signing (${matched})." >&2
echo "If a pre-commit hook is failing, fix the underlying issue rather than skipping it." >&2
echo "Set CSTACK_GUARDRAILS_OVERRIDE=1 to bypass this once." >&2
exit 2

#!/usr/bin/env bash
# SessionStart hook: when a session starts in a repo with an active
# orchestration, surface a one-line summary so the user (and the model)
# don't lose their place across sessions.
#
# No-op when no state.json is found.

set -euo pipefail

state_file="$("${CLAUDE_PLUGIN_ROOT}/scripts/state.py" find 2>/dev/null || true)"
[ -n "$state_file" ] || exit 0

parent="$(${CLAUDE_PLUGIN_ROOT}/scripts/state.py get parent 2>/dev/null || echo '?')"
wave_index="$(${CLAUDE_PLUGIN_ROOT}/scripts/state.py get wave_index 2>/dev/null || echo '?')"
waves_json="$(${CLAUDE_PLUGIN_ROOT}/scripts/state.py get waves 2>/dev/null || echo '[]')"
total_waves="$(printf '%s' "$waves_json" | jq 'length')"
pending="$(${CLAUDE_PLUGIN_ROOT}/scripts/state.py pending-children 2>/dev/null | tr '\n' ' ' | sed 's/ *$//')"

# Wave numbering: 0-indexed in the file, 1-indexed for human display.
human_wave=$(( wave_index + 1 ))

echo "cstack-collab: orchestration in progress for parent #${parent} (wave ${human_wave} of ${total_waves})." >&2
if [ -n "$pending" ]; then
    echo "  pending children: $(echo "$pending" | sed 's/ /, #/g; s/^/#/')" >&2
else
    echo "  all children merged — run \`scripts/state.py complete\` to close out." >&2
fi
echo "  state file: $state_file" >&2
exit 0

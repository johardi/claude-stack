#!/bin/bash
# setup-statusline.sh — UserPromptSubmit nudge for the cstack-core statusline.
# Fires on the first user message of each session. Injects additionalContext
# so Claude proactively asks the user if they want to install the statusline.
# Stops nudging after 3 sessions total.

SETTINGS_FILE="$HOME/.claude/settings.json"
NUDGE_FILE="$HOME/.claude/.cstack-statusline-nudge"
INSTALL_SCRIPT="$CLAUDE_PLUGIN_ROOT/scripts/statusline/install-statusline.sh"

# Read hook event JSON from stdin.
INPUT=$(cat)

# Already configured — nothing to do.
if command -v jq >/dev/null 2>&1; then
  EXISTING=$(jq -r '.statusLine // empty' "$SETTINGS_FILE" 2>/dev/null)
  [ -n "$EXISTING" ] && exit 0
fi

# Per-session dedup: only nudge once per session using session_id.
SESSION_ID=""
if command -v jq >/dev/null 2>&1; then
  SESSION_ID=$(printf '%s' "$INPUT" | jq -r '.session_id // empty' 2>/dev/null)
fi
if [ -n "$SESSION_ID" ]; then
  SESSION_FLAG="/tmp/.cstack-sl-$SESSION_ID"
  [ -f "$SESSION_FLAG" ] && exit 0
  touch "$SESSION_FLAG"
fi

# Read nudge count (default 0). Cap at 3 sessions total.
COUNT=0
[ -f "$NUDGE_FILE" ] && COUNT=$(cat "$NUDGE_FILE" 2>/dev/null)
COUNT=${COUNT:-0}
[ "$COUNT" -ge 3 ] 2>/dev/null && exit 0

# Increment and persist.
echo $((COUNT + 1)) > "$NUDGE_FILE"

# Output additionalContext JSON — injected into Claude's context by the hook runner.
NUDGE_NUM=$((COUNT + 1))
printf '{"additionalContext":"cstack-core: The statusline feature (shows pwd, git branch, model, tokens, and context %%) is available but not yet configured. This is nudge %d/3. Please let the user know and ask if they would like to install it. If yes, run: bash \\"%s\\""}' \
  "$NUDGE_NUM" "$INSTALL_SCRIPT"

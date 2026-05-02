#!/bin/bash
# setup-statusline.sh — SessionStart nudge for the cstack-core statusline.
# Fires once per new session (startup matcher). Checks if the statusline is
# configured; if not, injects an additionalContext message so Claude asks the
# user. Stops nudging after 3 sessions.

SETTINGS_FILE="$HOME/.claude/settings.json"
NUDGE_FILE="$HOME/.claude/.cstack-statusline-nudge"
INSTALL_SCRIPT="$CLAUDE_PLUGIN_ROOT/scripts/statusline/install-statusline.sh"

# Already configured — nothing to do.
if command -v jq >/dev/null 2>&1; then
  EXISTING=$(jq -r '.statusLine // empty' "$SETTINGS_FILE" 2>/dev/null)
  [ -n "$EXISTING" ] && exit 0
fi

# Read nudge count (default 0).
COUNT=0
[ -f "$NUDGE_FILE" ] && COUNT=$(cat "$NUDGE_FILE" 2>/dev/null)
COUNT=${COUNT:-0}

# Cap reached — stop nudging silently.
[ "$COUNT" -ge 3 ] 2>/dev/null && exit 0

# Increment and persist.
echo $((COUNT + 1)) > "$NUDGE_FILE"

# Output additionalContext JSON for the hook runner to inject into the session.
NUDGE_NUM=$((COUNT + 1))
printf '{"additionalContext":"cstack-core: The statusline feature (shows git branch, model, tokens, and context %%) is available but not configured. This is nudge %d/3. Please let the user know and ask if they would like to install it. If yes, run: bash \\"%s\\""}' \
  "$NUDGE_NUM" "$INSTALL_SCRIPT"

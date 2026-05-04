#!/bin/bash
# setup-statusline.sh — UserPromptSubmit nudge for the cstack-core statusline.
# Fires on the first user message of each session. Behaviour depends on the
# current statusLine configuration in ~/.claude/settings.json:
#
#   • Not configured          → nudge Claude to ask the user to install
#   • cstack-core stable wrapper already set → exit silently (auto-updates via glob)
#   • cstack-core old versioned path set     → auto-update to stable wrapper, no prompt
#   • Foreign statusline set  → nudge Claude to ask permission to replace
#
# Nudge count is incremented for cases 1 and 4; capped at 3 sessions total.

SETTINGS_FILE="$HOME/.claude/settings.json"
NUDGE_FILE="$HOME/.claude/.cstack-statusline-nudge"
INSTALL_SCRIPT="$CLAUDE_PLUGIN_ROOT/scripts/statusline/install-statusline.sh"

# Read hook event JSON from stdin.
INPUT=$(cat)

# Per-session dedup: only nudge once per session using session_id.
SESSION_ID=""
if command -v jq >/dev/null 2>&1; then
  SESSION_ID=$(printf '%s' "$INPUT" | jq -r '.session_id // empty' 2>/dev/null)
fi
SESSION_FLAG=""
if [ -n "$SESSION_ID" ]; then
  SESSION_FLAG="/tmp/.cstack-sl-$SESSION_ID"
fi

# Detect existing statusLine command.
EXISTING_CMD=""
if command -v jq >/dev/null 2>&1 && [ -f "$SETTINGS_FILE" ]; then
  EXISTING_CMD=$(jq -r '.statusLine.command // empty' "$SETTINGS_FILE" 2>/dev/null)
fi

# --- Case 2: cstack-core stable wrapper already configured — nothing to do.
if echo "$EXISTING_CMD" | grep -q "cstack-statusline"; then
  exit 0
fi

# --- Case 3: cstack-core old versioned path — auto-update to stable wrapper.
if echo "$EXISTING_CMD" | grep -q "cstack-core.*statusline"; then
  bash "$INSTALL_SCRIPT" >/dev/null 2>&1
  exit 0
fi

# Cases 1 and 4 both nudge — skip if already nudged this session.
[ -n "$SESSION_FLAG" ] && [ -f "$SESSION_FLAG" ] && exit 0
[ -n "$SESSION_FLAG" ] && touch "$SESSION_FLAG"

# Read nudge count; cap at 3 sessions total.
COUNT=0
[ -f "$NUDGE_FILE" ] && COUNT=$(cat "$NUDGE_FILE" 2>/dev/null)
COUNT=${COUNT:-0}
[ "$COUNT" -ge 3 ] 2>/dev/null && exit 0

# Increment and persist.
echo $((COUNT + 1)) > "$NUDGE_FILE"
NUDGE_NUM=$((COUNT + 1))

# --- Case 1: No statusline configured.
if [ -z "$EXISTING_CMD" ]; then
  printf '{"additionalContext":"cstack-core: The statusline feature (shows pwd, git branch, model, tokens, and context %%) is available but not yet configured. This is nudge %d/3. Please let the user know and ask if they would like to install it. If yes, run: bash \\"%s\\""}' \
    "$NUDGE_NUM" "$INSTALL_SCRIPT"
  exit 0
fi

# --- Case 4: Foreign statusline configured — ask permission to replace.
printf '{"additionalContext":"cstack-core: A statusline is already configured but it does not come from cstack-core. The cstack-core statusline (shows pwd, git branch, model, tokens, and context %%) is available as a replacement. This is nudge %d/3. Please let the user know and ask if they would like to replace their current statusline with the cstack-core one. Install only if the user gives permission. If yes, run: bash \\"%s\\""}' \
  "$NUDGE_NUM" "$INSTALL_SCRIPT"

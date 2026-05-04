#!/bin/bash
# install-statusline.sh — Installer for the cstack-core statusline.
# Called by Claude when the user agrees to install or replace (via the nudge
# flow), or invoked manually via the /install-cstack-statusline skill.
# Writes a stable wrapper at ~/.claude/cstack-statusline.sh that always
# resolves the latest cached version at runtime — no path updates needed
# when cstack-core upgrades. Overwrites any existing statusLine configuration.

SETTINGS_FILE="$HOME/.claude/settings.json"
WRAPPER="$HOME/.claude/cstack-statusline.sh"
NUDGE_FILE="$HOME/.claude/.cstack-statusline-nudge"

# Require jq.
if ! command -v jq >/dev/null 2>&1; then
  echo "[cstack-core] ❌ jq is required to install the statusline. Install it and try again." >&2
  exit 1
fi

# Write the stable wrapper script.
cat > "$WRAPPER" <<'EOF'
#!/bin/bash
# cstack-statusline.sh — Stable entry point for the cstack-core statusline.
# Dynamically resolves the latest installed version of the plugin at runtime.
SCRIPT=$(ls -t "$HOME/.claude/plugins/cache/claude-stack/cstack-core/"/*/scripts/statusline/statusline.sh 2>/dev/null | head -1)
[ -n "$SCRIPT" ] && exec bash "$SCRIPT"
EOF
chmod +x "$WRAPPER"

# Create settings.json if it doesn't exist.
[ -f "$SETTINGS_FILE" ] || echo '{}' > "$SETTINGS_FILE"

# Write statusLine into settings.json pointing to the stable wrapper.
TMP=$(mktemp)
jq --arg cmd "bash \"$WRAPPER\"" \
  '.statusLine = {"type": "command", "command": $cmd}' \
  "$SETTINGS_FILE" > "$TMP" && mv "$TMP" "$SETTINGS_FILE"

# Clear the nudge counter.
rm -f "$NUDGE_FILE"

echo "[cstack-core] ✅ Statusline installed." >&2

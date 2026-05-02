# Skill: install-cstack-statusline

Install the cstack-core statusline for the user. Use this skill when the user invokes `/install-cstack-statusline` or explicitly asks to install or enable the cstack-core statusline.

## Steps

1. Find the install script in the plugin cache:
   ```bash
   ls -t "$HOME/.claude/plugins/cache/claude-stack/cstack-core/"/*/scripts/statusline/install-statusline.sh 2>/dev/null | head -1
   ```

2. If no path is returned, tell the user the cstack-core plugin does not appear to be installed.

3. If a path is found, run it:
   ```bash
   bash "<path from step 1>"
   ```

4. Report the result to the user. On success the script prints:
   `✅ Statusline installed. Restart Claude Code to see it.`

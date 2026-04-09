#!/bin/bash
set -euo pipefail

# PreToolUse hook: Block raw robot/make commands that bypass the ODK Docker wrapper.
# All ROBOT and Make commands must go through odk-docker-run.js to ensure
# they run inside the ODK container with correct mounts.

input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command // empty')

# If no command, allow (not a Bash call we care about)
if [ -z "$command" ]; then
  exit 0
fi

# Allow if the command goes through the Docker wrapper
if echo "$command" | grep -q 'odk-docker-run'; then
  exit 0
fi

# Block raw robot commands
if echo "$command" | grep -qE '(^|\s|;|&&|\|)robot\s'; then
  cat >&2 <<'EOF'
{
  "hookSpecificOutput": {
    "permissionDecision": "deny"
  },
  "systemMessage": "BLOCKED: Do not run 'robot' directly. Use the ODK Docker wrapper instead:\n  node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js \"<project_dir>\" \"robot <args>\"\nThis ensures ROBOT runs inside the ODK container with correct dependencies and mounts."
}
EOF
  exit 2
fi

# Block raw make commands targeting ontology directories
if echo "$command" | grep -qE '(^|\s|;|&&|\|)make\s'; then
  cat >&2 <<'EOF'
{
  "hookSpecificOutput": {
    "permissionDecision": "deny"
  },
  "systemMessage": "BLOCKED: Do not run 'make' directly. Use the ODK Docker wrapper instead:\n  node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js \"<project_dir>\" \"make <args>\"\nThis ensures Make runs inside the ODK container with correct dependencies and mounts."
}
EOF
  exit 2
fi

# Not a robot or make command, allow
exit 0

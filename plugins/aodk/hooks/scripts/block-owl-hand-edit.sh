#!/bin/bash
set -euo pipefail

# PreToolUse hook: Block Write/Edit tools targeting OWL ontology files.
# All OWL changes must go through OWL-MCP tools, never hand-edited.

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name // empty')
file_path=""

if [ "$tool_name" = "Write" ]; then
  file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')
elif [ "$tool_name" = "Edit" ]; then
  file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')
fi

# If no file path, allow (not a file operation we care about)
if [ -z "$file_path" ]; then
  exit 0
fi

# Check if the file has an OWL-related extension
case "$file_path" in
  *.owl|*.rdf|*.ofn|*.owx|*.ttl)
    cat >&2 <<'EOF'
{
  "hookSpecificOutput": {
    "permissionDecision": "deny"
  },
  "systemMessage": "BLOCKED: Do not edit OWL files directly with Write/Edit tools. Use the OWL-MCP tools (mcp__owl__add_axioms, mcp__owl__remove_axiom, mcp__owl__set_ontology_iri, etc.) for all ontology changes. This ensures correct OWL functional syntax and prevents parsing errors."
}
EOF
    exit 2
    ;;
  *)
    # Not an OWL file, allow
    exit 0
    ;;
esac

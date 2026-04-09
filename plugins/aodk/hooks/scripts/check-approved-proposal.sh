#!/bin/bash
set -euo pipefail

# PreToolUse hook: Block OWL-MCP write tools unless an approved PROPOSAL exists.
#
# Checks projects/*/plans/PROPOSAL-*.md files for "status: approved".
# If no approved proposal is found, denies the tool call with a message
# directing the agent back to Steps 4-5 of the workflow.
#
# Skipped when:
#   - The OWL file path points to a test-data file (CQ verification creates these)
#   - No projects/ directory exists (not in an ontology workflow)

input=$(cat)
tool_input=$(echo "$input" | jq -r '.tool_input // empty')

# Extract the OWL file path from the tool input
owl_path=$(echo "$tool_input" | jq -r '.owl_file_path // empty')

# Allow writes to test-data files (CQ verification creates these before approval isn't relevant)
if [[ -n "$owl_path" && "$owl_path" == *"test-data"* ]]; then
  exit 0
fi

# If no projects/ directory exists, skip the check (user may not be in an ontology workflow)
if [ ! -d "$CLAUDE_PROJECT_DIR/projects" ]; then
  exit 0
fi

# Look for any PROPOSAL file with status: approved
found_approved=false
for proposal in "$CLAUDE_PROJECT_DIR"/projects/*/plans/PROPOSAL-*.md; do
  # Handle glob that matches nothing
  [ -e "$proposal" ] || continue

  # Check for status: approved in the YAML frontmatter or body
  if grep -q 'status:\s*approved' "$proposal" 2>/dev/null; then
    found_approved=true
    break
  fi
done

if [ "$found_approved" = true ]; then
  # Approved proposal found — allow the tool call
  exit 0
else
  # Check if ANY proposal exists (draft or otherwise)
  has_any_proposal=false
  for proposal in "$CLAUDE_PROJECT_DIR"/projects/*/plans/PROPOSAL-*.md; do
    [ -e "$proposal" ] || continue
    has_any_proposal=true
    break
  done

  if [ "$has_any_proposal" = true ]; then
    # Draft proposals exist but none approved
    cat >&2 <<'EOF'
{
  "hookSpecificOutput": {
    "permissionDecision": "deny"
  },
  "systemMessage": "BLOCKED: A draft proposal exists but has not been approved yet. The ontology-builder workflow requires explicit user approval (Step 5) before formalization (Step 6). Present the draft to the user and wait for their approval. Update the proposal's status to 'approved' before retrying."
}
EOF
    exit 2
  else
    # No proposals at all
    cat >&2 <<'EOF'
{
  "hookSpecificOutput": {
    "permissionDecision": "deny"
  },
  "systemMessage": "BLOCKED: No proposal file found. The ontology-builder workflow requires drafting a proposal (Step 4) and getting user approval (Step 5) before formalization (Step 6). Create a PROPOSAL file in projects/<project_dir>/plans/ first."
}
EOF
    exit 2
  fi
fi

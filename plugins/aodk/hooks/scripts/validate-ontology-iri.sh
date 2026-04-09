#!/bin/bash
set -euo pipefail

# PreToolUse hook: Block set_ontology_iri calls that use CURIEs instead of full IRIs.
# CURIEs in the Ontology(...) header produce files that ROBOT cannot parse.

input=$(cat)
tool_input=$(echo "$input" | jq -r '.tool_input // empty')

iri=$(echo "$tool_input" | jq -r '.iri // empty')
version_iri=$(echo "$tool_input" | jq -r '.version_iri // empty')

# Allow null/empty IRIs (used to clear the IRI)
if [ -z "$iri" ] || [ "$iri" = "null" ]; then
  exit 0
fi

# A valid full IRI must start with http:// or https://
# CURIEs look like "ex:", "obo:something", "schema:Thing", etc.
if [[ "$iri" =~ ^https?:// ]]; then
  # Full IRI — check version_iri too if present
  if [ -n "$version_iri" ] && [ "$version_iri" != "null" ]; then
    if [[ ! "$version_iri" =~ ^https?:// ]]; then
      cat >&2 <<EOF
{
  "hookSpecificOutput": {
    "permissionDecision": "deny"
  },
  "systemMessage": "BLOCKED: version_iri '${version_iri}' looks like a CURIE, not a full IRI. Use a complete IRI starting with http:// or https:// (e.g. 'http://example.org/ontology/my-ontology/1.0'). CURIEs in the Ontology(...) header cause ROBOT parsing failures."
}
EOF
      exit 2
    fi
  fi
  exit 0
else
  cat >&2 <<EOF
{
  "hookSpecificOutput": {
    "permissionDecision": "deny"
  },
  "systemMessage": "BLOCKED: iri '${iri}' looks like a CURIE, not a full IRI. Use a complete IRI starting with http:// or https:// (e.g. 'http://example.org/ontology/my-ontology/'). CURIEs in the Ontology(...) header produce files that ROBOT cannot parse."
}
EOF
  exit 2
fi

---
name: odk-run
description: Run custom Make targets or ODK tools that have no dedicated skill. Use when the user wants a one-off make target or to run Konclude, jena, relation-graph, jinjanate, OORT, souffle, dicer-cli, yq-mf, or sssom-cli. Do not use for robot—use odk-robot instead.
version: 1.0.0
allowed-tools: [Read, Glob, Grep, Bash, Write]
---

# ODK Run Skill

Use this skill when the user needs to run a command that is **not** covered by a dedicated skill: either a **custom Make target** in the ontology dir, or one of the **other ODK tools** (Konclude, Apache Jena, relation-graph, jinjanate, ontology-release-runner, souffle, dicer-cli, yq-mf, sssom-cli).

Run commands via the Bash tool using the ODK Docker wrapper:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "<project_dir>" "<command>"
```

The container mounts the project directory (workspace root or `projects/<slug>`) as `/work`; use paths relative to that root.

For **ROBOT**, use the **odk-robot** skill instead.

## When to Use This Skill (by outcome)

- User wants a **one-off or custom Make target** → use with `command`: `make -C ontology <target>`
- User wants to run **Konclude**, **jena**, **relation-graph**, **jinjanate**, **OORT**, **souffle**, **dicer-cli**, **yq-mf**, or **sssom-cli** → use with `command` set to the full invocation

## Arguments

| Argument       | Type   | Required | Description |
|----------------|--------|----------|-------------|
| **command**    | string | yes      | Full command (no robot). E.g. `make -C ontology custom-target`, `Konclude -i edit.owl -o out.owl`. Paths relative to the mounted project root. |
| **project_dir** | string | no       | Optional. Project root to mount at `/work` (e.g. `projects/pizza`). Pass `""` to use current working directory. |

## Examples

```bash
# Custom make (workspace)
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "" "make -C ontology some-custom-target"

# Custom make (cloned project)
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "projects/owner-repo" "make -C ontology some-custom-target"

# Konclude
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "" "Konclude -i edit.owl -o classified.owl"
```

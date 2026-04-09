---
name: clone-project
description: Clone an ontology repository into the workspace's projects directory for local contribution. Use whenever the user wants to clone an ontology repo, set up a project locally, or get a copy to work on—e.g. "clone this ontology", "set up this repo locally", "get a copy of this project to work on". All subsequent work (edits, branch, PR) is done from the cloned project directory.
version: 1.0.0
allowed-tools: [Read, Glob, Grep, Bash, Write]
---

# Clone Project Skill

Use this skill when the user wants to **clone an ontology repository** so they can work on it in this workspace. Clones go into a single, predictable location: **`projects/<slug>/`** at the root of the workspace. All later steps (implement, ODK/ROBOT, branch, commit, PR) are performed **from that project directory**.

## When to Use

- User says **"clone this ontology"**, **"set up this repo locally"**, **"get a copy of this project to work on"**, or provides a repo URL to clone.
- As the second step in the external-contribution workflow (after **analyze-project**, or in parallel): clone into `projects/`, then work from the clone for implementation and PR.

## Workflow

1. **Resolve repo URL**: From the user's message or a prior analyze step, get the clone URL (e.g. `https://github.com/owner/repo`) and derive a **stable slug** (e.g. `owner-repo`) so the same repo always lands in the same path.
2. **Ensure `projects/` exists**: At the workspace root, create the directory `projects/` if it does not exist. The `projects/` directory is gitignored.
3. **Clone**: Run `git clone <url> projects/<slug>`. If `projects/<slug>` already exists, do not overwrite—report that the project is already cloned and offer to pull latest or use the existing clone.
4. **Verify build (optional but recommended)**: Use ROBOT with `project_dir` set to the clone path:
   ```bash
   node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "projects/<slug>" "robot --version"
   ```
   Report success or any failure.
5. **Tell the user**: Confirm the clone path (`projects/<slug>/`). For ODK/ROBOT commands, use the Docker wrapper with `project_dir` set to `projects/<slug>`. Git operations (branch, commit, PR) are done from the clone directory.

## Slug Convention

- Prefer a slug that is stable and readable: e.g. from `https://github.com/org/ontology-name` use `ontology-name`. Avoid spaces and characters that are problematic in paths.
- The same repo URL should always map to the same slug so repeated clones find the same folder.

## Working on the Clone

After cloning:

- **ODK/ROBOT**: Use the Docker wrapper with `project_dir`:
  ```bash
  node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "projects/<slug>" "robot verify --input ontology/edit.owl"
  ```
- **Other ODK tools** (Make, Konclude, etc.):
  ```bash
  node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "projects/<slug>" "make -C ontology test"
  ```
- **Ontology-editor**: Use absolute paths to OWL files in the clone (e.g. `/path/to/projects/owner-repo/ontology/edit.owl`).
- **Git operations** (branch, commit, push, PR): Perform from the clone root. The **create-pull-request** skill assumes the agent is in that directory.

## Prerequisites

- Git installed; network access to the clone URL.
- For running ODK/QC after clone: Docker as required by the target project.

## Output

- Report the clone path: `projects/<slug>/`.
- If build/QC was run, report pass/fail.
- Remind that subsequent steps (implement, branch, PR) are done from that directory.

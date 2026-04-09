---
name: analyze-project
description: Understand a target ontology repo's structure, contribution workflow, and build setup. Use whenever the user wants to analyze an ontology repository, learn how to contribute to a project, understand repo layout, or inspect CONTRIBUTING/issue/PR conventions—e.g. "analyze this ontology repo", "how do I contribute to this project", "what's the structure of this repo", or when they provide a repo URL. Prefer this skill over ad-hoc inspection when contributing to external ontologies.
version: 1.0.0
allowed-tools: [Read, Glob, Grep, Bash, WebFetch, WebSearch]
---

# Analyze Project Skill

Use this skill when the user wants to **understand a target ontology repository** before contributing or cloning. You produce a short, structured report so the user (or a follow-up clone/issue/PR workflow) knows the layout, build system, contribution rules, and issue/PR expectations.

## When to Use

- User says they want to **contribute to** or **work on** an external ontology and provides a repo URL (or repo owner/name).
- User asks **"how do I contribute to this project"**, **"what's the structure of this repo"**, **"analyze this ontology repo"**, or similar.
- Before cloning or picking issues: analyzing first avoids wrong paths and missed conventions.

Use **web fetch or search** (and optionally terminal to list files if the repo is already cloned under `projects/`). Do **not** clone the repo only to analyze it—use the GitHub repo page, README, CONTRIBUTING, and `.github` structure from the web or from an existing clone.

## Workflow

1. **Identify the repo**: From the user's message, get the repo URL or `owner/repo` (e.g. from a GitHub link).
2. **Gather structure**: Fetch or read:
   - **README**: scope, build instructions, where ontology source lives (often `ontology/` or the project's edit directory).
   - **Top-level layout**: key dirs (e.g. `ontology/`, `imports/`, `subsets/`, `mappings/`, `docs/`, `.github/`).
   - **Build system**: ODK Makefile, Docker, CI (e.g. `.github/workflows/*.yml`), and how to run tests/QC (e.g. `make test`, `make -C ontology test`).
   - **CONTRIBUTING** (or "Contributing" in README): issue-first?, required fields for new term requests, link to editor guides or OBO Academy.
   - **Issue/PR conventions**: presence of `.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE.md`, CODEOWNERS; common labels and branch naming (e.g. `issue-N`, `feature/term-name`).
3. **Synthesize**: Produce a short **structure report** (see Output format below).

## Output Format

Return a concise report with:

- **Layout**: Top-level directories and where the ontology edit file / Makefile lives (e.g. `ontology/`). Note the **Make path** (path to the Makefile directory relative to repo root, e.g. `ontology`) so ROBOT can be called with the correct path when working on a clone.
- **Build and CI**: How to build and run QC locally (e.g. ODK Docker, `make -C ontology test`); what CI runs on PRs.
- **Contributing**: Issue-first? Where to find CONTRIBUTING; main contribution types (e.g. new term request, synonym, obsoletion).
- **Issue/PR expectations**: Any issue templates (NTR, bug, etc.); PR checklist or description expectations (e.g. "Closes #N", change table); review expectations if visible.

## Notes

- If the repo is already cloned under `projects/<slug>/`, you may list files and read CONTRIBUTING/README from disk instead of (or in addition to) fetching from the web.
- This skill does not clone; use the **clone-project** skill to clone into `projects/<slug>/` after (or in parallel with) analysis.

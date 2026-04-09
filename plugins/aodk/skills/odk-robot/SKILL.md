---
name: odk-robot
description: Run ROBOT for ontology QC, merge, reason, convert, template, or query. Use whenever the user needs to verify an ontology, validate OWL profile, merge OWL files, run a reasoner, convert OWL/OBO, build terms from CSV+template, or run SPARQL/DL over an ontology—e.g. "run robot verify", "merge these OWL files", "convert to OBO", "template from this CSV". This is the only skill for ROBOT; do not use odk-run for robot.
version: 1.0.0
allowed-tools: [Read, Glob, Grep, Bash, Write]
---

# ODK Robot Skill

Use this skill when the user needs to **run ROBOT** for: **verify** (rule-based QC), **validate** OWL 2 profile, **merge** ontologies, **reason** (classification/inference), **convert** format (OWL ↔ OBO etc.), **template** (generate terms from CSV + template), or **query** (SPARQL or DL).

Run ROBOT via the Bash tool using the ODK Docker wrapper:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "<project_dir>" "robot <robot_args>"
```

**Paths**: The ODK Docker wrapper mounts a project directory at `/work`. Paths in `robot_args` are **relative to that mounted root**.

- **Workspace ontology** (no `project_dir`): Pass an empty string `""` as project_dir. The current working directory is mounted; paths are relative to it (e.g. `ontology/edit.owl`).
- **Cloned project** under `projects/<slug>/`: Pass `project_dir` = the clone root (e.g. `projects/owner-repo`). Paths in `robot_args` are then relative to the clone root.

## When to Use This Skill (by outcome)

- User wants **QC / rule checks** on an OWL file → use **verify**.
- User wants to **check OWL 2 profile** (e.g. DL) → use **validate-profile**.
- User wants a **single merged OWL file** from several inputs → use **merge**.
- User wants **reasoning** (classification, consistency, inferred axioms) → use **reason**.
- User wants **format conversion** (e.g. OWL to OBO, RDF/XML to functional) → use **convert**.
- User wants to **generate or update terms** from a ROBOT template and CSV → use **template**.
- User wants to **run a SPARQL or DL query** and get results → use **query**.
- User wants **other ROBOT subcommands** (annotate, extract, filter, report, etc.) → use with the appropriate `robot_args`.

## What Each ROBOT Subcommand Does and How to Use It

### verify

**What it does**: Runs rule-based checks on an ontology (e.g. required annotations, logical consistency). Produces a report of violations or success.

**Example** (verify and write report):
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "" "robot verify --input edit.owl --output report.txt"
```

### validate-profile

**What it does**: Checks whether the ontology conforms to an OWL 2 profile (e.g. OWL 2 DL).

**Example**:
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "" "robot validate-profile --input edit.owl --profile DL"
```

### merge

**What it does**: Merges two or more OWL files into one ontology.

**Example**:
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "" "robot merge --inputs ontology/a.owl ontology/b.owl --output merged.owl"
```

### reason

**What it does**: Runs a reasoner (e.g. ELK, HermiT) to classify the ontology and optionally output inferred axioms.

**Example** (reason with ELK):
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "" "robot reason --input edit.owl --reasoner elk --output reasoned.owl --annotate-inferred-axioms true"
```

### convert

**What it does**: Converts between ontology formats (e.g. RDF/XML, OWL functional, OBO).

**Example** (OWL to OBO):
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "" "robot convert --input edit.owl --output edit.obo --format obo"
```

### template

**What it does**: Builds or updates ontology terms from a ROBOT template (CSV + template YAML).

**Example**:
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "" "robot template --template templates/terms.yaml --input terms.csv --output terms.owl"
```

### query

**What it does**: Runs a SPARQL or DL query over an ontology and writes results (e.g. to CSV).

**Example** (SPARQL):
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "" "robot query --input edit.owl --query query.rq results.csv"
```

### Other subcommands

**annotate**, **extract**, **filter**, **report**, **remove**, **rename**, **repair**, **collapse**, **expand**, **diff**, **explain**, **materialize**, **measure**, **mirror**, **reduce**, **relax**, **unmerge**, etc. See [ROBOT documentation](http://robot.obolibrary.org/) for each subcommand.

**Example** (extract subset):
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "" "robot extract --input edit.owl --term-file terms.txt --output subset.owl"
```

## When Not to Use This Skill

- **owltools, Konclude, jena, relation-graph, Make targets, etc.** → use **odk-run** skill.

## Arguments

| Argument       | Type   | Required | Description |
|----------------|--------|----------|-------------|
| **robot_args** | string | yes      | The full ROBOT subcommand and options. Paths relative to the mounted project root (e.g. `ontology/edit.owl`). |
| **project_dir** | string | no       | Optional. When working on a **cloned** or project dir under `projects/<slug>/`, set to that root (e.g. `projects/pizza`, `projects/owner-repo`). Omit or pass `""` for the workspace ontology. |

## Examples

```bash
# Verify (workspace)
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "" "robot verify --input ontology/edit.owl --output report.txt"

# Validate profile (cloned project)
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "projects/owner-repo" "robot validate-profile --input ontology/edit.owl --profile DL"

# Reason
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "" "robot reason --input ontology/edit.owl --reasoner elk --output reasoned.owl"

# Merge
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "" "robot merge --inputs ontology/a.owl ontology/b.owl --output merged.owl"

# Convert
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "" "robot convert --input ontology/edit.owl --output edit.obo --format obo"

# Query
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "" "robot query --input ontology/edit.owl --query query.rq results.csv"

# Version
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "" "robot --version"
```

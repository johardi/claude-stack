---
name: ontology-editor
description: Read, edit, and manage OWL ontologies with OWL-MCP (axioms, prefixes, metadata, pitfall scanning). Use whenever the user wants to add or remove axioms, search axioms, add prefixes, set the ontology IRI, inspect ontology metadata, scan for pitfalls, or formalize an ontology in OWL—e.g. "add this axiom", "find axioms for class X", "add prefix", "check for pitfalls". Align with Ontology Builder workflow (formalization step); use absolute paths for OWL files. Never edit OWL files by hand.
version: 1.0.0
allowed-tools: [Read, Glob, Grep, Bash, Write, mcp__owl__add_axiom, mcp__owl__add_axioms, mcp__owl__remove_axiom, mcp__owl__find_axioms, mcp__owl__get_all_axioms, mcp__owl__add_prefix, mcp__owl__ontology_metadata, mcp__owl__get_labels_for_iri, mcp__owl__set_ontology_iri, mcp__owl__test_pitfalls]
---

# Ontology Editor Skill

Use this skill when you need to **inspect or modify OWL ontology files** in this project. **Never edit OWL files directly**—use these tools for all axiom, prefix, and metadata changes. The tools are provided by the OWL-MCP server and operate on OWL files by **absolute file path**.

## When to Use

- **Step 6 (Formalization)** in the Ontology Builder workflow: add axioms, prefixes, and annotations to an OWL file after the user has approved the draft.
- **Ontology navigation**: find axioms, get all axioms, or read ontology metadata for an existing file.
- **Ontology editing**: add/remove axioms in OWL functional syntax; add prefix mappings; set the ontology IRI.
- **Quality checking**: scan for common modeling pitfalls (OOPS!-style checks).

Align with the project's workflow: work top-down, get user approval before large edits, and keep changes in formal OWL (functional syntax recommended).

## How the Server Works

- **File path**: Every tool takes `owl_file_path` — an **absolute path** to the OWL file (e.g. `C:\Users\...\ontology.owl` or `/path/to/ontology.owl`). The server loads the file on first access and syncs in-memory state with disk on writes.
- **Syntax**: Axioms are strings in **OWL functional syntax** (e.g. `SubClassOf(:Dog :Animal)`, `Declaration(Class(:Cat))`).

## Tools Overview

### Axioms

| Tool | Purpose |
|------|--------|
| **mcp__owl__add_axiom** | Add one axiom (e.g. `SubClassOf(:A :B)`). Params: `owl_file_path`, `axiom_str`. |
| **mcp__owl__add_axioms** | Add multiple axioms in one call. Params: `owl_file_path`, `axiom_strs` (array). |
| **mcp__owl__remove_axiom** | Remove one axiom (exact match). Params: `owl_file_path`, `axiom_str`. |
| **mcp__owl__find_axioms** | Search axioms by regex pattern; optional labels, limit, custom annotation property. Params: `owl_file_path`, `pattern`, `limit`, `include_labels`, `annotation_property` (nullable). |
| **mcp__owl__get_all_axioms** | Return all axioms (up to limit); optional labels, custom annotation property. Params: `owl_file_path`, `limit`, `include_labels`, `annotation_property` (nullable). |

### Prefixes, Metadata, and IRI Management

| Tool | Purpose |
|------|--------|
| **mcp__owl__add_prefix** | Add a prefix mapping (e.g. prefix `ex:` → `http://example.org/`). Params: `owl_file_path`, `prefix`, `uri`. |
| **mcp__owl__ontology_metadata** | Get ontology-level annotation axioms (metadata header). Params: `owl_file_path`. |
| **mcp__owl__get_labels_for_iri** | Get label(s) for a given IRI or CURIE; optional custom annotation property. Params: `owl_file_path`, `iri`, `annotation_property` (nullable). |
| **mcp__owl__set_ontology_iri** | Set or update the ontology IRI and optional version IRI. Pass `iri: null` to clear. Params: `owl_file_path`, `iri` (nullable), `version_iri` (nullable). |

### Quality Checks

| Tool | Purpose |
|------|--------|
| **mcp__owl__test_pitfalls** | Scan for common modeling pitfalls (31 OOPS!-inspired checks). Returns a JSON report listing detected issues, severity, and affected elements. Optionally filter by pitfall IDs. Params: `owl_file_path`, `pitfalls` (nullable, comma-separated IDs e.g. `"P04,P08,P11"`). |

**Available pitfall checks:** P02 (synonym classes), P03 ("is" relationship), P04 (unconnected elements), P05 (wrong inverses), P06 (class hierarchy cycles), P07 (merged concepts), P08 (missing annotations), P10 (missing disjointness), P11 (missing domain/range), P12 (undeclared equivalent properties), P13 (missing inverses), P19 (multiple domains/ranges), P20 (misused annotations), P21 (miscellaneous class), P22 (inconsistent naming), P24 (recursive definitions), P25 (self-inverse), P26 (inverse of symmetric), P27 (wrong equivalent properties), P28 (wrong symmetric), P29 (wrong transitive), P30 (undeclared equivalent classes), P31 (wrong equivalent classes), P32 (duplicate labels), P33 (single-property chain), P34 (untyped class), P35 (untyped property), P36 (URI file extension), P38 (no ontology declaration), P39 (ambiguous namespace), P41 (no license).

## Usage Tips

1. **Always use absolute paths**: Pass the full absolute path in `owl_file_path` to ensure the MCP server can resolve the file regardless of working directory.
2. **Finding content**: Call `mcp__owl__find_axioms` with a regex pattern; set `include_labels: true` for human-readable labels appended as `##` comments. Use `annotation_property` to override the default `rdfs:label` (e.g. for `skos:prefLabel`).
3. **Adding axioms**: Use OWL functional syntax. Add one axiom per call with `mcp__owl__add_axiom`, or batch with `mcp__owl__add_axioms`. Ensure required prefixes exist (e.g. `owl`, `rdf`, `rdfs`, `xsd`); add custom ones with `mcp__owl__add_prefix`.
4. **Setting the ontology IRI**: Use `mcp__owl__set_ontology_iri` to establish the ontology IRI and version IRI before adding axioms to a new file. **Always pass full IRIs** (e.g. `"http://example.org/ontology/my-ontology/"`), never CURIEs (e.g. `"ex:"`). CURIEs in the `Ontology(...)` header produce files that ROBOT cannot parse.
5. **Project workflow**: After the user approves a draft (Step 5), use these tools to implement the change in the OWL file (Step 6), then run `mcp__owl__test_pitfalls` as part of automated review (Step 7).
6. **Imports**: Add import axioms via `mcp__owl__add_axiom` using **full IRIs in angle brackets**: `Import(<http://purl.obolibrary.org/obo/bfo.owl>)`. Never use CURIEs in `Import(...)` (e.g. `Import(obo:bfo.owl)` is invalid and will cause ROBOT parsing failures).
7. **Annotating the ontology itself**: When the subject of an `AnnotationAssertion` is the ontology (e.g. for `rdfs:label`, `rdfs:comment`, `dcterms:license`), use the **full ontology IRI** as the subject, not a bare CURIE. Example: `AnnotationAssertion(rdfs:label <http://example.org/ontology/my-ontology/> "My Ontology"@en)`.

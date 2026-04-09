---
name: cq-verification
description: Verify competency questions against an OWL ontology using SPARQL queries with test data. Use to verify every CQ with real query execution. Also use whenever the user asks to test, validate, or verify an ontology against its CQs, run SPARQL verification, check CQ coverage, or asks "does the ontology answer the competency questions?"—e.g. "verify CQs", "test the ontology", "run CQ checks", "validate against competency questions".
version: 1.0.0
allowed-tools: [Read, Glob, Grep, Bash, Write, mcp__owl__add_axiom, mcp__owl__add_axioms, mcp__owl__add_prefix, mcp__owl__set_ontology_iri, mcp__owl__find_axioms]
---

# CQ Verification Skill

Use this skill during **Step 7 (Automated Review)** to verify that the ontology can answer every competency question.

## The Core Problem This Solves

A common mistake is running SPARQL queries against hand-crafted test triples without loading the ontology schema. This only tests whether the test data was constructed correctly — not whether the ontology itself supports the queries. For example, a query like `?x :relatedTo ?y` will succeed against raw triples that contain that pattern, even if the ontology doesn't define `:relatedTo` at all.

To truly verify the ontology, queries must run against a file that contains **both** the ontology schema (classes, properties, axioms) and test individuals. This is what `robot merge` provides — it loads both files by local path into a single in-memory model, making class hierarchies, domains/ranges, and equivalences available to the query engine.

## Procedure

### Phase 0 — Plan and Create Test Data

Before writing any individuals, read the CQ list from the approved proposal and **plan the test data**. For each CQ, note which classes and properties it exercises, and which individuals and assertions are needed to produce a non-empty result.

A quick planning table helps (you don't need to write this to a file — it's a mental model):

| CQ | Needs individuals of | Needs property assertions |
|----|---------------------|--------------------------|
| CQ01: What items belong to a given category? | :Item, :Category | :belongsTo |
| CQ02: Who created a given item? | :Item, :Person | :createdBy |

This planning step prevents two common problems: (1) creating individuals that no query uses, and (2) missing assertions that leave queries returning empty results.

**Create the test data file** at `projects/<project_dir>/queries/test-data.owl` using the OWL-MCP tools:

1. Call `mcp__owl__set_ontology_iri` on the test data file with a distinct IRI (e.g. append `/test-data` to the main ontology's namespace)
2. Add the same prefixes as the main ontology using `mcp__owl__add_prefix`
3. Add test individuals using `mcp__owl__add_axioms` — declarations, class assertions, and property assertions

Example axioms (OWL functional syntax):

```
Declaration(NamedIndividual(:item1))
ClassAssertion(:Item :item1)
DataPropertyAssertion(:hasName :item1 "Example Item")
ObjectPropertyAssertion(:belongsTo :item1 :category1)
```

**Do not add `Import(...)` axioms to this file.** Import statements require either a resolvable URL or an XML catalog mapping the IRI to a local path. Since ontology IRIs like `http://example.org/...` are not real URLs, the import will silently fail — ROBOT will load the test data without the ontology schema, and queries will pass trivially by pattern matching. Use `robot merge` in Phase 2 instead, which loads both files by local path.

Keep the test data **minimal** — only the individuals and assertions needed by the CQs. One or two individuals per class is usually enough.

### Phase 1 — Write All Queries

For every CQ in the approved proposal (section 2), write a SPARQL SELECT query. Save each as `projects/<project_dir>/queries/CQnn.rq` (e.g. `CQ01.rq`, `CQ02.rq`).

Each `.rq` file should:

1. Start with a comment containing the CQ text: `# CQ01: What items belong to a given category?`
2. Declare all necessary prefixes
3. Use a concrete test individual as the "given" entity (e.g. `:category1` from the test data)
4. SELECT the variables that answer the question

**Common query patterns:**

- **Binary relationship** ("Which X belongs to Y?"): straightforward triple pattern

```sparql
# CQ01: What items belong to a given category?
PREFIX : <http://example.org/my-ontology#>
SELECT ?item ?name WHERE {
  ?item :belongsTo :category1 .
  ?item :hasName ?name .
}
```

- **Data property** ("What is the name of X?"): match a literal value

```sparql
# CQ02: What is the name of a given item?
PREFIX : <http://example.org/my-ontology#>
SELECT ?name WHERE {
  :item1 :hasName ?name .
}
```

- **Type/classification** ("What kind of X is this?"): check `rdf:type`

```sparql
# CQ03: What type is a given item?
PREFIX : <http://example.org/my-ontology#>
SELECT ?type WHERE {
  :item1 a ?type .
  FILTER(?type IN (:TypeA, :TypeB))
}
```

- **Schema/hierarchy** ("Which subtypes of X exist?"): uses `rdfs:subClassOf` from the ontology — this is why the merge step matters

```sparql
# CQ04: Which subtypes of Role exist?
PREFIX : <http://example.org/my-ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?subtype ?label WHERE {
  ?subtype rdfs:subClassOf :Role .
  OPTIONAL { ?subtype rdfs:label ?label }
}
```

**Write all query files before executing any.** This prevents the pattern of writing one, running it, getting distracted, and never finishing the rest.

### Phase 1.5 — Pre-flight: Validate OWL File for ROBOT Compatibility

Before running any ROBOT commands, read the first ~15 lines of the ontology OWL file and check for these known issues that prevent ROBOT from parsing the file:

1. **CURIEs in the `Ontology(...)` header** — The `Ontology(...)` declaration must use full IRIs in angle brackets, not CURIEs. ROBOT's OWLAPI parser rejects CURIEs in this position.

   Bad: `Ontology(ex: ex:1.0`
   Good: `Ontology(<http://example.org/my-ontology/> <http://example.org/my-ontology/1.0>`

2. **CURIEs in `Import(...)` statements** — Import IRIs must be full IRIs in angle brackets.

   Bad: `Import(obo:bfo.owl)`
   Good: `Import(<http://purl.obolibrary.org/obo/bfo.owl>)`

3. **Bare CURIEs as annotation subjects** — When the ontology itself is the subject of an `AnnotationAssertion`, the subject must be the full IRI, not a bare prefix like `ex:`.

   Bad: `AnnotationAssertion(rdfs:label ex: "My Ontology")`
   Good: `AnnotationAssertion(rdfs:label <http://example.org/my-ontology/> "My Ontology")`

**If any of these are found**, fix them before proceeding:

- Use `mcp__owl__set_ontology_iri` with the **full IRI** (not a CURIE) to fix the `Ontology(...)` header.
- For `Import(...)` and `AnnotationAssertion` issues, use `mcp__owl__remove_axiom` to remove the broken axiom and `mcp__owl__add_axiom` to re-add it with the full IRI in angle brackets.

**Why this matters:** The ontology-editor tools (owl-mcp) produce OWL functional syntax. If the agent passed CURIEs instead of full IRIs to `mcp__owl__set_ontology_iri` or to `Import(...)` axioms during formalization, the resulting file will look valid but ROBOT will reject it with "INVALID ONTOLOGY FILE ERROR." The convert fallback below also fails on these files — you must fix the source syntax first.

### Phase 2 — Execute Queries

Use ROBOT to merge the ontology with the test data, then run each query against the merged result.

**Step 1 — Merge ontology + test data:**

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "projects/<project_dir>" "robot merge --input ontology/<name>.owl --input queries/test-data.owl --output queries/merged.owl"
```

The merge produces a single file with both TBox and ABox. Paths in the command are relative to the project directory.

**If merge fails** with a parsing error even after pre-flight checks pass, convert the ontology to RDF/XML first:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "projects/<project_dir>" "robot convert --input ontology/<name>.owl --output queries/ontology-rdfxml.owl --format owl"
```

Then merge using the converted file. Do **not** work around merge failures by manually copying axioms between files — this defeats schema-aware verification.

**Step 2 — Run queries in batches:**

ROBOT supports multiple `--query` flags in one call. Batch queries to reduce tool calls:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/odk-docker-run.js "projects/<project_dir>" "robot query --input queries/merged.owl --query queries/CQ01.rq queries/results/CQ01.csv --query queries/CQ02.rq queries/results/CQ02.csv --query queries/CQ03.rq queries/results/CQ03.csv"
```

Batch 5–10 queries per call. Create the `queries/results/` directory before running the first batch if it doesn't exist.

Read each output CSV to check the results.

**What results mean:**

- **Rows with expected individuals** → the ontology supports this CQ. Pass.
- **Zero rows** → either the test data is missing the necessary assertions, or the ontology is missing a class/property. Investigate which.
- **Query error** (syntax error, unknown prefix) → fix the `.rq` file and re-run.

**When something fails:**

- Fix the root cause (query, test data, or ontology)
- After any change to the ontology or test data, **always re-run the merge** before re-running queries — the merged file is stale otherwise
- If the ontology itself needed changes, return to Step 6 (formalization) to apply them via OWL-MCP tools

### Phase 3 — Report

Present results as a summary table covering every CQ:

| CQ | Question | Query File | Result | Notes |
|----|----------|------------|--------|-------|
| CQ01 | What items belong to a given category? | CQ01.rq | PASS (1 row) | Returned item1 |
| CQ02 | Who created a given item? | CQ02.rq | FAIL (0 rows) | Missing createdBy in test data |

Every CQ must appear in the table. If any CQ fails due to an ontology gap, fix the ontology and re-run.

## Common Pitfalls

### ROBOT fails with "INVALID ONTOLOGY FILE ERROR"

This almost always means CURIEs were used where full IRIs are required (see **Phase 1.5**). Run the pre-flight checks first. If those pass and ROBOT still fails, convert the file to RDF/XML as described in Phase 2. Never copy axioms between files via `mcp__owl__get_all_axioms` + `mcp__owl__add_axioms` as a workaround — this defeats schema-aware verification.

### Running queries one at a time

This wastes tool calls. Always batch using multiple `--query` flags as shown in Phase 2.

### Forgetting to re-merge after changes

If you fix a query, test data, or the ontology, the `merged.owl` file is stale. Always re-run the merge before re-running queries.

### Clean Up

After all CQs pass, delete `queries/merged.owl` and any intermediate conversion files (e.g. `queries/ontology-rdfxml.owl`) — they are build artifacts. Keep the test data and query files as project deliverables.

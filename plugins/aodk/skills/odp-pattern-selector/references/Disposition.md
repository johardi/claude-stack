# Disposition

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Disposition
**OWL Building Block:** (Roehl-jansen_disposition-pattern.owl — local to the pattern submission)

## Intent

This pattern allows the representation of non-probabilistic dispositions with unique triggering and realization process types.

## Competency Questions

- What is the triggering process for a given disposition? (e.g., a dose of penicillin can unfold its antibiotic disposition when being swallowed.)
- What is the realization of a given disposition? (e.g., developing a fever rash.)

## Domains

- Upper Ontology
- Biology
- General

## Solution Description

Relations are defined between dispositions, their realization processes, and their triggering processes. The pattern is easily compatible with many top-level ontologies. In this description, classes from BFO and BioTop are used.

References:
- Roehl/Jansen: "Representing Dispositions", Journal of Biomedical Semantics 2011, 2(Suppl 4):S4.
- BioTop: http://www.imbi.uni-freiburg.de/ontology/biotop/

## Elements

### Classes

- **Bearer** — (BFO: independent continuant; BioTop: material object) The entity that bears the disposition.
- **Disposition** — (BFO: dependent continuant > realizable > disposition; BioTop: disposition) The dispositional property itself.
- **Trigger** — (BFO: process; BioTop: process) The process that triggers the disposition.
- **Realization** — (BFO: process; BioTop: process) The process that realizes the disposition.

### Object Properties

- **hasDisposition** — Subrelation of bearerOf. Expresses that certain types of things have a certain disposition essentially. All instances will have instances of the disposition type inhering in them. E.g., all aspirin pills have the disposition to relieve pain.
- **inheresIn** — Expresses the relation between a disposition and its bearer. Even if particular dispositions are of the same type, their bearers do not have to be of the same type. E.g., both aspirin and paracetamol can bear the same type of pain-relief disposition.
- **hasTriggerR** — Relation between the realization process and the triggering process. E.g., dropping of the glass and its breaking.
- **hasTriggerD** — Relation between the disposition and the triggering process. E.g., fragility of the glass and the dropping event.
- **hasRealization** — Connects a disposition instance with any process instance which is its realization. A type of process R is the realization type of a disposition type D if and only if whenever any instance of D is realized, the realization is of type R.

## Consequences

Not explicitly stated. The pattern enables formal reasoning about dispositional properties, their triggers, and their realizations in ontologies aligned with BFO or similar upper ontologies.

## Scenarios

No explicit scenarios provided. Typical applications include:
- Modeling drug dispositions in pharmacology (e.g., penicillin's antibiotic disposition).
- Modeling material properties (e.g., fragility of glass).

## Related Patterns

- Aligns with **BFO** (Basic Formal Ontology) disposition hierarchy.
- Compatible with **BioTop** ontology.

## Additional Information

- Submitted by: Ludger Jansen
- Also Known As: Non-propositional Disposition

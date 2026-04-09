# Provenance

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Provenance
**OWL Building Block:** https://raw.githubusercontent.com/cogan-shimizu-wsu/ProvenanceOWL/master/EntityWithProvenanceOntologyPattern.owl

## Intent

Extracted core of PROV-O. This pattern captures the essential provenance concepts from the W3C PROV-O ontology, providing a lightweight way to represent the provenance (origin, derivation, and history) of entities.

## Competency Questions

Not explicitly listed. Implied questions from PROV-O semantics include:
- What entity was this derived from?
- Who or what was responsible for generating this entity?
- What activity produced this entity?
- When was this entity generated?

## Domains

- General
- Data Management
- Provenance

## Solution Description

Extracted core of PROV-O (W3C Provenance Ontology). The pattern provides a minimal set of classes and properties for tracking the origin and derivation history of entities, based on the PROV data model.

## Elements

### Classes

- **Entity** — A physical, digital, conceptual, or other kind of thing with some fixed aspects; entities may be real or imaginary.
- **Activity** — Something that occurs over a period of time and acts upon or with entities; it may include consuming, processing, transforming, modifying, relocating, using, or generating entities.
- **Agent** — Something that bears some form of responsibility for an activity taking place, for the existence of an entity, or for another agent's activity.

### Object Properties

- **wasDerivedFrom** — Relates an entity to another entity from which it was derived.
- **wasGeneratedBy** — Relates an entity to the activity that generated it.
- **wasAttributedTo** — Relates an entity to the agent that is attributed with its creation.
- **used** — Relates an activity to an entity it used.
- **wasAssociatedWith** — Relates an activity to an agent that was associated with it.

## Consequences

Enables lightweight provenance tracking without requiring the full PROV-O ontology. Suitable for recording the origin and derivation chain of entities in any domain.

## Scenarios

No explicit scenarios provided. Typical usage includes tracking the provenance of data transformations, document authorship, and derivation chains.

## Related Patterns

- **PROV-O** — Full W3C Provenance Ontology from which this pattern is extracted.

## Additional Information

- Submitted by: Cogan Shimizu
- Based on: W3C PROV-O (https://www.w3.org/TR/prov-o/)

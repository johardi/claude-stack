# Part Of

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:PartOf
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/partof.owl
**Also Known As:** part whole
**Extracted From:** http://www.loa-cnr.it/ontologies/DUL.owl

## Intent

To represent entities and their parts.

## Competency Questions

- What is this entity part of?
- What are the parts of this entity?

## Domains

- Parts and Collections

## Solution Description

This is a basic pattern for transitive part-whole relations. It introduces a single class (Entity) and a pair of inverse transitive object properties (hasPart / isPartOf) that can hold between any entities.

## Elements

### Classes

- **Entity** (owl:Class) — Anything: real, possible, or imaginary, which some modeller wants to talk about for some purpose.

### Object Properties

- **hasPart** (owl:ObjectProperty) — A transitive relation expressing parthood between any entities, e.g. "the human body has a brain as part". When specializing this pattern, take care of restricting the domain and range appropriately, since it could be counterintuitive to use this relation arbitrarily, e.g. between animals and planets. For an intransitive part-of pattern, see Componency.
- **isPartOf** (owl:ObjectProperty) — A transitive relation expressing parthood between any entities, e.g. "brain is a part of the human body". Inverse of hasPart. When specializing this pattern, take care of restricting the domain and range appropriately. For an intransitive part-of pattern, see Componency.

### Data Properties

None.

## Consequences

This pattern allows designers to represent entities and their parts (part-whole relations) with transitivity. The temporal aspect of this relation cannot be expressed with this pattern; to address this, the TimeIndexedPartOf pattern can be used. For an intransitive part-of pattern, see Componency.

## Scenarios

- Brain and heart are parts of the human body; substantia nigra is part of brain.

## Related Patterns

- **Componency** — intransitive (proper) part-of relation
- **TimeIndexedPartOf** — part-of with temporal indexing
- **Constituency** — constituents of a layered structure

## Additional Information

- **Specialization Of:** (none)
- **Has Components:** (none)
- **Examples (OWL):** http://www.ontologydesignpatterns.org/cp/examples/partof/humanbodyparts.owl

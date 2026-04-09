# Constituency

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Constituency
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/constituency.owl
**Extracted From:** http://www.loa-cnr.it/ontologies/DUL.owl

## Intent

To represent the constituents of a layered structure.

## Competency Questions

- Which are the constituents of this entity?
- What does this entity constitute (what is it a constituent of)?

## Domains

- Parts and Collections

## Solution Description

Constituency depends on some layering of the world described by the ontology. For example, scientific granularity (e.g. body-organ-tissue-cell) or ontological "strata" (e.g. social-mental-biological-physical) are typical layerings. Intuitively, a constituent is a part belonging to a lower layer. Since layering is actually a partition of the world, constituents are not properly classified as parts, although this kinship can be intuitive for common sense.

## Elements

### Classes

- **Entity** (owl:Class) — Anything: real, possible, or imaginary, which some modeller wants to talk about for some purpose.

### Object Properties

- **hasConstituent** (owl:ObjectProperty) — Relates an entity to its constituents across ontological layers. Examples include: wood pieces constituting a table, persons constituting a social system, molecules constituting a person, atoms constituting a river. In all these examples, there is a typical discontinuity between the constituted and the constituent object: e.g. a table is conceptualized at a functional layer, while wood pieces are at a material layer; a social system is at a different layer from the persons that constitute it.
- **isConstituentOf** (owl:ObjectProperty) — The inverse of hasConstituent.

### Data Properties

None.

## Consequences

A desirable advantage of this pattern is that we are able to talk e.g. of physical constituents of non-physical objects (e.g. systems), while this is typically impossible in terms of parts. This pattern must be distinguished from PartOf, CollectionEntity, and Componency patterns.

## Scenarios

- Different types of wood constitute this table.
- Persons constitute a social system.
- Molecules constitute a person.
- Atoms constitute a river.

## Related Patterns

- **PartOf** — transitive part-of (different: constituency crosses ontological layers)
- **Componency** — intransitive proper part (different: componency is within the same layer)
- **CollectionEntity** — membership in collections (different semantics)

## Additional Information

- **Specialization Of:** (none)
- **Has Components:** (none)

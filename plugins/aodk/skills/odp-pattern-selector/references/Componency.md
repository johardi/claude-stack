# Componency

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Componency
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/componency.owl
**Also Known As:** composition
**Extracted From:** http://www.loa-cnr.it/ontologies/DUL.owl

## Intent

To represent (non-transitively) that objects either are proper parts of other objects, or have proper parts.

## Competency Questions

- What is this object component of?
- What are the components of this object?

## Domains

- Parts and Collections

## Solution Description

This pattern distinguishes between parts and proper parts. The relation of proper part (hasComponent / isComponentOf) is not transitive, and implies a simple part-of relation (from the PartOf pattern), which is transitive. The pattern uses a transitive reduction logical pattern to preserve transitivity on the superproperty from the PartOf pattern.

## Elements

### Classes

- **Object** (owl:Class) — Any physical, social, or mental object, or a substance. Can be component only of other objects, and can be composed of only other objects.

### Object Properties

- **hasComponent** (owl:ObjectProperty) — The hasPart relation without transitivity, holding between an Object (the system) and another Object (the component), and assuming a Design that structures the system Object. The PartOf pattern acts here as the transitive reduction of the Componency pattern.
- **isComponentOf** (owl:ObjectProperty) — The inverse of the hasComponent object property.

### Data Properties

None.

## Consequences

This pattern allows designers to represent part-whole relations. It allows distinguishing between parts and proper parts. The relation of proper part is not transitive, and implies a simple part-of relation (from PartOf), which is transitive. Temporal indexing is not expressible. To solve this issue see the TimeIndexedPartOf pattern.

## Scenarios

- The turbine is a proper part of the engine, both are parts of a car. Furthermore, the engine and the battery are proper parts of the car.

## Related Patterns

- **PartOf** — transitive part-of (this pattern is a specialization of PartOf)
- **TimeIndexedPartOf** — part-of with temporal indexing
- **Constituency** — constituents of a layered structure

## Additional Information

- **Specialization Of:** PartOf
- **Has Components:** (none)
- This pattern also includes the elements of the PartOf pattern.

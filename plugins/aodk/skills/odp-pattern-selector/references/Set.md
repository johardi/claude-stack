# Set

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Set
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/set.owl
**Extracted From:** http://swan.mindinformatics.org/ontologies/1.2/collections.owl

## Intent

To model sets of things (elements). A Set is a collection that cannot contain duplicate elements.

## Competency Questions

- What is the cardinality (size) of this set?
- What are the elements in this set?

## Domains

- General
- Parts and Collections

## Solution Description

A Set is a collection that cannot contain duplicate elements. A Set is expressed by linking to it directly all the members (elements). Multiple identical values of members (elements) will be eliminated because by default they are treated as a set. Unlike the Bag pattern, Set links directly to member resources without an intermediary Item class.

## Elements

### Classes

- **Set** (owl:Class) — A collection that cannot contain duplicate elements.

### Object Properties

None locally (inherits `hasMember` / `isMemberOf` from CollectionEntity).

### Data Properties

- **size** (owl:DatatypeProperty) — The number of items belonging to a collection.

## Consequences

The Set pattern provides a simple way to model collections where each element appears at most once. Because members are linked directly (without the Item indirection used in Bag), OWL's set semantics naturally prevents duplicates. The size property allows tracking cardinality.

## Scenarios

- The set of EU member states.
- A set of unique keywords associated with a document.

## Related Patterns

- **CollectionEntity** — basic collection/membership (Set has this as a component)
- **Bag** — collection with duplicates
- **List** — ordered collection with duplicates

## Additional Information

- **Specialization Of:** (none)
- **Has Components:** CollectionEntity
- **Reengineered From:** http://swan.mindinformatics.org/ontologies/1.2/collections.owl
- The collections ontology (part of the SWAN ontologies) was created by Paolo Ciccarese (Massachusetts General Hospital/Harvard Medical School) and Marco Ocana (Balboa Systems Inc.). Available under a Creative Commons License.

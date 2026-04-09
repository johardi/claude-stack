# List

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:List
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/list.owl
**Extracted From:** http://swan.mindinformatics.org/ontologies/1.2/collections.owl

## Intent

To represent ordered collections, i.e. lists.

## Competency Questions

- What are the items (elements) in this list?
- What is the length (size) of this list?
- What is the first/last item in this list?
- What resource does this list item contain?
- What is the next/previous item in the list?

## Domains

- General
- Parts and Collections

## Solution Description

Representing ordered lists through a specialization of the Bag pattern, where each resource in the bag is referred through an item, so that the same item can occur in several places. The usual properties of lists are also present: the sequence of elements, and references to the first and last item.

## Elements

### Classes

- **List** (owl:Class) — An ordered array of items, that can be present in multiple copies.
- **ListItem** (owl:Class) — Element belonging to a list.

### Object Properties

- **hasFirstItem** (owl:FunctionalProperty) — The link to the first item of the list.
- **firstItemOf** (owl:ObjectProperty) — Inverse of hasFirstItem.
- **hasLastItem** (owl:FunctionalProperty) — The link to the last item of the list.
- **lastItemOf** (owl:ObjectProperty) — Inverse of hasLastItem.
- **nextItem** (owl:FunctionalProperty) — The link to the next item in a list (ordered collection).
- **previousItem** (owl:FunctionalProperty) — The link to the previous item in a list (ordered collection).

### Data Properties

None locally (inherits `size` from Bag).

## Consequences

The List pattern enables representation of ordered sequences with navigation (next/previous) and boundary access (first/last). Items can contain duplicate resources since it inherits from Bag. The functional nature of nextItem, previousItem, hasFirstItem, and hasLastItem enforces the linear structure of a list.

## Scenarios

- An ordered bibliography where the sequence of references matters.
- A playlist of songs in a specific order.

## Related Patterns

- **Bag** — unordered collection with duplicates (List specializes Bag)
- **Set** — unordered collection without duplicates
- **CollectionEntity** — basic collection/membership (List has this as a component)
- **Sequence** — ordering pattern (List has this as a component)

## Additional Information

- **Specialization Of:** Sequence, Bag
- **Has Components:** Sequence, CollectionEntity
- **Reengineered From:** http://swan.mindinformatics.org/ontologies/1.2/collections.owl
- The collections ontology (part of the SWAN ontologies) was created by Paolo Ciccarese (Massachusetts General Hospital/Harvard Medical School) and Marco Ocana (Balboa Systems Inc.). Available under a Creative Commons License.

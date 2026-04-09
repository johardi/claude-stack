# Bag

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Bag
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/bag.owl
**Extracted From:** http://swan.mindinformatics.org/ontologies/1.2/collections.owl

## Intent

To model bags of items (elements). The Bag is characterized by a collection that can have multiple copies of each object.

## Competency Questions

- What bag is this item an element of?
- What is the size of this bag?
- What resource does this item refer to?
- What are the items contained in this bag?

## Domains

- General
- Parts and Collections

## Solution Description

The Bag is characterized by a collection that can have multiple copies of each object. This is performed through the Item entity. The Item links exactly one resource through the relationship itemContent. This indirection through Item allows the same resource to appear multiple times in a Bag (each occurrence is a distinct Item).

## Elements

### Classes

- **Bag** (owl:Class) — Collection that can have a number of copies of each object.
- **Item** (owl:Class) — Element belonging to a Bag.

### Object Properties

- **hasItem** (owl:ObjectProperty) — The link to every item of the Bag.
- **itemOf** (owl:ObjectProperty) — The link from an item to the Bag where it is contained.
- **itemContent** (owl:ObjectProperty) — The link to the actual resource to which the item refers.

### Data Properties

- **size** (owl:DatatypeProperty) — The number of items belonging to a collection.

## Consequences

The Bag pattern allows modeling multisets (collections with duplicates). The indirection through the Item class means two Items can reference the same resource, enabling duplicate tracking. Each Item links to exactly one resource via itemContent.

## Scenarios

- A shopping cart containing two copies of the same book — each copy is a distinct Item referencing the same Book resource.

## Related Patterns

- **CollectionEntity** — basic collection/membership (Bag has this as a component)
- **List** — ordered collection with duplicates (specializes Bag)
- **Set** — collection without duplicates

## Additional Information

- **Specialization Of:** (none)
- **Has Components:** CollectionEntity
- **Reengineered From:** http://swan.mindinformatics.org/ontologies/1.2/collections.owl
- The collections ontology (part of the SWAN ontologies) was created by Paolo Ciccarese (Massachusetts General Hospital/Harvard Medical School) and Marco Ocana (Balboa Systems Inc.). Available under a Creative Commons License.

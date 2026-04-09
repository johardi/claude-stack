# Collection Entity

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:CollectionEntity
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/collectionentity.owl
**Also Known As:** collections, membership
**Extracted From:** http://www.ontologydesignpatterns.org/ont/dul/DUL.owl

## Intent

To represent collections, and their entities, i.e. to represent membership.

## Competency Questions

- Which collection is this entity a member of?
- Which are the members of this collection?

## Domains

- Parts and Collections

## Solution Description

This pattern is a basic one: it captures the idea of a collection and its members. It reifies sets into the domain of discourse through the class Collection, and relates collections to their member entities via the hasMember / isMemberOf properties.

## Elements

### Classes

- **Collection** (owl:Class) — Any container for entities that share one or more common properties. E.g. "stone objects", "the nurses", "the Louvre Aegyptian collection". A collection is not a logical class: a collection is a first-order entity, while a class is a second-order one.
- **Entity** (owl:Class) — Anything: real, possible, or imaginary, which some modeller wants to talk about for some purpose.

### Object Properties

- **hasMember** (owl:ObjectProperty) — A relation between collections and entities, e.g. "my collection of saxophones includes an old Adolphe Sax original alto" (i.e. my collection has member an Adolphe Sax alto).
- **isMemberOf** (owl:ObjectProperty) — The inverse of hasMember.

### Data Properties

None.

## Consequences

It is possible to put sets in the domain of discourse through the class Collection, which reifies them. For temporary membership, the TimeIndexedMembership pattern should be used.

## Scenarios

- The Louvre Aegyptian collection.
- Aldo, Alfio, and Valentina are members of the STLab.

## Related Patterns

- **Bag** — collection with duplicates (specializes CollectionEntity)
- **Set** — collection without duplicates (specializes CollectionEntity)
- **List** — ordered collection (specializes CollectionEntity)
- **PartOf** — part-of is distinct from membership

## Additional Information

- **Specialization Of:** (none)
- **Has Components:** (none)
- **Examples (OWL):** http://www.ontologydesignpatterns.org/cp/examples/collectionentity/ISTC.owl

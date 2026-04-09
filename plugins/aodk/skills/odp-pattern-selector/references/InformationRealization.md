# Information Realization

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Information_realization
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/informationrealization.owl

## Intent

To represent information objects and their physical realization.

## Competency Questions

- What are the physical realizations of this information object?
- What information objects are realized by this physical object?

## Domains

- Semiotics

## Solution Description

This is a basic pattern representing the difference between abstract and realized (manifested, concrete, etc.) information. It allows distinguishing information objects from their concrete realizations.

## Elements

### Classes

- **InformationObject** — An abstract piece of information, such as a musical composition, a text, a word, a picture, independently from how it is concretely realized.
- **InformationRealization** — A physical realization (manifestation) of an information object, e.g. a particular printed copy of a book.

### Object Properties

- **realizes** — Relates a physical object to the information object it realizes.
- **isRealizedBy** — Inverse of realizes; relates an information object to its physical realization.

## Consequences

This pattern allows distinguishing information objects from their concrete realizations. For example, the abstract work "Divina Commedia" vs. a specific printed book of it.

## Scenarios

- The book of the "Divina Commedia" — the abstract literary work (InformationObject) vs. a physical copy of the book (InformationRealization).

## Related Patterns

- **IntensionExtension** — Addresses meaning of information objects.
- **InformationObjectsAndRepresentationLanguages** — Deals with representation of information in formal/natural languages.

## Additional Information

- Submitted by: Valentina Presutti
- Extracted from: http://www.ontologydesignpatterns.org/ont/dul/ontologies/DUL.owl
- Example OWL file: http://www.ontologydesignpatterns.org/cp/examples/informationrealization/IMeMine.owl

# InformationObjectsAndRepresentationLanguages

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:InformationObjectsAndRepresentationLanguages
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/informationobjectsandrepresentationlanguages.owl

## Intent

To represent information objects expressed in different representation languages (natural, formal, iconic), and the relations between information objects and the languages they are expressed in.

## Competency Questions

Not explicitly listed. Implied questions include:
- In what language is this information object expressed?
- What information objects are expressed in this formal language?
- What does this formal expression formally represent?

## Domains

- General
- Semiotics

## Solution Description

The pattern defines a taxonomy of languages (natural, formal, iconic) and corresponding information objects (linguistic objects, formal expressions, iconic objects). It provides properties for relating information objects to concepts they express and to the representation languages they use.

## Elements

### Classes

- **Language** — A natural or artificial language, provided with an alphabet (or vocabulary) and combinatorial rules.
- **NaturalLanguage** — A natural language, evolved and used in a community across time. Components are "temporary" and "reconstructed" out of actual usage.
- **FormalLanguage** — A formal language, created by some human, with a fixed grammar, and usually with an explicit formal semantics.
- **IconicLanguage** — A language made up of graphical elements. It can be natural, artificial, and even formal.
- **LinguisticObject** — An information object represented in a NaturalLanguage.
- **FormalExpression** — Any information object represented in a FormalLanguage, usually having a formal interpretation by a FormalEntity, and used to formally represent any Entity.
- **IconicObject** — An information object represented in an IconicLanguage.

### Object Properties

- **conceptualizes** — A relation stating that an Agent is internally representing a SocialObject. E.g., "John believes in the conspiracy theory."
- **isConceptualizedBy** — Inverse of conceptualizes.
- **formallyRepresents** — The relation between formal expressions and anything that they are supposed to represent. E.g., "the predicate 'MariachiInTijuana' formallyRepresents the Collection of all mariachis in Tijuana."
- **isFormallyRepresentedIn** — Inverse of formallyRepresents.
- **hasRepresentationLanguage** — Links an information object to its representation language.
- **isRepresentationLanguageOf** — Inverse of hasRepresentationLanguage.

## Consequences

Enables distinguishing between different types of representation languages and their corresponding information objects, supporting reasoning about how information is encoded and what it formally represents.

## Scenarios

No explicit scenarios provided.

## Related Patterns

- **Information Realization** — Addresses physical realization of information objects.
- **IntensionExtension** — Addresses meaning (intension/extension) of information objects.

## Additional Information

- Submitted by: Aldo Gangemi
- Extracted from: DUL (DOLCE-Ultralite) ontology

# IntensionExtension

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:IntensionExtension
**OWL Building Block:** http://ontologydesignpatterns.org/cp/owl/intensionextension.owl

## Intent

To represent the meaning of an information object: the concepts it expresses, the things it is about.

## Competency Questions

- What is the meaning of an information object?
- What information objects express this meaning?
- What is this about?
- How can I call this?

## Domains

- General
- Semiotics

## Solution Description

This pattern employs a simple set of properties to link information objects to their meanings, and to entities they can be about. It implements a minimal version of the semiotic triangle, distinguishing between:

1. **Intensional meaning** — the concepts, descriptions, or social objects expressed by information objects:
   - Relational meaning (frame semantics): expresses relation between InformationObject and Description
   - Conceptual meaning (concept schemes): expresses relation between InformationObject and Concept
   - Paraphrase meaning (lexicographic): expresses relation between InformationObject and another InformationObject
   - Cultural meaning (social science): expresses relation between InformationObject and SocialObject

2. **Extensional meaning** — the entities or sets of entities an information object can be about:
   - Object-level formal meaning (first-order logic): expresses relation between InformationObject and Collection
   - Modal formal meaning (possible-world): InformationObject related to Collections in PossibleWorlds

## Elements

### Classes

- **InformationObject** — A piece of information, such as a musical composition, a text, a word, a picture, independently from how it is concretely realized.
- **SocialObject** — Any Object that exists within some communication Event, in which at least one PhysicalObject participates. Includes InformationObjects, SocialAgents, Places, Situations, Collections, Descriptions, and Concepts.

### Object Properties

- **expresses** — The relation between an InformationObject and a "meaning" (e.g., a Concept, Description, SocialObject). E.g., "the term Beehive expresses the Concept Beehive"; "the text of Italian Constitution expresses the 'content' of the Constitution."
- **isExpressedBy** — Inverse of expresses.
- **isAbout** — A relation between information objects and any Entity. E.g., "the proper noun 'Leonardo da Vinci' isAbout the Person Leonardo da Vinci"; "the common noun 'person' isAbout the set of all persons."
- **isReferenceOf** — Inverse of isAbout; relates entities to information objects that refer to them.

## Consequences

We are able to distinguish between the intension of the meaning of an information object (its social object, e.g. a concept), and its extension (the entities or sets of entities it can be about). In practice, this pattern allows encoding a minimal version of the semiotic triangle, useful in all cases where the domain needs to represent words, concepts, and things in the same ontology. SKOS has an overlap with this pattern.

## Scenarios

- "Leonardo da Vinci" is the name of the main Rome airport.
- "Legal Person" means an incorporated entity with legal status.

## Related Patterns

- **Information Realization** — Physical realization of information objects.
- **LMM** — Lexical Model for Meaning.
- **Tagging** — Uses information objects as tags.
- **Topic** — Relates things to their topics/subjects.

## Additional Information

- Submitted by: Aldo Gangemi
- Extracted from: http://ontologydesignpatterns.org/ont/dul/DUL.owl (DOLCE-UltraLite)
- The intension and extension pattern allows representation of the intensional expression and extensional reference of information objects.

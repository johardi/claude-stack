# Topic

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Topic
**OWL Building Block:** http://ontologydesignpatterns.org/cp/owl/topic.owl

## Intent

To represent topics and their relations.

## Competency Questions

- What is the topic of something?
- What topics are included in this one?
- What are the topics near to that one?

## Domains

- General

## Solution Description

Topics are modelled as conceptual complexes with part-of (containment), overlap, and vicinity relations, and can be related to any kind of entity. They are disjoint from "Concepts", which can be at the "core" of topics.

There is an interesting duality of topics: they are commonly interpreted as areas of shared knowledge within a Community (therefore as collections of social objects). On the other hand, existing directories and thesauri use "topic" (or "subject") more restrictively, as a relation between a document and a concept. In this pattern, Concept and Topic are disjoint.

## Elements

### Classes

- **Topic** — A topic, subject, argument, domain, theme, or subject area. Topics have a controversial intuition: they are commonly interpreted as areas of shared knowledge (extensional notion), which is different from concepts (intensional notion). E.g., "the football topic is part of the sport topic" vs. "the concept of football is part of the concept of sport" — the first is acceptable, the second is counterintuitive.
- **Concept** — A social object used to classify entities. Differently from Topic, concepts typically have an "is a" relation to entities. E.g., "A biography of Brigitte Bardot hasTopic 'star system' (Topic)" vs. "A biography of Brigitte Bardot is a Biography (Concept)."

### Object Properties

- **hasTopic** — The relation between something and its Topic (subject, argument, domain, theme, etc.). Very general; e.g., "A biography of Brigitte Bardot hasTopic 'star system'."
- **isTopicOf** — Inverse of hasTopic.
- **hasSubTopic** — The relation between two Topics, in terms of cultural coverage. E.g., "Sport hasSubTopic Football."
- **isSubTopicOf** — Inverse of hasSubTopic.
- **hasCoreConcept** — A Concept is a core concept for a Topic when it can classify many entities that have that Topic. E.g., "Saxophone (Concept) isCoreConceptFor Saxophones (Topic)."
- **isCoreConceptFor** — Inverse of hasCoreConcept.
- **nearTopicTo** — Vicinity relation between two topics, typically established by threshold on shared concepts/entities. E.g., "'star system' is nearTopicTo 'cinema'."
- **farTopicFrom** — Opposite of vicinity between two topics. E.g., "'star system' is farTopicFrom 'geology'."
- **overlappingTopic** — Overlap relation between two topics. E.g., "'star system' overlappingTopic 'Bollywood movies'."

## Consequences

We are able to represent topics, subjects, or themes of something, and to organize topics into partonomic and topological structures. For more sophisticated relations between topics, concepts, terms, etc., refer to the full ontopic.owl ontology.

## Scenarios

- "The topic of Moby Dick is the hatred of humanity."
- "What are the main subjects in newspapers today? And more specifically?"

## Related Patterns

- **Tagging** — Uses tags related to topics.
- **IntensionExtension** — Related through concept/meaning relationships.

## Additional Information

- Submitted by: Sara Bernardini, Aldo Gangemi
- Extracted from: http://www.ontologydesignpatterns.org/ont/dul/ontopic.owl
- Simplified version of the full ontopic.owl ontology.
- Note on SKOS mapping: skos:Concept should be mapped to the union of Concept and Topic.

# Description

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Description
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/description.owl

## Intent

To formally represent a conceptualization or a descriptive context.

## Competency Questions

- Which are the assumptions under which a certain thing is described?
- Which are the concepts involved in the description of a certain thing?
- What is the interpretation of this case/event/observation?

## Domains

- General

## Solution Description

A Description represents a conceptualization. It can be thought also as a descriptive context that defines concepts in order to see a relational context out of a set of data or observations. For example, a Plan is a description of some actions to be executed by agents in a certain way, with certain parameters; a Diagnosis is a description that provides an interpretation to a set of observed entities, etc.

## Elements

### Classes

- **Description** — Represents a conceptualization. It can be thought as a descriptive context that defines concepts in order to see a relational context out of a set of data or observations. For example, a Plan is a description of some actions to be executed by agents in a certain way, with certain parameters; a diagnosis is a description that provides an interpretation to a set of observed entities.
- **Concept** — An idea, notion, role, or even a reified class, defined in a Description. Once defined, a concept can be used in other descriptions.

### Object Properties

- **defines** — A relation between a Description and a Concept, e.g. a Workflow for a governmental Organization defines the Role 'officer', or 'the Italian Traffic Law defines the role Vehicle'. Inverse of isDefinedIn.
- **isDefinedIn** — A relation between a Description and a Concept, e.g. a workflow for a governmental organization defines the role officer. In order to be used, a concept must be previously defined in another description. Inverse of defines.
- **usesConcept** — A generic relation holding between a Description and a Concept. In order to be used, a Concept must be previously defined in another Description. Inverse of isConceptUsedIn.
- **isConceptUsedIn** — A more generic relation holding between a description and a concept. Inverse of usesConcept.

## Consequences

This CP allows the designer to represent both a (descriptive) context and the elements that characterize and are involved in that context.

## Scenarios

(No specific scenarios provided.)

## Related Patterns

- Situation
- DescriptionAndSituation

## Additional Information

Extracted from: http://www.loa-cnr.it/ontologies/DUL.owl. Submitted by Valentina Presutti.

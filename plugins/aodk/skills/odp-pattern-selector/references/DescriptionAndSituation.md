# Description and Situation

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:DescriptionAndSituation
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/descriptionandsituation.owl

## Intent

To represent conceptualizations (descriptions) and their corresponding groundings (situations), linking the descriptive/normative level with the factual level.

## Competency Questions

- What situations satisfy a certain description?
- What descriptions can be (partly) satisfied by that situation?
- What situations (partly) satisfying a certain description can emerge out of this dataset?

## Domains

- General

## Solution Description

The Description and Situation content ontology design pattern represents conceptualizations (i.e., descriptions) and corresponding groundings (i.e., situations). A Description gives a unity to a Collection of parts (the components), or constituents, by assigning a Role to each of them in the context of a whole Object (the system). A same Entity can be given different descriptions. The pattern links descriptions to situations through the satisfies/isSatisfiedBy properties. The pattern is extracted from DOLCE+DnS Ultralite by partial cloning of elements, and is composed of three other CPs: Description, Situation, and Classification.

## Elements

### Classes

(Inherits classes from Description, Situation, and Classification patterns.)

### Object Properties

- **describes** — The relation between a Description and an Entity: a Description gives a unity to a Collection of parts (the components), or constituents, by assigning a Role to each of them in the context of a whole Object (the system). A same Entity can be given different descriptions.
- **isDescribedBy** — The relation between any Thing and a Description. Inverse of describes.
- **isSatisfiedBy** — A relation between a Situation and a Description, e.g. the execution of a Plan satisfies that plan. Inverse of satisfies.
- **satisfies** — A relation between a Situation and a Description, e.g. the execution of a Plan satisfies that plan. Inverse of isSatisfiedBy.

## Consequences

This pattern enables linking conceptualizations (normative, descriptive frameworks) with their factual groundings (observed situations), allowing reasoning about which situations satisfy which descriptions.

## Scenarios

(No specific scenarios provided.)

## Related Patterns

- Description (has component)
- Classification (has component)
- Situation (has component)

## Additional Information

Extracted from: http://www.ontologydesignpatterns.org/ont/dul/DUL.owl. Submitted by Aldo Gangemi.

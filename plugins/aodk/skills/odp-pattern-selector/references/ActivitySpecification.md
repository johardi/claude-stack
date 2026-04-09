# ActivitySpecification

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:ActivitySpecification
**OWL Building Block:** http://ontology.eil.utoronto.ca/icity/ActivitySpecification

## Intent

This work is concerned with supporting a correct and meaningful representation of activities on the Semantic Web, with the potential to support tasks such as activity recognition and reasoning about causation. This requires an ontology capable of more than simply documenting and annotating individual activity occurrences; definitions of activity specifications — including detailed preconditions and effects with respect to change over time — are required.

## Competency Questions

- What are the preconditions (effects) of a given activity?
- Is/are the precondition(s) true at some time t?
- Is/are the effect(s) true at some time t?
- If we observe some state, what activity may have caused it?

## Domains

- Event Processing
- General

## Solution Description

The proposed solution adopts a view of causality similar to the Event Calculus [Kowalski, 1986], employing the concept of manifestations to describe the states (fluents). This pattern leverages existing work (the Change of Time Varying Entities pattern) to define activity specifications that include preconditions and effects, with explicit consideration of change over time.

## Elements

### Classes

- **Activity** — An occurrence or action that can be specified with preconditions and effects.
- **ActivitySpecification** — The specification/definition of an activity including its preconditions and effects.
- **Manifestation** — A state (fluent) that describes the condition of entities at a point in time; used to express preconditions and effects.
- **Precondition** — A manifestation that must hold before an activity can occur.
- **Effect** — A manifestation that results from an activity occurring.

### Object Properties

- **hasPrecondition** — Relates an activity specification to its preconditions.
- **hasEffect** — Relates an activity specification to its effects.
- **manifestationOf** — Relates a manifestation to the entity it describes.

## Consequences

- (-) Requires a temporal representation of the domain — specifically using the Logical OP for change — which results in a larger, more complex representation.
- (+) However, given that the concepts are preconditions and effects of an activity, they should be subject to change and so the resulting representation is (though larger) more appropriate and accurate.

## Scenarios

- My car must have gas (a manifestation of a specific vehicle should have gas) before I can drive to work (the manifestation should exist at some time before the drive-to-work activity occurs).
- An effect of my driving to work is that I am at work and so is my car.

## Related Patterns

- **Change of Time Varying Entities** — Component pattern for representing change over time.
- **Situation** — Related pattern for representing states.

## Additional Information

- Submitted by: Megan Katsumi
- Also Known As: Activity Specification OP
- Known Uses: http://ontology.eil.utoronto.ca/icity/UrbanSystem
- Extracted From: http://ontology.eil.utoronto.ca/icity/Activity/1.1/
- Has Components: http://ontology.eil.utoronto.ca/icity/Change/

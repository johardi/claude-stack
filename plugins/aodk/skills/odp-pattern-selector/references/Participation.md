# Participation

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Participation
**OWL Building Block:** http://ontologydesignpatterns.org/cp/owl/participation.owl
**Extracted From:** http://ontologydesignpatterns.org/ont/dul/DUL.owl

## Intent

To represent participation of an object in an event.

## Competency Questions

- Which objects do participate in this event?
- Which events does this object participate in?

## Domains

- General

## Solution Description

This pattern is a basic one, and enables the representation of any simple binary relation between objects and events. It clones equivalent elements from DOLCE-UltraLite. Using cardinality restrictions appropriately allows limiting the number of participants — e.g. "life of" is a specialization of this pattern that requires a functional object property (cardinality 1..1).

## Elements

### Classes

- **Event** (owl:Class) — Any physical, social, or mental process, event, or state.
- **Object** (owl:Class) — Any physical, social, or mental object, or substance.

### Object Properties

- **hasParticipant** (owl:ObjectProperty) — Relates an Event to an Object that participates in it.
- **isParticipantIn** (owl:ObjectProperty) — Relates an Object to an Event it participates in. Inverse of hasParticipant.

### Data Properties

None.

## Consequences

It is possible to model whatever relation between objects and events. Using cardinality restrictions appropriately allows limiting the number of participants, e.g. "life of" is a specialization requiring a functional object property (cardinality 1..1). This is a non-temporal version of the participation relation. For a time-indexed relation, use the TimeIndexedParticipation pattern.

## Scenarios

- Aldo Gangemi participated in the premiere of La Dolce Vita.
- A catalyst participates in a chemical reaction.

## Related Patterns

- **TimeIndexedParticipation** — participation with temporal qualification
- **ParticipantRole** — participation with role qualification (specializes Participation)
- **AgentRole** — agents and their roles (complementary)
- **Situation** — general situation reification

## Additional Information

- **Specialization Of:** (none)
- **Has Components:** (none)
- The basic participation pattern, without temporal indexing. It clones equivalent elements from DOLCE-UltraLite.

# Participant Role

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:ParticipantRole
**OWL Building Block:** http://www.ontology.se/odp/content/owl/ParticipantRole.owl

## Intent

To represent participants in events holding specific roles in that particular event.

## Competency Questions

- What is the role of this object in this event?
- What is the object holding this role in this event?
- In what event did this object hold this role?

## Domains

- General
- Organization

## Solution Description

The pattern introduces a situation (ParticipantRole) that connects the object to its role in a particular event. It reifies the three-way relationship between an object, its role, and the event in which it holds that role. This avoids the need for n-ary properties and provides a clean way to query role-qualified participation.

## Elements

### Classes

- **Role** (owl:Class) — A concept that classifies an object.
- **ParticipantRole** (owl:Class) — A situation that represents the role(s) of a specific object (or objects) participating in an event (or events).

Additionally inherits from Participation:
- **Event** (owl:Class) — Any physical, social, or mental process, event, or state.
- **Object** (owl:Class) — Any physical, social, or mental object, or substance.

### Object Properties

- **objectParticipating** (owl:ObjectProperty) — Links the ParticipantRole situation to the participating Object.
- **roleOfParticipant** (owl:ObjectProperty) — Links the ParticipantRole situation to the Role held by the participant.
- **participatingInEvent** (owl:ObjectProperty) — Links the ParticipantRole situation to the Event.
- **objectIncludedIn** (owl:ObjectProperty) — Links an Object to a ParticipantRole situation it is included in.
- **roleIncludedIn** (owl:ObjectProperty) — Links a Role to a ParticipantRole situation it is included in.
- **eventIncludedIn** (owl:ObjectProperty) — Links an Event to a ParticipantRole situation it is included in.

### Data Properties

None.

## Consequences

This pattern does not take into account time aspects of the participation; for such aspects see the TimeIndexedParticipation pattern. The reification through the ParticipantRole situation class provides a clean way to represent and query the three-way relationship between object, role, and event.

## Scenarios

- John was elected the meeting secretary of today's board meeting.
- During the party we used the blue cup as a vase.

## Related Patterns

- **Participation** — basic object-event participation (ParticipantRole specializes this)
- **Situation** — general situation reification (ParticipantRole has this as a component)
- **ObjectRole** — general object-role pattern
- **AgentRole** — agent-specific role pattern
- **TimeIndexedParticipation** — participation with temporal qualification

## Additional Information

- **Specialization Of:** Participation
- **Has Components:** Situation, Participation

# Time Indexed Participation

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Time_indexed_participation
**OWL Building Block:** http://ontologydesignpatterns.org/cp/owl/timeindexedparticipation.owl

## Intent

To represent participants in events at some time. To represent participants in parts of events.

## Competency Questions

- When did something participate in some event?
- At what time did an event have some participant?

## Domains

- General

## Solution Description

This pattern uses the Situation pattern to add temporal information to participation of objects in events. It specializes the TimeIndexedSituation pattern and composes the Participation and Region patterns.

## Elements

### Classes

- **TimeIndexedParticipation** — A Situation that represents participation of Object(s) in Event(s) at some Time.

### Object Properties

- **includesEvent** — A relation between situations and events, e.g. 'this morning I've prepared my coffee and had my fingers burnt' (the preparation of my coffee this morning included a burning of my fingers).
- **includesObject** — A relation between situations and objects, e.g. 'this morning I've prepared my coffee and had my fingers burnt' (the preparation of my coffee this morning included me).
- **isEventIncludedIn** — Inverse of includesEvent.
- **isObjectIncludedIn** — Inverse of includesObject.

## Consequences

We can represent participation relations with time. This enables participations at different times as well as partial participations in events. However, this pattern focuses on participation of one entity in one event. If complex events need to be represented (with subevents, more participants and times, etc.), a partonomic structure must be introduced, e.g. by creating a new pattern that composes TimeIndexedParticipation with PartOf.

## Scenarios

- This morning I've prepared my coffee and had my fingers burnt.
- The football match lasted only ten minutes for Totti.

## Related Patterns

- Participation (has component)
- Region (has component)
- TimeIndexedSituation (specialization of)
- Time indexed person role

## Additional Information

A time-indexed pattern for participation. Submitted by Aldo Gangemi.

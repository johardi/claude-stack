# N-ary Participation

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Nary_Participation
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/naryparticipation.owl

## Intent

To represent events with their participants, time, space, etc.

## Competency Questions

- What are the participants in that event at this time?
- What events had what participants in that location?

## Domains

- General

## Solution Description

The N-ary Participation pattern reifies participation relations so that multiple participants, time intervals, and locations can be associated with a single event. It specializes the Situation pattern and composes the Participation and TimeInterval patterns.

## Elements

### Classes

- **NaryParticipation** — The reified class of n-ary participation relations, e.g. "prepare a coffee with coffee pot".

### Object Properties

- **participationIncludes** — The relation holding between an NaryParticipation and any Entity that is part of it.
- **isIncludedInParticipation** — The relation holding between any Entity and a NaryParticipation. Inverse of participationIncludes.

## Consequences

All sorts of relations denoting events with multiple participants, space-time indexing, etc. can be represented with this pattern. When objects participate at the event at different times or with different parts, more elementary nary-participation instances must be created, and made parts of the main one.

## Scenarios

- The match lasted 95 minutes, and the winner used a new nano-carbon racquet.

## Related Patterns

- Participation (has component)
- TimeInterval (has component)
- Situation (specialization of)
- Co-participation

## Additional Information

Extracted from: http://www.loa.cnr.it/ontologies/DUL.owl. Example OWL file: http://www.ontologydesignpatterns.org/cp/examples/naryparticipation/naryparticipationex.owl. Submitted by Aldo Gangemi.

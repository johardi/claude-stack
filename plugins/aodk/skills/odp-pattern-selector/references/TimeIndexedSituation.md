# Time Indexed Situation

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:TimeIndexedSituation
**OWL Building Block:** http://ontologydesignpatterns.org/cp/owl/timeindexedsituation.owl

## Intent

To represent time indexed situations.

## Competency Questions

- At what time did a certain situation occur?
- What situations occurred at a certain time?

## Domains

- General

## Solution Description

This pattern adds a time specification (the TimeInterval pattern) to the Situation pattern, in order to provide a handy solution to many cases where situations need temporal indexing.

## Elements

### Classes

- **TimeIndexedSituation** — A Situation that is explicitly indexed at some time for at least one entity.

### Object Properties

- **atTime** — Relates a TimeIndexedSituation to a TimeInterval, specifying when the situation holds.
- **forEntity** — Relates a TimeIndexedSituation to the entity it is about.
- **hasTimeIndexedSetting** — Relates an entity to a TimeIndexedSituation that provides a time-indexed setting for it.
- **isTimeIndexFor** — Relates a TimeInterval to a TimeIndexedSituation it indexes.

## Consequences

We can represent situations that have an explicit time parameter. In principle, this can be done already with the Situation pattern, but this provides a handy composition with the TimeInterval pattern.

## Scenarios

- Mustafa's address in 2005 was in Brussels.

## Related Patterns

- Situation (specialization of)
- TimeInterval (has component)
- Time indexed participation
- TimeIndexedClassification

## Additional Information

A generic pattern usable for all situations that require a temporal indexing.

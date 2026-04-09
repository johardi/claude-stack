# Recurrent Situation Series

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:RecurrentSituationSeries
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/recurrentsituationseries.owl

## Intent

To represent recurrent situation series as situations and collections of consecutive situations, with a regular time period between situations and unifying factors.

## Competency Questions

- What are the situations of a recurrent situation series?
- Which is the time period elapsing between two situations of a recurrent situation series?
- When is the next situation of a recurrent situation series scheduled?
- What are the unifying criteria shared by all the situations in a recurrent situation series?
- Which are the unifying situations shared by a (subset of) the situations member of a recurrent situation series?
- When is a unifying situation valid?
- Which is the (immediate) next situation in a recurrent situation series?
- Which is the (immediate) previous situation in a recurrent situation series?

## Domains

- General

## Solution Description

A recurrent situation series is modelled as an intersection of a collection and a situation. A recurrent situation series is seen as a collection, since it contains entities that share one or more common properties and are unified conceptually (unifying factors). These entities are members of the collection, and are all consecutive situations. At the same time, a recurrent situation series is a situation, intended as a relational context in which the contextualised things are based on a frame: a recurrent situation series is similar to a plan that defines how the things involved in that plan (i.e. the specific situations) shall be carried out, e.g. where the situations shall be located, in which time of the year, etc.

## Elements

### Classes

- **RecurrentSituationSeries** — Modelled as an intersection of Collection and Situation. Contains consecutive situations that share unifying factors and recur at regular time periods. Each situation has either a previous situation, a next situation, or both.
- **Situation** — Represents a situation that is a member of the series.
- **TimePeriod** — Represents a time period (e.g. 1 week) between consecutive situations.
- **UnifyingFactor** — A concept which classifies an element or property occurring in each situation member of a recurrent situation series, which unifies the collection.
- **UnifyingSituation** — A situation involving a unifying factor, valid at a specific time interval.

### Object Properties

- **hasEstimatedTimePeriod** — Relates a recurrent situation series to an estimated time period.
- **hasImmediateNextSituation** — Relates a situation member to the immediate next situation member in the series.
- **hasImmediatePreviousSituation** — Relates a situation member to the immediate previous situation member in the series.
- **hasMeasuredTimePeriod** — Relates a recurrent situation series to a measured time period.
- **hasMemberSituation** — Relates a recurrent situation series to a situation that is a member of it.
- **hasNextSituation** — Relates a situation member to a next situation member in the series.
- **hasPreviousSituation** — Relates a situation member to a previous situation member in the series.
- **hasTimePeriod** — Relates a recurrent situation series to a time period.
- **hasTimePeriodBeforeNextSituation** — Relates a situation member to the time period elapsing before its next situation.
- **hasUnifyingFactor** — Relates a collection to a unifying factor.
- **hasUnifyingSituation** — Relates a recurrent situation series to a unifying situation.
- **involvesUnifyingFactor** — Relates a unifying situation to the involved unifying factor.
- **isEstimatedTimePeriodOf** — Inverse of hasEstimatedTimePeriod.
- **isInvolvedInUnifyingSituation** — Relates a unifying factor to the unifying situation it is involved in.
- **isLocallyInconsistentWith** — Relates two entities that are considered locally inconsistent.
- **isMeasuredTimePeriodOf** — Inverse of hasMeasuredTimePeriod.
- **isSituationMemberOf** — Inverse of hasMemberSituation.
- **isTimePeriodBeforeNextSituationOf** — Inverse of hasTimePeriodBeforeNextSituation.
- **isTimePeriodOf** — Inverse of hasTimePeriod.
- **isUnifyingFactorOf** — Inverse of hasUnifyingFactor.
- **isUnifyingSituationOf** — Inverse of hasUnifyingSituation.
- **isValidIn** — Relates a unifying situation to its temporal validity.

### Data Properties

- **isTheLastSituation** — Defines if a situation member of a recurrent situation series is the last one or not.
- **situationNumber** — Represents the number of the situation in the recurrent situation series (the first situation, the second situation, etc.)

## Consequences

A series of recurrent situations, its unifying factors and the recurrent time period can be modeled.

## Scenarios

- Umbria Jazz is a collection of situations, which all take place in July and in the Italian region of Umbria, and has the musical genre jazz as a topic. Its situations recur at regular time periods, i.e. annually.

## Related Patterns

- Classification
- Collection
- Description
- Recurrent Event Series
- Sequence
- Situation

## Additional Information

This pattern is a new version of the Recurrent Event Series ODP, based on new analysis which led to terminological and modelling changes.

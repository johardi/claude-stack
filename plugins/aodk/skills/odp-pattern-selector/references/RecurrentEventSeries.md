# Recurrent Event Series

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:RecurrentEventSeries
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/recurrenteventseries.owl

## Intent

To represent recurrent event series as situations and collections of consecutive events, with a regular time period between events and unifying factors.

## Competency Questions

- What are the events of a recurrent event series?
- Which is the time period elapsing between two events of a recurrent event series?
- When is the next event of a recurrent event series scheduled?
- What are the unifying criteria shared by all the events in a recurrent event series?
- Which is the (immediate) next event in a recurrent event series?
- Which is the (immediate) previous event in a recurrent event series?

## Domains

- General / Events

## Solution Description

A recurrent event series is modelled as an intersection of a collection and a situation. A recurrent event is seen as a collection, since it contains entities that share one or more common properties and are unified conceptually (unifying factors). These entities are members of the collection, and are all consecutive events. At the same time, a recurrent event is a situation, intended as a relational context in which the contextualised things are based on a frame: a recurrent event is similar to a plan that defines how the things involved in that plan (i.e. the specific events) shall be carried out, e.g. where the events shall be located, in which time of the year, etc.

## Elements

### Classes

- **RecurrentEventSeries** — Modelled as an intersection of Collection and Situation. Contains consecutive events that share unifying factors and recur at regular time periods.

### Object Properties

(Inherits properties from Situation and Collection patterns.)

## Consequences

A series of recurrent events, its unifying factors and the recurrent time period can be modelled.

## Scenarios

- Umbria Jazz is a collection of events, which all take place in July and in the Italian region of Umbria, and has the musical genre jazz as a topic. Its events recur at regular time periods, i.e. annually.

## Related Patterns

- Situation
- Sequence
- Classification
- CollectionEntity

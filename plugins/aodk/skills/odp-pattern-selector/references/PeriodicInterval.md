# Periodic Interval

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:PeriodicInterval
**OWL Building Block:** http://delicias.dia.fi.upm.es/ontologies/PeriodicInterval.owl

## Intent

The goal of this pattern is to represent non-convex intervals where the duration of each internal interval and the duration of the gaps between intervals are constant. These intervals are called periodic intervals within the context of this pattern.

## Competency Questions

- What is the period of the interval 'every tuesday of 2010'? The period is a week (weekly).

## Domains

- Time

## Solution Description

The class "Interval" defined in the OWL-Time ontology has been extended within this pattern by means of the class "PeriodicInterval". This concept has been created in order to define periodic intervals. These intervals are defined by four elements, namely, its beginning, its end, the duration of each subinterval and the duration of the period, that is, the gaps between two subintervals. In order to model the beginning and end of the interval, the relationships "hasBeginning" and "hasEnd" already defined in the OWL-Time ontology are reused. The durations of the subintervals and the period between them have been modelled by means of the relationships "hasIntervalDurationPerPeriod" and "hasPeriod" respectively. Both relationships are defined between the concepts "PeriodicInterval" and "DurationDescription".

## Elements

### Classes

- **PeriodicInterval** — A subclass of Interval representing non-convex intervals with constant subinterval duration and constant gap duration between subintervals.

### Object Properties

- **hasIntervalDurationPerPeriod** — Relates a PeriodicInterval to a DurationDescription representing the duration of each subinterval within the period.
- **hasPeriod** — Relates a PeriodicInterval to a DurationDescription representing the duration of the gap (period) between two consecutive subintervals.

## Consequences

This content pattern allows designers to represent non-convex intervals where the period between subintervals, that is, the gaps between subintervals, and the duration of the subintervals are constant.

## Scenarios

- Sam teaches every monday.

## Related Patterns

- Extends the OWL-Time ontology (http://www.w3.org/TR/owl-time).

## Additional Information

This ontology design pattern extends the OWL-Time ontology defining periodic intervals. Submitted by Maria Poveda and Mari Carmen Suarez-Figueroa (WOP:2012). Known use: http://www.oeg-upm.net/index.php/en/ontologies/82-mio-ontologies

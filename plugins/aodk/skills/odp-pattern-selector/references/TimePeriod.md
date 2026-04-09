# TimePeriod

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:TimePeriod
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/timeperiod.owl

## Intent

To represent time periods between events.

## Competency Questions

- Which is the measurement unit of a time period?
- Which is the value of a time period?

## Domains

- Time

## Solution Description

A time period is modeled as an n-ary relation with a measurement unit and a numerical value. This allows representing durations (amounts of elapsed time) between events, independently of specific calendar dates. The pattern captures both the magnitude and the unit of time.

## Elements

### Classes

The pattern defines classes for representing time periods as structured values. Based on the solution description, the expected elements include:

- **TimePeriod** — A duration of time characterized by a measurement unit and a numerical value. Represents the elapsed time between events or the duration of a process.
- **MeasurementUnit** — The unit in which the time period is measured (e.g., seconds, minutes, hours, days, months, years).

### Object Properties

- Properties relating TimePeriod to its measurement unit and to the events it separates (specific property names follow the n-ary relation pattern).

### Data Properties

- A numerical value property for the magnitude of the time period.

## Consequences

The measurement unit and the numerical value of a time period (e.g., 1 year) can be modeled. This allows expressing durations without requiring specific calendar dates, making it suitable for recurring intervals, expected durations, and relative temporal relationships.

## Scenarios

- A time period of 1 year elapses between two consecutive editions of Umbria Jazz Festival.
- A manufacturing process has a curing time period of 24 hours.
- The incubation period of a disease is a time period of 5 to 14 days.

## Related Patterns

- **TimeInterval** — Represents specific date-bounded intervals (start/end dates), while TimePeriod represents durations (amounts of time). They are complementary: TimeInterval for "when" and TimePeriod for "how long."
- **Sequence** — For ordering events that are separated by time periods.

## Additional Information

- Submitted by: Valentina Anita Carriero
- Certified pattern
- The pattern uses an n-ary relation approach to cleanly separate the numerical value from the measurement unit of a time period.

# TimeInterval

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:TimeInterval
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/timeinterval.owl

## Intent

To represent time intervals.

## Competency Questions

- What is the end time of this interval?
- What is the starting time of this interval?
- What is the date of this time interval?

## Domains

- Time

## Solution Description

The TimeInterval pattern provides a simple class for representing time intervals with associated start and end dates as datatype values. It is designed to be composed with other Content OPs when temporal aspects need to be represented. The dates of the time interval are datatype values (not domain entities); if reasoning about dates is needed, this pattern should be composed with the Region Content OP.

## Elements

### Classes

- **TimeInterval** — Any region in a dimensional space that represents time.

### Object Properties

None.

### Data Properties

- **hasIntervalDate** (owl:DatatypeProperty) — A datatype property that encodes values from xsd:date for a time interval. A same time interval can have more than one xsd:date value: begin date, end date, date at which the interval holds, as well as dates expressed in different formats: xsd:gYear, xsd:dateTime, etc.
- **hasIntervalStartDate** (owl:DatatypeProperty) — The start date of a TimeInterval. Subproperty of hasIntervalDate.
- **hasIntervalEndDate** (owl:DatatypeProperty) — The end date of a TimeInterval. Subproperty of hasIntervalDate.

## Consequences

The dates of the time interval are not part of the domain of discourse — they are datatype values. If there is the need of reasoning about dates, this Content OP should be used in composition with the Region Content OP.

## Scenarios

- The time interval "January 2008" starts at 2008-01-01 and ends at 2008-01-31.

## Related Patterns

- **Region** — Compose with TimeInterval when reasoning about dates as domain entities is needed.
- **Sequence** — For ordering time intervals.
- **Action** — Uses TimeInterval for representing action durations and suspension periods.
- **Transition** — Uses time intervals for positioning initial states, final states, and events.
- **TimePeriod** — Represents durations (amounts of time) between events, complementing TimeInterval which represents specific date-bounded intervals.

## Additional Information

- Submitted by: Valentina Presutti
- Certified pattern
- This Content OP can be composed with other Content OPs when temporal aspects need to be represented.
- Example OWL file: http://www.ontologydesignpatterns.org/cp/examples/timeinterval/january2008.owl

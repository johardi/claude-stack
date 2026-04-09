# Sequence

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Sequence
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/sequence.owl

## Intent

To represent sequence schemas. It defines the notion of transitive and intransitive precedence and their inverses. It can then be used between tasks, processes, time intervals, spatially located objects, situations, etc.

## Competency Questions

- What is before what?
- What's next?
- What's immediately following this?

## Domains

- General
- Organization
- Workflow
- Time

## Solution Description

This pattern is a basic one; it represents the 'path' cognitive schema, which underlies many different conceptualizations: spatial paths, time lines, event sequences, organizational hierarchies, graph paths, etc. The Sequence pattern reuses the logical pattern Transitive Reduction in order to represent both transitive and non-transitive (direct) precedence relations.

## Elements

### Classes

No locally defined classes. The pattern is domain-agnostic and provides only the ordering properties. Any class can participate in a sequence.

### Object Properties

- **precedes** (owl:TransitiveProperty) — A transitive relation between entities, expressing a 'sequence' schema. E.g. "year 1999 precedes 2000", "deciding what coffee to use precedes preparing coffee", "in the Milan to Rome autoroute, Bologna precedes Florence." Can be used between tasks, processes, time intervals, spatially located objects, situations, etc. Subproperties can be defined for different uses.
- **follows** (owl:TransitiveProperty) — Inverse of precedes. A transitive relation expressing sequence. E.g. "year 2000 follows 1999", "preparing coffee follows deciding what coffee to use."
- **directlyPrecedes** — The intransitive precedes relation. E.g. "Monday directly precedes Tuesday." Directness of precedence depends on the designer's conceptualization.
- **directlyFollows** — The intransitive follows relation. Inverse of directlyPrecedes. E.g. "Wednesday directly follows Tuesday."

### Data Properties

None.

## Consequences

We can represent and reason over transitive or intransitive sequences of any kind. However, since coreference cannot be expressed in OWL, it is not possible to represent and reason over loops and other sequences involving coreference.

## Scenarios

- Year 1999 precedes year 2000.
- Monday directly precedes Tuesday.
- In a workflow, "gather requirements" precedes "design system" which precedes "implement code."
- On the Milan-to-Rome autoroute, Bologna precedes Florence.

## Related Patterns

- **Transitive Reduction** (logical pattern) — Reused to distinguish transitive from intransitive precedence.
- **Action** — Uses Sequence as a component for ordering actions.
- **Transition** — Uses Sequence for temporal ordering of states and events.
- **TimeInterval** — Sequence can order time intervals.

## Additional Information

- Submitted by: Aldo Gangemi
- Certified pattern
- Extracted from: DUL (DOLCE+DnS Ultralite) ontology — http://www.ontologydesignpatterns.org/ont/dul/DUL.owl
- This is one of the most fundamental and widely-reused content ontology design patterns, serving as a building block for many other patterns.

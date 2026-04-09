# Transition

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Transition
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/transition.owl

## Intent

To represent basic knowledge about transitions (events, states, processes, objects).

## Competency Questions

- What states of some object are changed by what event during a transition?
- What is the process that is invariant through the transition?
- What transitions are occurring on what object at what time?

## Domains

- General
- Workflow
- Manufacturing

## Solution Description

This pattern composes the Time-indexed Participation, Region, and Sequence patterns in order to represent changing of states for objects, fired by some event, through an underlying process. It can represent part of the semantics involved in transitions (e.g. what is implied by Petri Nets): initial and final states, causal events, underlying processes, affected objects, and sequences of time intervals for situations and events.

However, it is not possible to define axioms for automatically inferring initial and final states from time sequences, because coreference is not allowed in OWL (not even in OWL2).

## Elements

### Classes

- **Transition** — The entity that is invariant across the Process underlying the transition, but is also changed from an initial to a final state by an Event. A transition is a Situation that creates a context for three TimeIntervals, two additional different Situations, one Event, one Process, and at least one Object: the Event is observed as the cause for the transition, one Situation is the state before the transition, the second Situation is the state after the transition, the Process is the invariance under some different transitions, in which at least one Object is situated. This class partly encodes the ontology underlying typical engineering algebras for processes, e.g. Petri Nets.
- **Process** — The invariance under some different transitions (including the one represented here), in which at least one Object is situated.

### Object Properties

- **includesInitialSituation** — Relates a transition situation to the situation existing before the transition event.
- **isInitialSituationIncludedIn** — Inverse of includesInitialSituation.
- **includesFinalSituation** — Relates a transition situation to the situation resulting from the transition.
- **isFinalSituationIncludedIn** — Inverse of includesFinalSituation.
- **includesProcess** — Relates a transition situation to the underlying process that is invariant for the object(s) included in the transition.
- **isProcessIncludedIn** — Inverse of includesProcess.
- **hasInitialStateAtTime** — The time of the initial state in the transition.
- **hasFinalStateAtTime** — The time of the final state of the transition.
- **hasEventAtTime** — The time of the event causing the transition.
- **occursAt** — General temporal occurrence relation.
- **isTimeOf** — Inverse of occursAt.

### Data Properties

None.

## Consequences

The pattern enables representing state transitions caused by events within an underlying process, with temporal positioning. It captures initial and final states, the causal event, the invariant process, and the affected objects. However, a full representation of the transition ontology is outside the expressivity of OWL, because it would need qualified cardinality restrictions, coreference, property equivalence, and property composition. Loops and other sequences involving coreference cannot be represented.

## Scenarios

- The addition of Bud Powell on piano made the tune jump from a static, aerial comping into a hard driving swing improvisation.
- A chemical reaction transitions a substance from liquid state to gas state, caused by the event of heating, within the underlying process of phase change.

## Related Patterns

- **Time indexed participation** (component) — Provides time-indexed participation of objects in situations.
- **Region** (component) — Provides regions for state description.
- **Sequence** (component) — Provides temporal ordering of situations and events.
- **Move** — For spatial transitions specifically (change of location).

## Additional Information

- Submitted by: Aldo Gangemi
- Certified pattern
- A simple pattern to represent transitions between states.
- OWL expressivity limitations: cannot automatically infer initial/final states from time sequences due to OWL's lack of coreference support.

# Observation

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Observation
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/observation.owl

## Intent

To represent observations of things, under a set of parameters. Common parameters may be the time and place of the observation, but may be any feature that is observed concerning the specific thing being observed.

## Competency Questions

- What objects have been observed?
- What are the observations of this object?
- What are the parameters under which this object was observed?
- What objects were observed under this parameter?

## Domains

- General
- Science

## Solution Description

The pattern introduces an Observation class that links observed objects to the parameters of their observation. It is a specialization of the Situation pattern.

## Elements

### Classes

- **Observation** — A specific situation where some thing is observed with respect to a set of parameters.
- **Parameter** — The parameters of an observation describe the context and content of the observation. For example, in a medical context an observation of a patient may contain a set of symptoms, that are the parameters of that observation.

### Object Properties

- **hasObservation** — Relates an observed thing to its observations.
- **isObservationOf** — Inverse of hasObservation; relates an observation to the thing observed.
- **hasParameter** — Relates an observation to its parameters.
- **isParameterOf** — Inverse of hasParameter.

### Data Properties

- **inDate** — Records the date of an observation.

## Consequences

We are able to represent the parameters of observations made, enabling queries about what was observed, when, and under what conditions.

## Scenarios

- The aquatic species "Skipjack tuna" was observed in 2004 having the exploitation state "fully exploited" in the climatic zone "tropical" at the vertical distance "pelagic."

## Related Patterns

- **Situation** — Parent pattern; Observation is a specialization of Situation.
- **EEP (Execution-Executor-Procedure)** — More elaborate observation/actuation pattern for sensor networks.

## Additional Information

- Submitted by: Eva Blomqvist
- Version: 1.0
- Imports: http://www.ontologydesignpatterns.org/cp/owl/situation.owl

# BasicPlan

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:BasicPlan
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/basicplan.owl

## Intent

To represent plan descriptions, their components (tasks, goals, parameters), and the relationship between plans and their executions.

## Competency Questions

- What tasks compose this plan?
- What goal does this plan aim to achieve?
- Which agent conceptualizes this plan?
- What situation satisfies this plan?
- What parameters constrain this plan?

## Domains

- General
- Workflow
- Organization

## Solution Description

The BasicPlan content ontology design pattern represents plan descriptions and their executions. It is defined by combining and expanding other CPs: basic plan description, basic plan execution, and object role. Expansion involves the partial clone of ontology elements from DOLCE Ultra Lite and Plans Lite ontologies.

## Elements

### Classes

- **GoalSituation** — A goal situation is a situation that satisfies a goal. Opposite to the case of subplan executions, a goal situation is not part of a plan execution. This helps to account for: (a) Execution of plans containing abort or suspension conditions (the plan would be satisfied even if the goal has not been reached), (b) Incidental satisfaction, like when a situation satisfies a goal without being intentionally planned (but anyway desired).

### Object Properties

- **conceptualizes** — A relation stating that an Agent is internally representing a SocialObject. E.g., "John believes in the conspiracy theory"; "the task force members share the attack plan."
- **isConceptualizedBy** — Inverse of conceptualizes. A relation stating that an Agent is internally representing a Description.
- **executesTask** — A relation between an action and a task, e.g. "putting some water in a pot and putting the pot on a fire until the water starts bubbling" executes the task "boiling."
- **isExecutedIn** — Inverse of executesTask.
- **satisfies** — A relation between a Situation and a Description, e.g. the execution of a Plan satisfies that plan.
- **isSatisfiedBy** — Inverse of satisfies.
- **parametrizes** — The relation between a Parameter, e.g. 'MajorAgeLimit', and a Region, e.g. '18_year'.
- **isParametrizedBy** — Inverse of parametrizes.

### Data Properties

None.

## Consequences

The pattern enables representation of plans as descriptions that can be satisfied by situations (plan executions). It supports goal modeling, task decomposition within plans, parameterization, and the conceptualization relationship between agents and plans. However, it does not directly address temporal ordering of tasks within a plan (for that, see the Sequence or Controlflow patterns).

## Scenarios

- A cooking plan that includes the tasks "fill pot with water," "add ingredients," and "heat until boiling," conceptualized by a chef, and satisfied by the actual cooking execution.
- A project plan with goals, tasks, and parameters, where the goal situation may be achieved incidentally or through planned execution.

## Related Patterns

- **BasicPlanExecution** — Represents the execution (situation) side of plans.
- **Situation** — The general pattern for situations that satisfy descriptions.
- **ObjectRole** — Used as a component for role modeling.
- **TaskExecution** — Related pattern for task-action relationships.

## Additional Information

- Submitted by: Aldo Gangemi
- Certified pattern
- Extracted from: DOLCE Ultra Lite and Plans Lite ontologies (http://www.loa-cnr.it/ontologies/PlansLite.owl)

# BasicPlanExecution

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:BasicPlanExecution
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/basicplanexecution.owl

## Intent

To represent the execution of a plan and the entities that participate in such an execution, including actions, agents, objects, and regions involved.

## Competency Questions

- What actions are included in this plan execution?
- Which agents participate in a plan execution?
- What objects are involved in the execution of a plan?
- Does this situation satisfy a given plan?

## Domains

- General
- Workflow
- Organization

## Solution Description

The BasicPlanExecution content ontology design pattern represents the execution of a plan and the entities that participate in such an execution. This CP is the composition of other CPs: Situation and Region. Furthermore, it expands such CPs with ontology elements that are partial clones of elements from the DOLCE Ultra Lite and the Plans Lite ontologies.

## Elements

### Classes

- **Action** — An Event with at least one Agent that isParticipantIn it, and that executes a Task that typically isDefinedIn a Plan, Workflow, Project, etc.
- **PlanExecution** — Plan executions are situations that proactively satisfy a plan. Subplan executions are proper parts of the whole plan execution.

### Object Properties

- **actionHasParticipant** — A relation between a Process and an Object, e.g. "the avalanche hasParticipant a mass of snow", or "the cooking of a cake hasParticipant an agent, some sugar, flour, etc."
- **isParticipantInAction** — Inverse of actionHasParticipant.
- **includesAction** — A relation between situations and actions, e.g. "this morning I've prepared my coffee and had my fingers burnt" (the preparation included a burning of my fingers).
- **isActionIncludedIn** — Inverse of includesAction.
- **includesAgent** — A relation between situations and agents, e.g. "this morning I've prepared my coffee" (the preparation included me).
- **isAgentIncludedIn** — Inverse of includesAgent.
- **includesObject** — A relation between situations and objects participating in the execution.
- **isObjectIncludedIn** — Inverse of includesObject.
- **includesRegion** — A relation between situations and regions (parameter values, spatial regions, etc.).
- **isRegionIncludedIn** — Inverse of includesRegion.

### Data Properties

None.

## Consequences

The pattern allows representing plan executions as situations that bind together actions, agents, objects, and regions. It connects the execution (situation) with the plan (description) via the satisfies/isSatisfiedBy properties inherited from the Situation pattern. Subplan executions can be modeled as proper parts of a larger plan execution.

## Scenarios

- A cooking plan execution where the agent (chef) performs the actions (chopping, boiling) with objects (vegetables, pot) in a kitchen.
- A project execution that includes multiple sub-plan executions carried out by different team members.

## Related Patterns

- **BasicPlan** — The description side of plan modeling (this pattern handles the execution side).
- **Situation** — The general pattern for reified situations.
- **Region** — Used for representing parameter values and spatial/temporal regions in executions.
- **Participation** — The general participation pattern.

## Additional Information

- Submitted by: Aldo Gangemi
- Certified pattern
- Extracted from: DOLCE Ultra Lite and Plans Lite ontologies

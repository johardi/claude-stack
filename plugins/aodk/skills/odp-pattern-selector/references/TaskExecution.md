# TaskExecution

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:TaskExecution
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/taskexecution.owl

## Intent

To represent actions through which tasks are executed.

## Competency Questions

- Which task is executed through this action?
- What actions can be done in order to execute that task?

## Domains

- Organization
- Management
- Scheduling
- Workflow

## Solution Description

The pattern models the relationship between actions (events performed by agents) and tasks (descriptions of what should be done). An action executes a task, and a task is defined within a plan, workflow, or project context. The pattern imports and composes the TaskRole, Participation, and AgentRole component patterns.

## Elements

### Classes

- **Action** — An Event with at least one Agent that isParticipantIn it, and that executes a Task that typically isDefinedIn a Plan, Workflow, Project, etc.

### Object Properties

- **executesTask** — A relation between an action and a task, e.g. "putting some water in a pot and putting the pot on a fire until the water starts bubbling" executes the task "boiling."
- **isExecutedIn** — Inverse of executesTask. Relates a task to the action(s) that execute it.

### Data Properties

None.

## Consequences

This CP allows designers to make assertions on roles played by agents without involving the agents that play those roles, and vice versa. It allows to express neither the context type in which tasks are defined, nor the particular context in which the action is carried out. Moreover, it does not allow to express the time at which the task is executed through the action (for actions that do not solely execute that certain task).

## Scenarios

- She smiled at us, so obtaining the effect of making us feeling positive.
- A nurse administers medication (action) that executes the task "administer prescribed drugs."

## Related Patterns

- **TaskRole** (imported) — Allows expressing the dependence between tasks and roles.
- **Participation** (imported) — General participation pattern for agents in events.
- **AgentRole** (imported/related) — Relates agents to roles they play.
- **NaryClassification** — Can be specialized to create a temporally-indexed version of TaskExecution.
- **BasicPlan** — Provides the plan context in which tasks are defined.

## Additional Information

- Submitted by: Aldo Gangemi
- Certified pattern
- Created by: Aldo Gangemi
- Imports: taskrole.owl, participation.owl, agentrole.owl
- Extracted from: DUL (DOLCE+DnS Ultralite) ontology

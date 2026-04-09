# Controlflow

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Controlflow
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/controlflow.owl

## Intent

To represent control flows: activation, branching, decisions, concurrency, etc.

## Competency Questions

- What is the control structure of this plan or workflow?
- What tasks branch from a decision point?
- Which tasks can be executed concurrently?
- What is the loop condition for a repeated task?
- What tasks must synchronize before proceeding?

## Domains

- Workflow
- Business process modeling
- Planning

## Solution Description

The Controlflow pattern provides a rich taxonomy of control tasks that structure the execution flow of plans and workflows. It reifies control constructs as task classes, enabling representation of procedural knowledge within the ontology. This allows coordination tasks to be modeled explicitly (e.g., a manager coordinating the execution of several related activities).

## Elements

### Classes

- **ControlTask** — A task executed during a planning activity aimed at anticipating other activities. Control tasks usually have at least one direct successor task (the controlled one), except for ending tasks. The reification of control constructs enables representing procedural knowledge alongside controlled actions.
- **ActionTask** — An elementary task that sequences non-planning activities like moving, exercising forces, gathering information, etc. Planning activities are mental events involving some rational event.
- **ActivationTask** — A control task aimed at starting an activity. Specialized by beginning tasks or reactivation tasks.
- **BranchingTask** — A task that articulates the plan into an ordered set of tasks.
- **CaseTask** — A control task branched to a set of tasks that are not executable concurrently. Requires preliminary deliberation tasks to choose which task to undertake, possibly based on information-gathering and decision rationales.
- **BooleanCaseTask** — A yes-or-no case task requiring exactly two deliberation tasks.
- **ConcurrencyTask** — A task branched to a set of tasks executable concurrently (the sequenced perdurants can overlap). No deliberation task is performed to choose among them. Has at least one successor synchronization task.
- **DeliberationTask** — A control task executed in a deliberation state (a decision taken during a case task execution, e.g. a yes or no, or a known value).
- **DecisionActivity** — An activity related to planning. Executes a 'case task' and can contain an information gathering activity.
- **DeliberationState** — A state related to planning. Finalizes the execution of a 'deliberation task' and is preceded by a decision activity.
- **LoopTask** — A control task whose successor is an action (or complex) task that sequences at least two distinct activities sharing a minimal common set of properties. Supports exit conditions, iteration intervals, and iteration cardinality.
- **MergingTask** — A task that joins a set of tasks after a branching.
- **AbstractMergingTask** — A merging aimed at 'formally' joining tasks that are direct successors to a case task. Unlike synchronization tasks, abstract mergings only provide abstract boundaries because in a case task, only one action task is supposed to be executed.
- **SynchroTask** — A synchronization task aimed at waiting for the execution of all (except optional ones) tasks that are direct successors to a concurrent or any-order task.
- **EndingTask** — A control task that has no successor tasks defined in the plan.

### Object Properties

Properties are inherited from imported component patterns and the Plans Lite ontology. The pattern focuses on the class taxonomy of control constructs rather than defining new properties.

### Data Properties

None.

## Consequences

The pattern provides a comprehensive vocabulary for workflow control structures. By reifying control constructs as classes, it enables: (1) representation of procedural knowledge within the same ontology as domain knowledge, (2) modeling of coordination responsibilities (e.g., a manager role responsible for a complex task), and (3) formal specification of branching, concurrency, synchronization, and looping patterns. Some axioms cannot be fully expressed in OWL-DL (e.g., value mappings for concurrency constraints).

## Scenarios

- A manufacturing workflow with sequential steps, a quality-check decision point (case task), and parallel assembly tasks (concurrency task) that must synchronize before packaging.
- A medical treatment plan with an activation task, a loop for repeated medication administration, and an ending task upon patient recovery.

## Related Patterns

- **Sequence** — Provides basic ordering; Controlflow extends this with richer control structures.
- **BasicPlan** — Plans whose control flow this pattern structures.
- **TaskExecution** — The execution of tasks referenced in control flows.
- **Action** — The Action pattern provides action lifecycle (proposed, implemented, abandoned) that complements control flow structures.

## Additional Information

- Submitted by: Aldo Gangemi
- Certified pattern
- Extracted from: Plans Lite ontology (http://www.loa-cnr.it/ontologies/PlansLite.owl)
- Some OWL-DL limitations: certain constraints (e.g., MinimalCommonType for LoopTask, value mappings for ConcurrencyTask) cannot be fully expressed in OWL-DL.

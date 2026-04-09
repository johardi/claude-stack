# Action

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Action
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/action.owl

## Intent

The purpose of the pattern is to model actions that are proposed, planned, and performed or abandoned, together with their status and durations in time.

## Competency Questions

- What actions is this action dependent on?
- When was this action started?
- What are the actions contained in this plan?
- What are the consequences of this action?
- What is the status of this action?
- When was this action completed?
- What is the suspension time of this action?

## Domains

- Product development
- Business
- General

## Solution Description

This pattern models an action class, and subclasses that represent different kinds of actions depending on their properties. It also includes properties of actions such as status and duration. The pattern imports the Sequence and TimeInterval patterns as components.

## Elements

### Classes

- **Action** — The process of doing something. An action is performed by an agent. An action can be proposed (proposed actions make up a plan), implemented or abandoned, and it has a status and possibly one or more suspension periods. Actions can have consequences and can be dependent on other actions, e.g. the action of pouring water from a cup is dependent on the action to first fill the cup with water.
- **Action_status** — The different values the status of an action can take. A possible set of status values could be {proposed, ongoing, completed, abandoned}.
- **Implemented_action** — An implemented action is an action that has been started.
- **Proposed_action** — A proposed action is an action that is in some plan, whether the plan is accepted or shared between agents or not. Proposed actions can be abandoned or implemented.
- **Completed_action** — A completed action is an implemented action that has also been finalized.
- **Abandoned_action** — An abandoned action is an action which is no longer going to be performed, regardless if it was previously just proposed or actually partly implemented. An abandoned action could be seen as an action that is permanently suspended.
- **Plan** — A set of proposed actions and the sequence in which to perform them.
- **Suspension** — The time interval within which an action is (temporarily or permanently) suspended.
- **Performance_duration** — The time interval within which an action is performed.

### Object Properties

- **has_status** — Relates an action instance to its current status. Example: "I finished making coffee."
- **is_status_of** — Inverse of has_status. Relates a status to instances of actions.
- **has_consequence** (owl:TransitiveProperty) — A causal relation between actions. Example: "swimming" is a consequence of "jumping into deep water." Transitive.
- **is_consequence_of** (owl:TransitiveProperty) — Inverse of has_consequence. Transitive.
- **has_direct_consequence** — An intransitive subproperty of has_consequence for representing direct consequences.
- **is_direct_consequence_of** — Inverse of has_direct_consequence. Intransitive.
- **is_dependent_on** (owl:TransitiveProperty) — Represents non-causal dependencies between actions. Example: "swimming" is dependent on "getting into the water." Transitive.
- **has_dependent** (owl:TransitiveProperty) — Inverse of is_dependent_on. Transitive.
- **is_directly_dependent_on** — Intransitive version of the dependency property for direct dependency relations.
- **has_direct_dependent** — Inverse of is_directly_dependent_on. Intransitive.
- **has_duration** — Relates implemented actions to their duration (a possibly open-ended time interval).
- **is_duration_of** — Inverse of has_duration.
- **has_suspension** — Relates an action instance to periods of suspension.
- **is_suspension_of** — Inverse of has_suspension.
- **plan_composed_of** — Relates a plan to the proposed actions it contains.
- **action_proposed_in** — Inverse of plan_composed_of. Relates a proposed action to its plan(s).

### Data Properties

None.

## Consequences

The pattern allows representing different types of actions, e.g. implemented actions or suspended actions, but does not enforce any rules such as "if an action is an instance of the class of completed actions it has to have the status 'completed'."

## Scenarios

- The action of making coffee is dependent on the action of buying coffee.
- The action of making coffee is 'completed'.
- The consequence of making coffee is drinking coffee.
- I performed the action of making coffee between 9 and 9:05am this morning.
- I plan to make coffee tomorrow, and then I plan to have breakfast.

## Related Patterns

- **Sequence** — Used as a component for ordering actions within plans.
- **TimeInterval** — Used as a component for representing durations and suspension periods.

## Additional Information

- Submitted by: Eva Blomqvist
- Certified pattern
- The Action pattern uses a data model pattern approach ('action' data model pattern).

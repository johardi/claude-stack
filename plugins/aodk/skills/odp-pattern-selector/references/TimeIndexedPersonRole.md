# Time Indexed Person Role

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Time_indexed_person_role
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/timeindexedpersonrole.owl

## Intent

To represent classification of things at a certain time. Specifically, to represent the time-indexed relationship between persons and the roles they play.

## Competency Questions

- What role does a person play at a given time?
- During which time period did a person hold a certain role?
- Who played a specific role during a particular time interval?

## Domains

- General
- Business
- Organization

## Solution Description

This pattern is encoded by specializing the Situation pattern and composing it with the Agent Role pattern. It reifies the relationship between a person and a role into a situation (TimeIndexedPersonRole) that can be qualified with a time interval, allowing temporal indexing of role assignments.

## Elements

### Classes

- **Person** — Persons in commonsense intuition, i.e. either as physical agents (humans) or social persons.
- **TimeIndexedPersonRole** — A situation that expresses time indexing for the relation between persons and roles they play. This is the core reification class that binds a person, a role, and a time interval together.

### Object Properties

Properties are inherited from the imported component patterns (AgentRole, Classification, NaryClassification, ObjectRole). The pattern itself does not define new object properties locally but relies on the composition of:
- Agent role assignment properties (from agentrole.owl)
- Classification properties (from classification.owl)
- N-ary classification properties (from naryclassification.owl)
- Object role properties (from objectrole.owl)

### Data Properties

None.

## Consequences

The pattern enables representing temporal roles for persons without the monotonicity issues of modeling roles as disjoint subclasses of Person. A person can hold multiple roles simultaneously or sequentially, and each role assignment is independently time-stamped. However, the pattern is specific to persons and roles — for more general time-indexed classifications, the underlying N-ary Classification or Situation patterns should be used directly.

## Scenarios

- John was the CEO of Acme Corp from 2010 to 2015.
- Mary held the role of project manager during Q1 2024.
- A person transitions from trainee to senior engineer over time.

## Related Patterns

- **AgentRole** (imported) — Provides the agent-role relationship that this pattern extends with temporal indexing.
- **Classification** (imported) — Provides the general classification structure.
- **NaryClassification** (imported) — Provides n-ary classification for reifying multi-argument relations.
- **ObjectRole** (imported) — Provides the object-role relationship.
- **Situation** — The parent pattern that TimeIndexedPersonRole specializes.

## Additional Information

- Submitted by: Aldo Gangemi
- Certified pattern
- Created with TopBraid Composer
- Imports: agentrole.owl, classification.owl, naryclassification.owl, objectrole.owl, cpannotationschema.owl

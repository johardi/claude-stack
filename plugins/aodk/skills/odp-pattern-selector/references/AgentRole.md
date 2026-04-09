# Agent Role

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:AgentRole
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/agentrole.owl
**Extracted From:** http://www.loa-cnr.it/ontologies/DUL.owl

## Intent

To represent agents and the roles they play.

## Competency Questions

- Which agent does play this role?
- What is the role that is played by that agent?

## Domains

- Management
- Organization
- Scheduling

## Solution Description

This pattern specializes the ObjectRole pattern by restricting the object to an Agent. It allows assertions on roles played by agents without involving the agents that play those roles, and vice versa. Roles are reified as first-order entities.

## Elements

### Classes

- **Agent** (owl:Class) — Any agentive Object, either physical or social.

### Object Properties

Inherits from ObjectRole:
- **hasRole** (owl:ObjectProperty) — A relation between an Object and a Role, e.g. the person "John" has role "student".
- **isRoleOf** (owl:ObjectProperty) — Inverse of hasRole.

### Data Properties

None.

## Consequences

This pattern allows designers to make assertions on roles played by agents without involving the agents that play those roles, and vice versa. It does not allow expressing temporariness of roles. For temporal roles, use the TimeIndexedPersonRole pattern or specialize the N-ary Classification pattern.

## Scenarios

- She greeted us all in her various roles of mother, friend, and daughter.
- Aldo Gangemi is a senior researcher. He is also a father and a saxophonist.

## Related Patterns

- **ObjectRole** — general object-role pattern (AgentRole specializes this)
- **TimeIndexedPersonRole** — roles with temporal indexing
- **N-ary Participation** — can be specialized for temporal role qualification
- **ParticipantRole** — roles in the context of event participation
- **ActingFor** — agent acting on behalf of a social agent

## Additional Information

- **Specialization Of:** ObjectRole
- **Has Components:** (none)
- **Examples (OWL):** http://www.ontologydesignpatterns.org/cp/examples/agentrole/ex1.owl
- The elements of this pattern are added with the elements of its components and/or the elements of the Content OPs it is a specialization of.

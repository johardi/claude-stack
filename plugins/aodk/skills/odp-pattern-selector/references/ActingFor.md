# Acting For

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:ActingFor
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/actingfor.owl
**Reengineered From:** http://www.ontologydesignpatterns.org/ont/dul/DUL.owl

## Intent

To represent that some agent is acting in order to forward the action of a social (non-physical) agent.

## Competency Questions

- Who is working for which organization?
- Who is representing the company?

## Domains

- Organization
- Agency

## Solution Description

This pattern captures the delegation relationship between agents: a physical agent (e.g. a person) acts on behalf of a social agent (e.g. a corporation, an institution). The dependency can be "delegated" — e.g. a university can be acted for by a department, which in turn is acted for by physical agents.

## Elements

### Classes

- **Agent** (owl:Class) — Any agentive Object, either physical (e.g. a whale, a robot, an oak) or social (e.g. a corporation, an institution, a community). A computational agent can be considered as a PhysicalAgent that realizes a certain class of algorithms.
- **SocialAgent** (owl:Class) — Any individual whose existence is granted simply by its social communicability and capability of action (through some PhysicalAgent).

### Object Properties

- **actsFor** (owl:ObjectProperty) — The relation holding between any Agent and a SocialAgent. In principle, a SocialAgent requires at least one PhysicalAgent in order to act, but this dependency can be "delegated"; e.g. a university can be acted for by a department, which in turn is acted for by physical agents.
- **actsThrough** (owl:ObjectProperty) — The relation holding between a SocialAgent and an Agent (inverse direction). A SocialAgent acts through some Agent.

### Data Properties

None.

## Consequences

An ontology designer is able to express relations like delegation, working for, etc. It is not possible to express either time indexing (the Situation pattern should be specialized to that purpose), nor the role or task under which the social action is carried out by the physical agent (the DescriptionAndSituation pattern should be used instead).

## Scenarios

- Matteo Sanvitale is working as an officer for CEMA s.r.l.
- A department acts for a university.

## Related Patterns

- **AgentRole** — agents and their roles (complementary: ActingFor captures delegation, AgentRole captures role-playing)
- **Situation** — for temporal qualification of acting-for relations
- **DescriptionAndSituation** — for capturing the role/task under which the action is carried out

## Additional Information

- **Specialization Of:** (none)
- **Has Components:** (none)

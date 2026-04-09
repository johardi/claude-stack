# Object Role

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Objectrole
**OWL Building Block:** http://ontologydesignpatterns.org/cp/owl/objectrole.owl
**Extracted From:** http://www.loa-cnr.it/ontologies/DUL.owl

## Intent

To represent objects and the roles they play.

## Competency Questions

- What role does this object play?
- Which objects do play that role?

## Domains

- General

## Solution Description

This pattern reifies roles as first-order entities. Instances of Role classify Objects, allowing meta-level concepts (roles) to be placed in the ordinary domain of an ontology. An Object is related to a Role through the hasRole / isRoleOf properties. This is the general pattern; AgentRole specializes it for agents specifically.

## Elements

### Classes

- **Object** (owl:Class) — Any physical, social, or mental object, or a substance.
- **Role** (owl:Class) — A Concept that classifies an Object.

### Object Properties

- **hasRole** (owl:ObjectProperty) — A relation between an Object and a Role, e.g. the person "John" has role "student". isRoleOf is its inverse.
- **isRoleOf** (owl:ObjectProperty) — A relation between a Role and an Object, e.g. the "student" is the role of "John". hasRole is its inverse.

### Data Properties

None.

## Consequences

It is possible to make assertions about roles, which are typically considered at the meta-level of an ontology. Instances of Role reify such elements, which are therefore put in the ordinary domain of an ontology. It is not possible to parametrize the classification over different dimensions e.g., time, space, etc. For temporal parametrization, see TimeIndexedPersonRole or N-ary Classification patterns.

## Scenarios

- This old glass is used as a flower pot.
- A person plays the role of "project coordinator" in a research project.

## Related Patterns

- **AgentRole** — specialization for agents (restricts Object to Agent)
- **Classification** — general classification pattern (ObjectRole specializes this)
- **ParticipantRole** — roles in event participation contexts
- **TimeIndexedPersonRole** — temporal role assignments

## Additional Information

- **Specialization Of:** Classification
- **Has Components:** (none)
- The elements of this pattern are added with the elements of its components and/or the elements of the Content OPs it is a specialization of.

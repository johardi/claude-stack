# Object with States

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Object_with_states
**OWL Building Block:** http://delicias.dia.fi.upm.es/ontologies/ObjectWithStates.owl

## Intent

An object can have different states for which different restrictions apply. The goal of the pattern is to allow modelling the different states of an object and the restrictions on such object for its different states.

## Competency Questions

- Objects must have a unique state.
- Object states must belong to a single collection of non-duplicate elements (i.e., to a set).
- What are the possible states (e.g., StateA, StateB, StateC)?
- An object can have three different states.
- Objects in StateA must have at least one value for property1.
- Objects in StateB must have at most one value for property2.
- Objects in StateC must have exactly one value for property3.

## Domains

- General

## Solution Description

The pattern contains three classes: one for representing objects, another for representing object states, and a third for representing sets of states. It uses object properties for relating objects and states (subproperties of those defined in the Situation pattern) and for relating states and sets of states (reused from the CollectionEntity pattern), plus a datatype property for defining the size of a set of states (reused from the Set pattern).

To apply the pattern:
1. Create all possible states as instances of the State class using the Value Partition pattern.
2. Define different classes to represent the object in each state.
3. Apply state-specific restrictions to those classes.
4. Define the object class as a disjoint union of these state-specific classes.

## Elements

### Classes

- **Object** — Objects are entities that have different states and that in each state different restrictions on their properties apply.
- **State** — States are the different states that an object can have. States must belong to a single collection of non-duplicate elements (i.e., to a set).
- **StateSet** — State sets are sets of states (i.e., collections of non-duplicate states).

### Object Properties

- **hasState** — Defines the state of an object.
- **isStateOf** — Inverse; defines the object that has a state.

## Consequences

The pattern requires modelling states as individuals instead of as literals.

## Scenarios

A software defect created in an issue tracker must have a creator and be associated to a certain software product. Once it is checked that the defect is reproducible, it must be assigned to some developer and have a certain priority. However, before checking the defect reproducibility, the defect must not have either assignee or priority.

## Related Patterns

- **Situation** — Parent pattern (Object with States is a specialization).
- **CollectionEntity** — Used for relating states to state sets.
- **Set** — Used for defining the size of state sets.
- **Value Partition** (W3C) — Used for creating states as individuals.

## Additional Information

- Submitted by: Raul Garcia-Castro
- Known Uses: http://delicias.dia.fi.upm.es/ontologies/alm-istack.owl
- Submitted to: WOP 2013

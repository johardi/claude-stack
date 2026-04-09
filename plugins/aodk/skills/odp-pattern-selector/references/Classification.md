# Classification

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Classification
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/classification.owl

## Intent

To represent the relations between concepts (roles, tasks, parameters) and entities (persons, events, values), which concepts can be assigned to. To formalize the application (e.g. tagging) of informal knowledge organization systems such as lexica, thesauri, subject directories, folksonomies, etc., where concepts are first-order elements.

## Competency Questions

- What concept is assigned to this entity?
- Which category does this entity belong to?

## Domains

- General

## Solution Description

The Classification pattern provides a basic mechanism to relate Concepts to Entities. Instances of Concept reify meta-level elements (categories, types, roles), which are therefore put in the ordinary domain of an ontology. It is not possible to parametrize the classification over different dimensions (e.g., time, space) with this pattern alone — for that, see TimeIndexedClassification.

## Elements

### Classes

- **Concept** — A Social Object. The classifies relation relates concepts to entities at some time.
- **Entity** — Anything: real, possible, or imaginary, which some modeller wants to talk about for some purpose.

### Object Properties

- **classifies** — A relation between a Concept and an Entity, e.g. the Role 'student' classifies a Person 'John'.
- **isClassifiedBy** — A relation between an Entity and a Concept, e.g. 'John is considered a typical rude man'; your last concert constitutes the achievement of a lifetime; '20-year-old means she's mature enough'. Inverse of classifies.

## Consequences

It is possible to make assertions about e.g., categories, types, roles, which are typically considered at the meta-level of an ontology. Instances of Concept reify such elements, which are therefore put in the ordinary domain of an ontology. It is not possible to parametrize the classification over different dimensions e.g., time, space, etc.

## Scenarios

- Mac OSX 10.5 is classified as an operating system in the Fujitsu-Siemens product catalog.

## Related Patterns

- Description
- DescriptionAndSituation
- TimeIndexedClassification

## Additional Information

Extracted from: http://www.loa-cnr.it/ontologies/DUL.owl. Submitted by Valentina Presutti.

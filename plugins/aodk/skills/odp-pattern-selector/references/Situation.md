# Situation

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Situation
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/situation.owl

## Intent

To represent contexts or situations, and the things that are contextualized.

## Competency Questions

- What is the context or situation of something?
- What are the things present in this context or situation?

## Domains

- General

## Solution Description

The Situation pattern provides a way to contextualize things that have something in common, or are associated: a same place, time, view, causal link, systemic dependence, etc. It can also reify n-ary relations as situations.

A Situation is a view on a set of entities. It can be seen as a 'relational context', reifying a relation. For example, a PlanExecution is a context including some actions executed by agents according to certain parameters and expected tasks to be achieved from a Plan; a DiagnosedSituation is a context of observed entities that is interpreted on the basis of a Diagnosis, etc.

## Elements

### Classes

- **Situation** — A view on a set of entities. It can be seen as a 'relational context', reifying a relation. Situation is also able to represent reified n-ary relations, where isSettingFor is the top-level relation for all binary projections of the n-ary relation. If used in a transformation pattern for n-ary relations, the designer should take care of: (1) creating only one situation for each instance of an n-ary relation, otherwise the 'identification constraint' could be violated; (2) adding an 'exact cardinality' restriction corresponding to the arity of the n-ary relation, otherwise the designer would actually represent a polymorphic relation.

### Object Properties

- **hasSetting** — A relation between entities and situations, e.g. 'this morning I've prepared my coffee with a new fantastic Arabica' (i.e.: (an amount of) a new fantastic Arabica hasSetting the preparation of my coffee this morning).
- **isSettingFor** — Inverse of hasSetting. A relation between a situation and the entities it contextualizes.

## Consequences

We can contextualize things that have something in common, or are associated: a same place, time, view, causal link, systemic dependence, etc. We can also reify n-ary relations as situations.

## Scenarios

- The lecture was held in January 1921 by Bela Fleck, with some physicians in the audience making questions, in a very relaxed atmosphere.
- I prepared a coffee with my heater, 300 ml of water, and an Arabica coffee mix.

## Related Patterns

- Description
- DescriptionAndSituation

## Additional Information

Created by Aldo Gangemi and Valentina Presutti. Extracted from: http://www.ontologydesignpatterns.org/ont/dul/DUL.owl. Imports: http://www.ontologydesignpatterns.org/schemas/cpannotationschema.owl

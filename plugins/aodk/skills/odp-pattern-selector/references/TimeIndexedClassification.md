# Time Indexed Classification

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:TimeIndexedClassification
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/timeindexedclassification.owl

## Intent

To represent classification ('counting as') of an entity at some time.

## Competency Questions

- At what time was a certain entity classified as a certain concept?
- What classifications held at a certain time?

## Domains

- General

## Solution Description

This pattern specializes the TimeIndexedSituation pattern to the specific case of classification (counting as). It imports both the CountingAs pattern and the TimeIndexedSituation pattern, combining temporal indexing with classification. A TimeIndexedClassification is a Situation that represents classification of an entity at some time.

## Elements

### Classes

- **TimeIndexedClassification** — A Situation to represent classification ('counting as') of an entity at some time.

### Object Properties

(Inherits properties from TimeIndexedSituation and CountingAs patterns.)

## Consequences

We can represent classifications that are explicitly time-indexed, allowing the same entity to be classified differently at different times.

## Scenarios

- A building is classified as a historical monument from 1995 onwards.

## Related Patterns

- TimeIndexedSituation (specialization of)
- CountingAs (imports)
- Situation

## Additional Information

- Version 0.1: Created by Aldo Gangemi
- Version 0.2: Revised with specialization from timeindexedsituation.owl
- Imports: http://www.ontologydesignpatterns.org/cp/owl/countingAs.owl
- Imports: http://www.ontologydesignpatterns.org/cp/owl/timeindexedsituation.owl

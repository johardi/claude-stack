# Place

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Place
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/place.owl

## Intent

To talk about places of things.

## Competency Questions

- Where is a certain thing located?
- What is located at this place?

## Domains

- General

## Solution Description

This is a basic pattern, useful to represent generic locations for anything, which becomes a place when it is assumed as a reference location. A Place is an 'approximate', relative location. For an 'absolute', abstract location, cf. the pattern spaceregion.owl.

## Elements

### Classes

- **Place** — A location, in a very generic sense: a political geographic entity (Roma, Lesotho), a location determined by the presence of other entities ('the area close to Roma'), pivot events or signs ('the area where the helicopter fell'), complements of other entities ('the area under the table'), as well as physical objects conceptualized as locations as their main identity criterion ('the territory of Italy'). Formally, a Place is defined by the fact of having something located in it; a Place is located in itself.

### Object Properties

- **hasLocation** — A generic, relative localization, holding between any entities. E.g. 'the cat is on the mat', 'Omar is in Samarcanda', 'the wound is close to the femural artery'. For 'absolute' locations, see SpaceRegion.
- **isLocationOf** — A generic, relative localization, holding between any entities. E.g. 'Rome is the seat of the Pope', 'the liver is the location of the tumor'. Assumed as transitive. Inverse of hasLocation. For 'absolute' locations, see SpaceRegion.

## Consequences

We can represent, transitively, where something is located. It remains unspecified what kind of location relation we are trying to represent: reference location, partial location, physical location, social or metaphoric location, etc. Moreover, temporal location is not caught with this pattern (you need a placement situation for that).

## Scenarios

- The Colosseum is located in Rome.

## Related Patterns

- SpaceRegion (for absolute locations)

## Additional Information

Extracted from: http://www.ontologydesignpatterns.org/ont/dul/DUL.owl. Imports: http://www.ontologydesignpatterns.org/schemas/cpannotationschema.owl. Submitted by Aldo Gangemi.

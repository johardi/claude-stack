# Region

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Region
**OWL Building Block:** http://ontologydesignpatterns.org/cp/owl/region.owl

## Intent

To represent and reason on values of attributes of things, by explicitly talking about the dimensions ("regions") of the attributes, which include those values.

## Competency Questions

- What is the value for the attribute of that entity?
- Which entities have a certain value on that parameter/attribute/feature?

## Domains

- General

## Solution Description

This pattern is a basic one, which allows talking about attributes/parameters/dimensions, while still referring to their values. It creates a path from things to data values through "regions" representing attributes. Regions are portions of a dimensional space which can be used as a value for a quality of an Entity.

## Elements

### Classes

- **Region** — Any region in a dimensional space (a dimensional space is a maximal Region), which can be used as a value for a quality of an Entity. For example, TimeInterval, SpaceRegion, PhysicalAttribute, Amount, SocialAttribute are all subclasses of Region. Regions are not data values in the ordinary knowledge representation sense.

### Object Properties

- **hasRegion** — A relation between entities and regions. E.g., "the number of wheels of that truck is 12."
- **isRegionFor** — Inverse; a relation between regions and entities. E.g., "the color of my car is red."

### Data Properties

- **hasRegionDataValue** — A datatype property that encodes values for a Region. E.g., a float for the Region Height.

## Consequences

We can represent and reason on any kind of attributes, parameters, features, etc., which have a given set of values. With OWL2 support for custom and complex datatypes, this pattern should be confronted with possible enrichments, or may be restricted to OWL1. Since datatypes cannot overlap with classes even in OWL2, the pattern remains useful for cases where the domain must be kept homogeneous.

## Scenarios

No explicit scenarios provided. Typical usage includes representing measurable attributes (height, weight, color) as regions with associated data values.

## Related Patterns

- Part of the DOLCE-UltraLite (DUL) foundational ontology.

## Additional Information

- Submitted by: Aldo Gangemi
- Extracted from: http://www.ontologydesignpatterns.org/ont/dul/DUL.owl
- The region content ontology design pattern represents regions that are portions of a dimensional space which can be used as a value for a quality of an Entity. The CP is extracted from DOLCE + DnS Ultra Lite ontology.

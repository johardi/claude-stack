# Parameter

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Parameter
**OWL Building Block:** http://ontologydesignpatterns.org/cp/owl/parameter.owl

## Intent

To represent parameters to be used for a certain concept.

## Competency Questions

- What parameters constrain a certain concept?
- What is the data value of a certain parameter?

## Domains

- General

## Solution Description

A basic pattern to represent parameters over concepts. A Concept can have a Parameter that constrains the attributes that a classified Entity can have in a certain Situation. Parameters are constraints or selections on observable values.

## Elements

### Classes

- **Concept** — A SocialObject, defined in a Description. Once defined, a Concept can be used in other descriptions. The classifies relation relates concepts to entities at some time.
- **Parameter** — A Concept that classifies something having a certain value, e.g. 'High' can be said of people taller than 185 cm. In order to formally represent constraints, an anonymous type must be added to a parameter instance, using a property that conveys the semantics of the parameter.

### Object Properties

- **hasParameter** — A Concept can have a Parameter that constrains the attributes that a classified Entity can have in a certain Situation, e.g. a 4WheelDriver Role definedIn the ItalianTrafficLaw has a MinimumAge parameter on the Amount 16.
- **isParameterFor** — Inverse of hasParameter.

### Data Properties

- **hasParameterDataValue** — Parametrizes values from a datatype. For example, a Parameter AgeForDriving hasParameterDataValue 18 on datatype xsd:int, in the Italian traffic code. More complex parametrization requires workarounds (e.g. creating sub-parameters for ranges: MinimumAgeRange and MaximumAgeRange). Ordering on subparameters can be created by using or specializing the object property 'precedes'.

## Consequences

Parameters can be associated with concepts to constrain the attributes of classified entities in specific situations.

## Scenarios

(No specific scenarios provided.)

## Related Patterns

- Classification
- Description
- Situation

## Additional Information

The parameter content ontology design pattern. Extracted from the DOLCE Ultra Lite ontology (http://www.ontologydesignpatterns.org/ont/dul/DUL.owl). It represents parameters which are constraints or selections on observable values. Submitted by Aldo Gangemi.

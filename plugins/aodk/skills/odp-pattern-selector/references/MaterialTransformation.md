# Material Transformation

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Material_Transformation
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/materialtransformation.owl

## Intent

To contextualize the transformation process from raw components and the required equipment to a final manufactured artifact.

## Competency Questions

- What material resources were required to produce a product?
- Where did the transformation take place?
- What was the time necessary for the transformation?
- What other materials or conditions were necessary for the transformation process to occur?
- What materials change during the transformation?

## Domains

- Manufacturing
- Chemistry
- Workflow
- Ecology

## Solution Description

The pattern models a material transformation as something that has inputs and catalysts, and produces some outputs. All inputs, catalysts, and outputs are material, and within them, embodied energy may be described. Instances of this pattern may be chained with other instances or with instances of semantic trajectory.

## Elements

### Classes

- **MaterialTransformation** — The central class representing a transformation process that converts input materials into output products, potentially using catalysts and energy.
- **Resource** — Input materials consumed or used in the transformation process.
- **Product** — Output materials produced by the transformation process.
- **Catalyst** — Materials or conditions necessary for the transformation process to occur but not consumed by it.
- **MaterialType** — Classification of materials involved in the transformation.
- **Energy** — Energy involved in or embodied within the transformation process.
- **EnergyValue** — A quantitative measure of energy.
- **EnergyUnit** — The unit of measurement for energy values.
- **Neighborhood** — The spatial context (location) where the transformation occurs.

### Object Properties

- **hasInput** — Relates a MaterialTransformation to its input Resources.
- **hasOutput** — Relates a MaterialTransformation to its output Products.
- **hasCatalyst** — Relates a MaterialTransformation to its Catalyst(s).
- **hasEmbodiedEnergy** — Relates a material (Resource, Product, or Catalyst) to its embodied Energy.
- **hasEnergyValue** — Relates Energy to its quantitative EnergyValue.
- **hasEnergyUnit** — Relates Energy to its EnergyUnit.
- **needsEnergy** — Relates a MaterialTransformation to the Energy required for the process.
- **occursAtTimeInterval** — Relates a MaterialTransformation to the time interval during which it occurs.
- **occursInNeighborhood** — Relates a MaterialTransformation to its spatial Neighborhood.

### Data Properties

- **asLiteral** — A literal (string) representation of a value.
- **asNumeric** — A numeric representation of a value.

## Consequences

This is not a very generic pattern describing a change of states. It may not be applicable to broader types of transformation, like change of money or change of political affiliations. However, an instance of this pattern may be chained with another instance of this pattern or an instance of semantic trajectory. There are two important constraints not expressible in OWL: (1) at least one input must not be in the output, and (2) at least one output must not be part of the input.

## Scenarios

- A pile of wood is transformed into ash by burning.
- Embodied energy involved in the process of mixing aggregate, water, cement, and other binders to create concrete.
- Materials required to construct a manufactured artifact such as a window (glass, wood, aluminum).

## Related Patterns

- **Transition** — A more generic pattern for state changes; Material Transformation is specific to physical/material changes.
- **Sequence** — For chaining multiple transformation steps.
- **Semantic Trajectory** — Can be combined with Material Transformation for tracking material flows.

## Additional Information

- Submitted by: Adila Krisnadhi
- Certified pattern
- Submitted to WOP 2014
- Full description: "An Ontology Design Pattern and Its Use Case for Modeling Material Transformation" (Semantic Web Journal) — http://www.semantic-web-journal.net/content/ontology-design-pattern-and-its-use-case-modeling-material-transformation-1
- OWL limitations: Two key constraints (at least one input not in output, at least one output not in input) cannot be expressed in OWL/FOL.

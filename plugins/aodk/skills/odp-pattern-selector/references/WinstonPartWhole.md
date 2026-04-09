# Winston Part-Whole

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:WinstonPartWhole
**OWL Building Block:** https://raw.githubusercontent.com/cogan-shimizu-wsu/WinstonPartWhole/master/WinstonPartWhole.owl
**Submitted by:** Cogan Shimizu

## Intent

To provide a comprehensive taxonomy of part-whole relations based on the Winston, Chaffin, and Herrmann (1987) classification. This pattern distinguishes six types of meronymic (part-whole) relations, each with different properties regarding functionality, homeomericity, and separability.

## Competency Questions

- What type of part-whole relation holds between these two entities?
- Is this entity a component of another entity?
- Is this a member-collection, portion-mass, or stuff-object relation?
- What features does this activity have?
- What places are contained within this area?

## Domains

- Parts and Collections
- General

## Solution Description

The pattern provides six distinct object properties, each representing one of Winston et al.'s six types of part-whole (meronymic) relations:

1. **Component–Integral Object** (po-component): e.g. handle–cup, wheel–car
2. **Member–Collection** (po-member): e.g. tree–forest, ship–fleet
3. **Portion–Mass** (po-portion): e.g. slice–pie, grain–salt
4. **Stuff–Object** (po-stuff): e.g. steel–car, hydrogen–water
5. **Feature–Activity** (po-feature): e.g. paying–shopping, dating–adolescence
6. **Place–Area** (po-place): e.g. oasis–desert, room–house

## Elements

### Classes

None defined locally (the pattern focuses on properties that can be applied to any domain classes).

### Object Properties

- **po-component** (owl:ObjectProperty) — Component–Integral Object relation. The part is a functional component of a structured whole. Functional, not homeomeric, separable. Example: a handle is a component of a cup.
- **po-member** (owl:ObjectProperty) — Member–Collection relation. The part is a member of a collection. Not functional, not homeomeric, separable. Example: a tree is a member of a forest.
- **po-portion** (owl:ObjectProperty) — Portion–Mass relation. The part is a portion of a homogeneous mass. Not functional, homeomeric, separable. Example: a slice is a portion of a pie.
- **po-stuff** (owl:ObjectProperty) — Stuff–Object relation. The part is the material or substance of which the whole is made. Not functional, homeomeric, not separable. Example: steel is the stuff of a car.
- **po-feature** (owl:ObjectProperty) — Feature–Activity relation. The part is a feature or phase of an activity or process. Functional, not homeomeric, not separable. Example: paying is a feature of shopping.
- **po-place** (owl:ObjectProperty) — Place–Area relation. The part is a place within a larger area. Not functional, homeomeric, not separable. Example: an oasis is a place within a desert.

### Data Properties

None.

## Consequences

This pattern provides a fine-grained classification of part-whole relations that helps avoid incorrect transitive inferences that arise when a single generic "part-of" property is used for semantically different meronymic relations. Each property type has distinct logical characteristics (functionality, homeomericity, separability) that guide appropriate usage.

## Scenarios

- A handle is a **component** of a cup (po-component).
- A tree is a **member** of a forest (po-member).
- A slice is a **portion** of a pie (po-portion).
- Steel is the **stuff** of a car body (po-stuff).
- Paying is a **feature** of shopping (po-feature).
- An oasis is a **place** in a desert (po-place).

## Related Patterns

- **PartOf** — generic transitive part-of (this pattern refines it into 6 subtypes)
- **Componency** — intransitive component relation (overlaps with po-component)
- **Constituency** — cross-layer constituency (overlaps with po-stuff)
- **CollectionEntity** — membership (overlaps with po-member)

## Additional Information

- Based on: Winston, M. E., Chaffin, R., & Herrmann, D. (1987). A taxonomy of part-whole relations. *Cognitive Science*, 11(4), 417–444.
- This pattern was submitted without detailed intent/CQ fields in the ODPA repository. The documentation above is reconstructed from the Winston et al. taxonomy and the OWL building block.

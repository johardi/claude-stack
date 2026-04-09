# Time Indexed Part Of

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:TimeIndexedPartOf
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/timeindexedpartof.owl
**Also Known As:** temporary part of
**Extracted From:** http://www.loa-cnr.it/ontologies/DUL.owl

## Intent

To represent objects that have temporary parts.

## Competency Questions

- When was this object part of this other one?
- Which object was this one part of at a certain time?
- What are the parts of this object at a certain time?

## Domains

- Parts and Collections

## Solution Description

This pattern reifies the part-of relation into a situation (TimeIndexedPartOf) that connects at least two Objects — one as the whole, the other(s) as the part(s) — together with a TimeInterval. This allows expressing that parthood holds at a specific time, which is not possible with a simple binary part-of property.

## Elements

### Classes

- **Object** (owl:Class) — Any physical, social, or mental object, or a substance.
- **TimeIndexedPartOf** (owl:Class) — A situation that includes at least two Objects, one having the role of whole object, the other(s) being a part(s) of it, and one time interval.

### Object Properties

- **atTime** (owl:ObjectProperty) — A relation between a temporary part-of situation and the time it occurs at. Subproperty of isSettingFor. Domain: TimeIndexedPartOf. Range: TimeInterval.
- **isTimeOf** (owl:ObjectProperty) — The inverse of atTime.
- **includesWholeObject** (owl:ObjectProperty) — A relation between a temporary part-of situation and the whole object involved. Subproperty of isSettingFor. Domain: TimeIndexedPartOf. Range: Object.
- **isWholeObjectOf** (owl:ObjectProperty) — The inverse of includesWholeObject.
- **includesPartObject** (owl:ObjectProperty) — A relation between a temporary part-of situation and the part(s) involved. Subproperty of isSettingFor. Domain: TimeIndexedPartOf. Range: Object.
- **isPartObjectOf** (owl:ObjectProperty) — The inverse of includesPartObject.

### Data Properties

None.

## Consequences

This pattern allows designers to represent part-whole relations with a temporal index (holding at a certain time). It reifies the relation as a situation, enabling qualification with time intervals.

## Scenarios

- My Toyota Yaris mounted Michelin pneumatics in 2007, but in 2008 it mounts Pirelli pneumatics.

## Related Patterns

- **PartOf** — simple transitive part-of (no temporal aspect)
- **Componency** — intransitive proper part (no temporal aspect)
- **Situation** — general situation pattern (this pattern specializes it)
- **TimeInterval** — time interval pattern (used as a component)

## Additional Information

- **Specialization Of:** Situation
- **Has Components:** PartOf, TimeInterval
- **Examples (OWL):** http://www.ontologydesignpatterns.org/cp/examples/timeindexedpartof/yarispneumatics.owl
- This pattern also includes the elements of the Situation, TimeInterval, and PartOf patterns.

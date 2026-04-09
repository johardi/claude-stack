# Move

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Move
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/move.owl

## Intent

To represent the action of moving a physical object from one place to another, including origin, destination, trajectory, and decomposition into sub-moves.

## Competency Questions

- What physical object was moved?
- Where was the object moved from?
- Where was the object moved to?
- What place did the move take place at (trajectory)?
- What sub-moves does this move consist of?

## Domains

- Cultural heritage
- Logistics
- General

## Solution Description

The Move content ontology design pattern represents the action of moving a physical object from a place to another. The Move CP is extracted from the CIDOC-CRM ontology (http://cidoc.ics.forth.gr/cidoc_v4.2.owl). It models a Move event class with properties for the moved object, origin, destination, and trajectory, along with decomposition into sub-moves.

## Elements

### Classes

- **Move** — This class comprises changes of the physical location of instances of PhysicalObject. The class inherits the property 'took place at' (witnessed): Place. This property should be used to describe the trajectory or a larger area within which a move takes place, whereas movedTo and movedFrom describe the start and end points only. Moves may also be documented to consistsOf other moves, in order to describe intermediate stages on a trajectory.
- **PhysicalObject** — Items of a material nature that are units for documentation and have physical boundaries that separate them completely in an objective way from other objects. Includes all aggregates of objects made for functional purposes of whatever kind, independent of physical coherence, such as a set of chessmen. Also called "bona fide objects."
- **Place** — Extents in space, in particular on the surface of the earth, in the pure sense of physics: independent from temporal phenomena and matter. Determined by reference to the position of "immobile" objects such as buildings, cities, mountains, rivers, or dedicated geodetic marks. Any object can serve as a frame of reference for Place determination.

### Object Properties

- **moved** — Identifies the PhysicalObject that is moved during a move event. Implies the object's passive participation. Example: Monet's painting "Impression sunrise" was moved for the first Impressionist exhibition in 1874.
- **movedBy** — Inverse of moved.
- **movedFrom** — Identifies the starting Place of a Move. A move may be linked to many origins (picking up a set of objects).
- **wasOriginOf** — Inverse of movedFrom.
- **movedTo** — Identifies the destination of a Move. A move may be linked to many terminal Places (distribution of a set of objects).
- **wasDestinationOf** — Inverse of movedTo.
- **tookPlaceAt** — Describes the spatial location of an instance of a Move. The related Place should be seen as an approximation of the geographical area within which the phenomena occurred.
- **witnessed** — Inverse of tookPlaceAt.
- **consistsOf** — Describes the decomposition of an instance of Move into discrete, subsidiary moves. The sub-moves form a logical whole.
- **formsPartOf** — Inverse of consistsOf.

### Data Properties

None.

## Consequences

The pattern enables representing move events with origin, destination, and trajectory information. Moves can be decomposed into sub-moves for modeling intermediate stages. The pattern is specific to physical objects and spatial movements. It does not cover abstract transitions or state changes (for those, see the Transition pattern).

## Scenarios

- Monet's painting "Impression sunrise" was moved from storage to an exhibition hall for the first Impressionist exhibition in 1874.
- A shipment of goods is moved from a warehouse in Rotterdam to a distribution center in Berlin, with an intermediate stop in Cologne (modeled as sub-moves).

## Related Patterns

- **Transition** — For representing abstract state transitions (not spatial moves).
- **Participation** — For general participation of objects in events.
- **Sequence** — For ordering moves or sub-moves in time.

## Additional Information

- Submitted by: Aldo Gangemi
- Certified pattern
- Extracted from: CIDOC-CRM ontology (http://cidoc.ics.forth.gr/cidoc_v4.2.owl)
- Reengineered from: CIDOC-CRM ontology

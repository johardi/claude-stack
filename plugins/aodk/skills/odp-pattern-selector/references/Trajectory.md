# Trajectory

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Trajectory
**OWL Building Block:** http://krisnadhi.github.io/onto/trajectory.owl

## Intent

The pattern provides a model of trajectory, which is understood as a sequence of spatiotemporal points. The model generalizes the Semantic Trajectory pattern from [Hu, et al., COSIT 2013] by employing the notion of place, instead of location/geo-coordinate, to represent the spatial extent of the trajectory. This pattern is suitable for a variety of trajectory datasets and easily extensible by aligning to or matching with existing trajectory ontologies, foundational ontologies, or other domain-specific vocabularies.

## Competency Questions

- Show the birds which stop at x and y.
- Show the birds which move at a ground speed of 0.4 m/s.
- Show the trajectories of rivers which cross national parks.
- Where are the ports at which the oceanographic cruise A3221 stopped after leaving Woods Hole?
- List the places and times that represent the spatiotemporal extent of the 1990 World Chess Championship event.

## Domains

- General
- Earth Science / Geoscience

## Solution Description

This pattern is reengineered from [Hu, et al., COSIT 2013] with changes as described in the intent of the pattern.

## Elements

### Classes

- **Trajectory** — Represents the notion of trajectory; the main class that can be hooked with other patterns. A trajectory is understood as a sequence of fixes connected by segments. There is exactly one starting fix and exactly one ending fix. Each fix has a temporal extent and a place.
- **Fix** — Describes a fix, which is an adorned spatiotemporal point. A sequence of fixes forms the trajectory.
- **StartingFix** — The first fix in a particular sequence of fixes.
- **EndingFix** — The last fix in a particular sequence of fixes.
- **Segment** — Captures the "connection" between two consecutive fixes. A segment starts from a fix and ends at another fix. If used to model the trajectory of a moving object, each segment is traversed by that moving object. Additional information can be attached as attributes.
- **MovingObject** — Hook to an ontology/pattern that describes the moving object which moves along the trajectory.
- **Place** — Hook to other pattern/ontology that describes the notion of place, which is more general than just a location/geo-coordinate.
- **TimeEntity** — Hook to class/pattern/ontology that models time; provides the temporal extent of the trajectory (e.g., W3C Time Ontology).
- **Attribute** — Captures additional information that enriches some fix or segment.

### Object Properties

- **hasTrajectory** — Anything that has a trajectory can use this property to connect it to the trajectory instance.
- **hasFix** — Relating the trajectory to each of its fixes.
- **hasSegment** — Relating the trajectory to each of its segments.
- **nextFix** — Relates one fix to the immediately following fix in the sequence.
- **startsFrom** — Connects a segment to the fix it starts from.
- **endsAt** — Connects a segment to the fix it ends at.
- **traversedBy** — Connect a segment to the moving object that traverses it.
- **atPlace** — Connects anything (including fixes) to Place.
- **atTime** — Connects anything (including fixes) to TimeEntity.
- **hasAttribute** — Connects a fix or a segment to additional information as represented by an instance of Attribute.

## Consequences

Unlike the original version of Semantic Trajectory, this pattern omits the hook to the data source for fixes (which was a subclass of ssn:Device) because instead of location/geo-coordinate, the notion of place is employed to capture the spatial extent. Nevertheless, it should be relatively straightforward to extend this version if the user wishes to attach data source information to the fixes.

## Scenarios

- Mike's trip to the GeoVoCamp 2012 from his home integrating data from GPS device, vehicle information, and personal information.
- A toucan flies through the air as recorded by researchers in MoveBank.
- The 1990 World Chess Championship event was held in two locations at two different times.

## Related Patterns

- **Place** — Hook for spatial representation.
- **Time** — Hook for temporal representation.
- **MovingObject** — Hook for the entity traversing the trajectory.
- **SpatioTemporalExtent** — Uses Trajectory as a component.

## Additional Information

- Submitted by: Adila Krisnadhi
- Reengineered from: Yingjie Hu; Krzysztof Janowicz; David Carral; Simon Scheider; Werner Kuhn; Gary Berg-Cross; Pascal Hitzler; Mike Dean; Dave Kolas: "A Geo-ontology Design Pattern for Semantic Trajectories." In COSIT 2013, pp. 438-456.

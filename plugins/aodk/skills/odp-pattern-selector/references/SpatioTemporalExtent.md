# SpatioTemporalExtent

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:SpatioTemporalExtent
**OWL Building Block:** http://krisnadhi.github.io/onto/spatiotemporalextent.owl

## Intent

This pattern models a spatiotemporal extent, i.e., a combination of spatial and temporal extent as a set of generalized trajectories which cannot have temporal overlap. This pattern reuses the semantic trajectory pattern as a component.

## Competency Questions

- Where is Poland located in 1700?
- List all places and time in which the 1990 World Chess Championship Match took place.
- Where and when did the oceanographic cruise A01132 go?

## Domains

- Earth Science / Geoscience
- General

## Solution Description

See Adila Krisnadhi, Pascal Hitzler, Krzysztof Janowicz. "A Spatiotemporal Extent Pattern based on Semantic Trajectories." Under review for WOP 2016.

## Elements

### Classes

- **SpatioTemporalExtent** — The class that represents the notion of spatiotemporal extent. A spatiotemporal extent is realized as a collection of generalized trajectories that have no temporal overlap.
- **Trajectory** — The hook to the Trajectory pattern, which acts as a component of the Spatiotemporal Extent pattern.

### Object Properties

- **hasSpatioTemporalExtent** — Property relating anything (thus the domain is trivially owl:Thing and the range is unscoped) to a SpatioTemporalExtent.
- **hasTrajectory** — Set to be equivalent to trj:hasTrajectory from the Trajectory pattern, this property relates anything (including SpatioTemporalExtent) to Trajectory.

## Consequences

Not explicitly stated. The pattern enables representation and querying of entities that exist across multiple places and times, leveraging the Trajectory pattern as a component.

## Scenarios

- The World Chess Championship Match 1990 was held in two parts: New York (October 8 to November 7) and Lyons, France (November 26 to December 30).
- The Renaissance occurred in different places at different times.
- A hurricane moves through spacetime.

## Related Patterns

- **Trajectory** — Component pattern; the SpatioTemporalExtent is composed of generalized trajectories.

## Additional Information

- Submitted by: Adila Krisnadhi
- Has Components: Trajectory

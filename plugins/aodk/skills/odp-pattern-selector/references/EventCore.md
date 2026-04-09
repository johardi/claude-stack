# EventCore

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:EventCore
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/eventcore.owl

## Intent

The purpose of this pattern is to provide a minimalistic model of event where it is not always possible to separate its spatial and the temporal aspects, thus can model events that move or possess discontinuous temporal extent. Events according to this model have at least one participant, attached via a participant-role, and may have additional descriptive information through its information object.

## Competency Questions

- Where and when did the 1990 World Chess Championship Match take place?
- Who were involved in the 1990 World Chess Championship Match?

## Domains

- General
- Event Processing

## Solution Description

See Adila Krisnadhi; Pascal Hitzler: "A Core Pattern for Events" (WOP 2016). The pattern provides a minimalistic event model with spatiotemporal extent, participant roles, and information objects as core components.

## Elements

### Classes

- **Event** — Represents any kind of events. An event possesses a spatiotemporal extent, provides at least one participant-role (performed by some entity — agents or otherwise), and may be a sub-event of another event. An event may also have additional descriptive information consolidated through an information object.
- **SpatioTemporalExtent** — Hook to a complex notion representing a unified spatial and temporal extent. Intended to cover non-static or discontinuous spatiotemporal extent. Should be aligned to a separate Spatiotemporal Extent pattern.
- **ParticipantRole** — Every ParticipantRole represents a reified relationship between an event and one of its participants. Should normally be aligned to a separate Participant-Role pattern.
- **InformationObject** — An entity that encapsulates all descriptive or non-defining information of the corresponding event, e.g., names, additional identifiers, textual descriptions, etc. Should normally be aligned to a separate Information Object pattern.

### Object Properties

- **hasSpatioTemporalExtent** — Relates Event to SpatioTemporalExtent. Range is always SpatioTemporalExtent (globally). Domain is not restricted to Event since non-Events may also have spatiotemporal extent.
- **providesParticipantRole** — Relates Event to ParticipantRole. Range is always ParticipantRole. Domain is not restricted to Event since non-Events may also provide a participant role.
- **subEventOf** — Expresses partonomic relation between two events. Domain and range are always Event.
- **subSpatioTemporalExtentOf** — Indicates partonomic relation between two spatiotemporal extents. Domain and range are not explicitly stated; assumed given by the spatiotemporal extent pattern actually used.
- **hasInformationObject** — Relates Event to InformationObject. Domain is not restricted to Event. Range is always InformationObject.
- **freshProp1** — Artificially generated property to express the rule: Event(?x) ^ providesParticipantRole(?x,?p) ^ subEventOf(?x,?y) -> providesParticipantRole(?y,?p). Translated into OWL axioms.
- **freshProp2** — Artificially generated property to express the rule: Event(?x) ^ hasSpatioTemporalExtent(?x,?w) ^ subEventOf(?x,?y) ^ Event(?y) ^ hasSpatioTemporalExtent(?y,?z) -> subSpatioTemporalExtentOf(?w,?z). Translated into OWL axioms.

### Annotation Properties

- **DASE_RULE** — Attached to an axiom, this annotation property provides information on the original (SWRL) rule from which the axiom was obtained through translation.

### Data Properties

None.

## Consequences

This pattern can model moving events and events with discontinuous temporal extents, provided an appropriate spatiotemporal extent model is used. This pattern, however, does not facilitate modeling complex relationships between events, such as causality, provenance, or correlation.

## Scenarios

- The 1990 World Chess Championship Match takes place in New York from October 8 to November 7, 1990, and in Lyons, France, from November 26 to December 30, 1990.

## Related Patterns

- **SpatioTemporalExtent** — Should be aligned to provide the unified spatial-temporal extent model.
- **ParticipantRole** — Should be aligned for modeling reified participant-event relationships.
- **AgentRole** — Related role pattern for agent participants.
- **Objectrole** — Related role pattern for non-agent object participants.
- **Information realization** — Related pattern for information modeling.
- **InformationObjectsAndRepresentationLanguages** — Related pattern for information representation.
- **EventProcessing** — Related pattern for event processing scenarios.

## Additional Information

- Submitted by: Adila Krisnadhi
- Certified pattern
- Submitted to WOP:2016
- The freshProp1 and freshProp2 properties are artifacts of translating SWRL rules into OWL axioms and are not intended for direct use in modeling.

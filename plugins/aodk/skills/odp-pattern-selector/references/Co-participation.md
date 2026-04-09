# Co-participation

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Co-participation
**OWL Building Block:** http://www.ontologydesignpatterns.org/cp/owl/coparticipation.owl

## Intent

To represent two objects that both participate in a same event.

## Competency Questions

- What objects participate in a same event?
- Who is involved with whom in something?

## Domains

- General

## Solution Description

Any two objects, agents, etc. participating in a same event, even partly or for some limited time, can be related. The pattern provides room for representing participation in that event as well, by importing the Participation pattern.

This pattern does not allow to express the complete relation between an event and its participants: this has to be added manually.

## Elements

### Classes

No locally defined classes. The pattern relies on the imported Participation pattern and DUL (DOLCE+DnS Ultralite) ontology classes.

### Object Properties

- **coparticipatesWith** (owl:ObjectProperty) — A symmetric binary relation between objects. It is intended to represent co-participation in the same event, and such event and the related participation relations should be added separately.

### Data Properties

None.

## Consequences

The pattern allows representing the fact that two objects co-participate in some event. However, the event itself and the individual participation relations must be modeled separately (e.g., by importing the Participation pattern).

## Scenarios

- Mike and Greta had a great fun together.
- Aldo Gangemi and Valentina Presutti co-participate at the ISWC 2007 conference.

## Related Patterns

- **Participation** — Co-participation imports and extends the Participation pattern to add the symmetric co-participation relation.

## Additional Information

- Submitted by: Aldo Gangemi
- Certified pattern
- Extracted from: DUL (DOLCE+DnS Ultralite) ontology — http://www.loa.cnr.it/ontologies/DUL.owl
- Example OWL file: http://www.ontologydesignpatterns.org/cp/examples/coparticipation/ISWCco-participation.owl

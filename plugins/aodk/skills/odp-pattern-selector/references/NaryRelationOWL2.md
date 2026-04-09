# N-Ary Relation Pattern (OWL 2)

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:N-Ary_Relation_Pattern_(OWL_2)
**OWL Building Block:** http://purl.org/net/nary-relation

## Intent

To allow the inference of property relations between the different relata of an original N-Ary relation based on its reification, using OWL 2 features (local reflexivity and property chains).

## Competency Questions

- What are the relata of an n-ary relation?
- What are the binary projections of an n-ary relation?

## Domains

- General

## Solution Description

OWL does not support N-Ary relations natively. This means that an n-ary relation can only be represented in its reified form in OWL. This is problematic, as the relational character is then completely lost.

The N-Ary relation is reified by creating a class for the relation (NR), and creating properties and classes for the domain (D) and ranges (R1-Rn) of the relation (that is, if the relation is directional). The NR class is specified using a local reflexivity restriction of the form: `NR equiv is_NR some Self`. Role chains are then specified for each of the binary relations between the domain and ranges. For instance: `has_NR o is_NR o r1 -> has_r1`.

## Elements

### Classes

- **NR (N-ary Relation)** — The reified class representing the n-ary relation. Specified with a local reflexivity restriction (`NR equiv is_NR some Self`).
- **D (Domain)** — The domain class of the relation.
- **R1..Rn (Ranges)** — The range classes of the relation.

### Object Properties

- **is_NR** — Reflexive property on NR, used for the local reflexivity restriction.
- **has_NR** — Relates the domain to the n-ary relation instance.
- **r1..rn** — Properties from NR to each range class.
- **has_r1..has_rn** — Inferred properties from domain to ranges via property chains (e.g. `has_NR o is_NR o r1 -> has_r1`).

## Consequences

The patient (e.g., Christine, P) is related both to the diagnosis value (Cancer) and its probability via inferred binary projections. The relational character of the n-ary relation is preserved through OWL 2 property chains.

## Scenarios

- The cancer diagnosis relation from the SWBP N-Ary relations patterns: a patient (Christine) has a diagnosis of Cancer with a certain probability. The pattern allows inferring direct relations between the patient and the diagnosis value and probability.

## Related Patterns

- N-ary Participation
- Situation (alternative reification approach)

## Additional Information

This pattern uses OWL 2 features: local reflexivity and property chains. The reusable component contains an N-Ary relation with four ranges and a domain, which can easily be extended or reduced. Available under the CC-BY licence (http://creativecommons.org/licenses/by/2.0/). Author: Rinke Hoekstra.

Reference: Rinke Hoekstra. Ontology Representation – Design Patterns and Ontologies that Make Sense, volume 197 of Frontiers of Artificial Intelligence and Applications. IOS Press, Amsterdam, June 2009.

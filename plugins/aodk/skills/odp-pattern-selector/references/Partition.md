# Partition

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Partition
**OWL Building Block:** http://www.informatik.uni-ulm.de/ki/Noppens/generation.owl (example)

## Intent

The Partition Pattern is a logical pattern that introduces axioms which model a partition of concepts. A partition is a general structure which is divided into several disjoint parts. With respect to ontologies, the structure is a concept which is divided into several pair-wise disjoint concepts. This pattern reflects the simplest case where a named concept is defined as a partition of concepts.

## Competency Questions

Not explicitly listed as questions. The pattern addresses:
- How to model a concept that is exhaustively divided into disjoint subconcepts.
- How to ensure that all instances of the parent concept belong to exactly one of the partition members.

## Domains

- General
- Logic / Structural Pattern

## Solution Description

Let P be a named concept that is the partition which is divided into several concepts C_i. Then the partition is defined by introducing the following axioms:

In OWL 2 Abstract Syntax:
```
EquivalentClasses(P, ObjectUnionOf(C1, ..., Cn))
DisjointClasses(C1, ..., Cn)
```

This ensures:
1. P is equivalent to the union of all partition members (covering axiom).
2. All partition members are pairwise disjoint (disjointness axiom).

Note that C_i can also be arbitrary concept expressions.

## Elements

### Axiom Patterns

- **EquivalentClasses(P, ObjectUnionOf(C1, ..., Cn))** — Defines the partition concept P as exactly the union of its parts.
- **DisjointClasses(C1, ..., Cn)** — Ensures all partition members are pairwise disjoint.

### Classes

- **P** (Partition concept) — The named concept being partitioned.
- **C1, ..., Cn** (Partition members) — The disjoint subconcepts that exhaustively cover P.

## Consequences

Any instance of P must be an instance of exactly one C_i. The reasoner can infer partition membership and detect inconsistencies when an individual is classified under multiple partition members.

## Scenarios

In an ontology about family relationships, the concept Gender is partitioned into Male and Female:
```
EquivalentClasses(Gender, ObjectUnionOf(Male, Female))
DisjointClasses(Male, Female)
```

This enables defining concepts like:
- `Parent-Of-Son ≡ ∃hasChild.Male`
- `Parent-Of-Daughter ≡ ∃hasChild.Female`
- `Aunt ≡ Uncle-Or-Aunt ⊓ Female`

## Related Patterns

- **Value Partition** (W3C SWBP) — A closely related pattern for modelling fixed value sets.
- **Object with States** — Uses partition-like structure for state modelling.

## Additional Information

- Submitted by: Olaf Noppens
- Submitted to: WOP 2009
- This is a **logical/structural pattern**, not a content pattern — it provides axiom templates rather than domain-specific classes and properties.
- References:
  - Patel-Schneider, P. F., Swartout, B.: "Description-Logic Knowledge Representation System Specification", 1993.
  - Motik, B., Patel-Schneider, P. F., Parsia, B.: "OWL 2 Structural Specification and Functional-Style Syntax." W3C Candidate Recommendation, 11 June 2009.

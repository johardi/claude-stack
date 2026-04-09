# Modeling Checklist

Consult this checklist during **Step 4 (Draft Proposal)** before finalizing the class hierarchy. These checks catch common over-classification and structural errors.

---

## 1. Enumerated Options Are Individuals, Not Subclasses

When a class represents a category with a **fixed set of values** that all share the same structure (same properties, same axioms) and differ only in their label or identity, those values are **NamedIndividuals** of the class, not subclasses.

This applies to any concept that acts as a closed list of options — labels, tags, rating categories, named options in a dataset column, etc.

**Key test:** If no CQ requires different axioms or properties for each option, they are individuals.

**Consistency rule:** Apply this consistently across the ontology — if one enumerated class uses individuals, all analogous enumerated classes must too. Creating subclasses for enumerated options is one of the most common over-classification errors; it inflates the class count without adding reasoning benefit.

## 2. The "Would It Have Its Own Instances?" Test

Before creating a subclass, ask: "Would instances of this proposed subclass ever be created, and would they behave differently from instances of the parent class?"

If the proposed subclass would never be instantiated — because the concept itself *is* the instance — it should be a **NamedIndividual** of the parent class, not a subclass.

**Rule of thumb:** Subclasses are for types that get instantiated; named options, labels, and enumerated values are individuals.

## 3. CQ-Driven Class Justification

Before adding any class to the draft, state which CQ requires it to be a class rather than an individual. If the answer is "none," omit it from the class hierarchy.

## 4. Class Budget Check

For a typical task with 5–15 CQs, expect roughly 5–25 classes. If the draft exceeds this range, re-examine each class against the CQs and prune those that are not required. This is a guideline, not a hard limit — some domains genuinely need more classes — but large overruns should trigger a review.

## 5. CQ Examples Are Not Class Requirements

When a CQ uses an example to illustrate a query pattern (e.g. "What are the plays written by Shakespeare?" uses "Shakespeare" as an example), do not create a class for the example. The example is an individual or a query parameter, not a class. Focus on the structural pattern the CQ requires (e.g. a `writtenBy` property between `Play` and `Person`).

## 6. Context Classes Stay Simple

When a concept appears in the user story only as context for another concept's properties (e.g. "plays are performed at a venue"), model it as a single class without subclasses unless a CQ specifically requires distinguishing subtypes. Do not elaborate taxonomies for context concepts.

## 7. CQ-Driven Taxonomic Placement

When placing a concept in the is-a hierarchy, examine how the CQs **use** the concept, not just its dictionary definition:

- If CQs treat a concept as something **attended, observed, or participated in** — and it has temporal/spatial extent — it is likely an **Event**, even if it could also be categorized as an artifact or creative work.
- If CQs treat a concept as a **container for other events** (e.g. "what X could be seen during Y?"), the parent–child relationship is likely a **sub-event** composition, not a custom linking property. Check the **EventCore** ODP (`subEventOf`).
- If CQs ask about a concept's **content, authorship, or informational properties** alongside its event-like properties, consider whether the concept has a **dual nature** (both an information object and an event/realization). Check the **InformationRealization** ODP.

**Test:** For each proposed class, state in one sentence which CQ dictates its hierarchical placement. If the placement is based on intuition rather than a CQ, reconsider.

## 8. Hierarchy Completeness

- Every proposed class must participate in at least one SubClassOf relationship (either as parent or child).
- If a proposed class would be a direct child of `owl:Thing` with no children of its own, reconsider whether it needs an abstract parent or whether it is needed at all.
- When the scoped concept is clearly a specialization of a broader concept, model both the general parent and the specific subclass — even if only the specialization is in scope.

## 9. Property Minimalism

- Create only object and data properties that are directly required to answer at least one CQ. Before adding each property, cite which CQ it serves.
- Do not create inverse properties by default. Only add an inverse when a specific CQ requires navigating the relationship in the reverse direction.
- State cardinality only where a CQ explicitly requires it.

## 10. Anti-Pattern Scan

Before finalizing the draft, scan for these common anti-patterns:

| Anti-Pattern | What to Check | Corrective ODP |
|---|---|---|
| **Role as subclass of entity** | Are roles (Coordinator, Reviewer, etc.) modeled as disjoint subclasses of an entity that can change roles? | **AgentRole**, **TimeIndexedPersonRole** |
| **Missing inverses** | Does a CQ require navigating a relationship in both directions, but only one direction is defined? | Add inverse property |
| **Unnecessary n-ary reification** | Is an intermediary class created for a relationship that has only 1–2 attributes and is never queried independently? | Remove intermediary; attach attributes to an endpoint |
| **Warranted n-ary reification** | Does a relationship genuinely connect 3+ entities or repeat with different attributes? | **Situation**, **NaryParticipation**, **NaryRelationOWL2** |
| **Overly strict datatypes** | Is `xsd:dateTime` used for dates (no time component) or `xsd:integer` for years? | Prefer `xsd:date`, `xsd:gYear`; document DL tradeoffs |

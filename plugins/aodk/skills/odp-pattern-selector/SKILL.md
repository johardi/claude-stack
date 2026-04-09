---
name: odp-pattern-selector
description: Browse and select Ontology Design Patterns (ODPs) from the ODP catalogue for ontology modeling. Use whenever the user needs to choose a modeling pattern, asks "how should I model X?", wants to represent parts, roles, events, time, collections, situations, n-ary relations, or any recurring ontology structure. Also use proactively during Step 3 (Knowledge Organization) and Step 4 (Draft Proposal) of the ontology-builder workflow when identifying candidate axiom patterns. Covers 55+ patterns from ontologydesignpatterns.org and the ODPA repository.
version: 1.0.0
allowed-tools: [Read, Glob, Grep]
---

# Ontology Design Pattern Selector

Use this skill to **find and apply established Ontology Design Patterns (ODPs)** when modeling an ontology. ODPs are reusable, community-vetted solutions to common ontology engineering problems. Each pattern comes with a formal OWL building block, competency questions, and usage guidance.

## When to Use

- **Step 3 (Knowledge Organization)**: When identifying candidate axiom patterns and checking whether an existing ODP fits the domain.
- **Step 4 (Draft Proposal)**: When structuring the class hierarchy and choosing how to model relations, roles, events, temporal aspects, or part-whole structures.
- **Ad-hoc modeling questions**: When the user asks "how should I model roles?", "what pattern handles n-ary relations?", "how do I represent part-whole with time?", etc.
- **Import-over-reinvention**: When a pattern's OWL building block can be imported or adapted rather than recreating equivalent structures.

## How to Use

1. **Run the modeling checklist** (`references/ModelingChecklist.md`): Before finalizing any draft, check for over-classification, anti-patterns, and structural issues. This is mandatory during Step 4.
2. **Scan the catalogue below** to find patterns matching the user's modeling problem (match by intent, CQs, or domain).
3. **Read the full reference file** for candidate patterns: each pattern has a detailed file at `references/<pattern-name>.md` with full documentation, OWL elements, consequences, related patterns, and the OWL building block URL.
4. **Present candidates** to the user with rationale for why each pattern fits.
5. **Apply the pattern** by adapting its classes and properties to the user's domain, referencing the OWL building block as a template.

## Source

All patterns originate from [ontologydesignpatterns.org](http://ontologydesignpatterns.org) and the [ODPA patterns repository](https://github.com/odpa/patterns-repository). Most are based on DOLCE-UltraLite (DUL).

---

## Pattern Catalogue

### Parts and Wholes

| Pattern | Intent | When to Use | Reference |
|---------|--------|-------------|-----------|
| **PartOf** | Represent entities and their parts with transitive parthood. | You need a general transitive part-whole relation (e.g. brain is part of body). | `references/PartOf.md` |
| **Componency** | Represent proper parts (intransitive) of objects. | You need non-transitive composition where components form a designed system (e.g. engine has turbine as component). | `references/Componency.md` |
| **Constituency** | Represent constituents of an entity (material composition). | The parts are a different kind from the whole — matter-form relation (e.g. a vase is constituted by clay). | `references/Constituency.md` |
| **WinstonPartWhole** | Distinguish multiple part-whole relation types (component, member, portion, stuff, feature, place). | You need fine-grained distinctions between different kinds of parthood following Winston's taxonomy. | `references/WinstonPartWhole.md` |
| **TimeIndexedPartOf** | Represent part-whole relations that change over time. | Parts can be added or removed from a whole over time (e.g. a department was part of a university from 2000 to 2010). | `references/TimeIndexedPartOf.md` |

### Collections and Membership

| Pattern | Intent | When to Use | Reference |
|---------|--------|-------------|-----------|
| **CollectionEntity** | Represent collections and their members. | You need to model groups, sets, or named collections with membership (e.g. the Louvre Egyptian collection). | `references/CollectionEntity.md` |
| **Bag** | Model bags — collections allowing duplicate items. | The collection can have multiple copies of the same element, and you need to track each item individually. | `references/Bag.md` |
| **List** | Model ordered sequences of items. | Order matters — you need first, last, next, previous navigation through a collection. | `references/List.md` |
| **Set** | Model sets — collections without duplicates. | You need a mathematical set with no repeated elements and set operations. | `references/Set.md` |

### Agents, Roles, and Participation

| Pattern | Intent | When to Use | Reference |
|---------|--------|-------------|-----------|
| **AgentRole** | Represent agents and the roles they play. | An agent (person, organization) plays one or more roles; roles are not permanent types but assignable positions. | `references/AgentRole.md` |
| **Objectrole** | Represent objects and the roles they play (generalization of AgentRole). | Any object (not just agents) can play a role — a more general version of AgentRole. | `references/Objectrole.md` |
| **ActingFor** | Represent agents acting on behalf of other agents. | One agent delegates to or acts as proxy for another (e.g. a lawyer acts for a client). | `references/ActingFor.md` |
| **Participation** | Represent objects participating in events. | You need a basic binary relation between objects and events (e.g. a person participated in a meeting). | `references/Participation.md` |
| **ParticipantRole** | Represent participation with an explicit role. | The kind of participation matters — the same object can participate in different roles (e.g. speaker vs. attendee). | `references/ParticipantRole.md` |
| **Co-participation** | Represent multiple objects participating in the same event. | You need to query which objects co-participated in an event without n-ary reification. | `references/Co-participation.md` |
| **TimeIndexedPersonRole** | Represent time-bounded roles played by persons. | Roles are temporary and you need to record when a person held a specific role. | `references/TimeIndexedPersonRole.md` |

### Events, Actions, and Processes

| Pattern | Intent | When to Use | Reference |
|---------|--------|-------------|-----------|
| **Action** | Represent intentional actions by agents. | You need to model deliberate actions that agents perform (with a plan or goal behind them). | `references/Action.md` |
| **EventCore** | Represent events with participants, time, and place. | You need a rich event model connecting who, what, when, and where. | `references/EventCore.md` |
| **BasicPlan** | Represent plans as descriptions that define goals and tasks. | You need to model plans, strategies, or workflows as first-class objects that can be described and compared. | `references/BasicPlan.md` |
| **BasicPlanExecution** | Represent the execution of a plan (linking plan to actual performance). | You need to track how a plan was actually carried out — which actions satisfied which plan steps. | `references/BasicPlanExecution.md` |
| **TaskExecution** | Represent tasks and their execution by agents. | You need to model task assignment and completion — who did what task and when. | `references/TaskExecution.md` |
| **Controlflow** | Represent control flow ordering between tasks or actions. | You need to model if-then, sequence, parallel, or conditional branching between process steps. | `references/Controlflow.md` |
| **Move** | Represent the movement of entities from one place to another. | Something physically moves — you need origin, destination, and the moving object. | `references/Move.md` |
| **Transition** | Represent state transitions of entities. | An object moves from one state to another as the result of a process or event. | `references/Transition.md` |
| **MaterialTransformation** | Represent transformations of materials or substances. | Raw materials are transformed into products through a process (e.g. manufacturing, cooking). | `references/MaterialTransformation.md` |

### Time, Sequence, and Recurrence

| Pattern | Intent | When to Use | Reference |
|---------|--------|-------------|-----------|
| **Sequence** | Represent ordering/precedence relations (transitive and intransitive). | You need to express "before/after" between tasks, events, time intervals, or spatial objects. | `references/Sequence.md` |
| **TimeInterval** | Represent time intervals with start and end. | You need to model durations, periods, or spans of time with boundary points. | `references/TimeInterval.md` |
| **TimePeriod** | Represent named time periods. | You need named, possibly recurring time units (e.g. "Monday", "January", "Q3 2025"). | `references/TimePeriod.md` |
| **PeriodicInterval** | Represent regularly recurring intervals. | Something happens on a regular schedule (e.g. every Tuesday, every 6 months). | `references/PeriodicInterval.md` |
| **RecurrentEventSeries** | Represent series of recurring events. | A named event recurs multiple times (e.g. annual conference, weekly meeting). | `references/RecurrentEventSeries.md` |
| **RecurrentSituationSeries** | Represent series of recurring situations. | A situation (context with multiple entities) recurs regularly. | `references/RecurrentSituationSeries.md` |

### Temporal Indexing

| Pattern | Intent | When to Use | Reference |
|---------|--------|-------------|-----------|
| **TimeIndexedClassification** | Represent classification/categorization that changes over time. | An entity's category or type is not permanent — it changes over time and you need to record when. | `references/TimeIndexedClassification.md` |
| **TimeIndexedSituation** | Represent situations (contexts) anchored to specific time intervals. | You need to record when a particular situation held (e.g. during 2020, the team had these members). | `references/TimeIndexedSituation.md` |
| **TimeIndexedParticipation** | Represent participation that is bounded in time. | An object's participation in an event has a specific time range (e.g. an employee joined a project in March 2024). | `references/TimeIndexedParticipation.md` |

### Description, Situation, and Context

| Pattern | Intent | When to Use | Reference |
|---------|--------|-------------|-----------|
| **Description** | Represent descriptions as social objects that define concepts, roles, parameters. | You need to model plans, norms, regulations, diagnoses — any conceptual framework that can be applied to reality. | `references/Description.md` |
| **Situation** | Represent contexts or reified n-ary relations. | You need to group multiple related entities into a single context, or reify an n-ary relation as a first-class object. | `references/Situation.md` |
| **DescriptionAndSituation** | Link descriptions (conceptual) to situations (actual). | You need to express that a real-world situation satisfies (or violates) a description/plan/norm. | `references/DescriptionAndSituation.md` |
| **Classification** | Represent concept/category assignment to entities. | Entities are classified under concepts that are first-order objects (not just OWL classes) — e.g. tagging, folksonomies, thesauri. | `references/Classification.md` |
| **Parameter** | Represent parameters that constrain or qualify descriptions. | A description has configurable parameters with regions of allowed values (e.g. a medical guideline with dosage ranges). | `references/Parameter.md` |

### N-ary Relations and Reification

| Pattern | Intent | When to Use | Reference |
|---------|--------|-------------|-----------|
| **NaryParticipation** | Reify participation as an n-ary relation. | Participation has attributes beyond just "who" and "in what" — you need to attach role, time, or other qualifiers to the participation itself. | `references/NaryParticipation.md` |
| **NaryRelationOWL2** | Represent n-ary relations in OWL 2. | A relation connects 3+ entities simultaneously and cannot be reduced to binary properties. | `references/NaryRelationOWL2.md` |

### Space and Place

| Pattern | Intent | When to Use | Reference |
|---------|--------|-------------|-----------|
| **Place** | Represent places as first-class entities. | You need to model locations, geographic regions, or spatial entities with their own identity. | `references/Place.md` |
| **SpatioTemporalExtent** | Represent entities with both spatial and temporal extent. | Things occupy space and time together — you need to model spatiotemporal regions or events with location and duration. | `references/SpatioTemporalExtent.md` |
| **Trajectory** | Represent trajectories — paths through space over time. | An entity follows a path from point to point across time (e.g. GPS tracks, migration routes). | `references/Trajectory.md` |

### Information and Knowledge

| Pattern | Intent | When to Use | Reference |
|---------|--------|-------------|-----------|
| **InformationRealization** | Represent information objects and their physical realizations. | You need to distinguish between abstract information (e.g. a novel) and its physical forms (e.g. a hardcover copy, an ebook). | `references/InformationRealization.md` |
| **InformationObjectsAndRepresentationLanguages** | Represent information objects along with their representation languages. | Information is encoded in a specific language or format (e.g. an ontology in OWL, a document in HTML). | `references/InformationObjectsAndRepresentationLanguages.md` |
| **IntensionExtension** | Represent the distinction between intension (meaning) and extension (instances). | You need to separate a concept's definition from its actual instances (e.g. "mammal" as concept vs. all actual mammals). | `references/IntensionExtension.md` |
| **Observation** | Represent observations or measurements. | You need to model who observed what, when, where, with which method, and what result was obtained. | `references/Observation.md` |
| **Topic** | Represent topics or subjects. | Entities are about or related to topics/themes (e.g. documents have subjects). | `references/Topic.md` |
| **Tagging** | Represent tagging — associating tags with entities. | Users or systems assign free-form or structured tags to entities (e.g. social tagging, annotation). | `references/Tagging.md` |
| **Provenance** | Track the provenance/lineage of entities. | You need to record where something came from, who created it, and how (e.g. data provenance, artifact history). | `references/Provenance.md` |

### State, Disposition, and Change

| Pattern | Intent | When to Use | Reference |
|---------|--------|-------------|-----------|
| **ObjectWithStates** | Represent objects that can be in different states. | An object transitions between named states over its lifecycle (e.g. an order: pending → shipped → delivered). | `references/ObjectWithStates.md` |
| **Disposition** | Represent dispositions or capabilities of entities. | An entity has a latent capability that may or may not be realized (e.g. fragility, solubility, a skill). | `references/Disposition.md` |

### Miscellaneous

| Pattern | Intent | When to Use | Reference |
|---------|--------|-------------|-----------|
| **Region** | Represent abstract or concrete regions (value spaces). | You need to model value spaces, quality regions, or continuous/discrete ranges (e.g. color space, temperature range). | `references/Region.md` |
| **Partition** | Partition a class into exhaustive, disjoint subclasses. | A class is divided into non-overlapping categories that together cover the whole class. | `references/Partition.md` |
| **ActivitySpecification** | Represent specifications of activities. | You need to describe what an activity should do (its specification) separately from actual activity instances. | `references/ActivitySpecification.md` |
| **EEP** | Executor-Execution-Procedure: link who does it, the doing, and the specification. | You need the triad of an executor (who), an execution (the act), and a procedure (the plan/spec). | `references/EEP.md` |
| **CommunicationEvent** | Represent communication events between agents. | You need to model messages, conversations, or information exchange between parties. | `references/CommunicationEvent.md` |

---

## Pattern Selection Guide

When uncertain which pattern to use, consider these common modeling problems:

| Modeling Problem | Recommended Pattern(s) |
|-----------------|----------------------|
| "X is part of Y" (transitive) | **PartOf** |
| "X is a component of Y" (designed system) | **Componency** |
| "X is made of Y" (material constitution) | **Constituency** |
| Parts change over time | **TimeIndexedPartOf** |
| Groups, teams, collections | **CollectionEntity**, **Bag**, **List**, **Set** |
| People/agents play roles | **AgentRole**, **TimeIndexedPersonRole** |
| Objects play roles | **Objectrole** |
| Delegation or proxy | **ActingFor** |
| Something participates in an event | **Participation**, **ParticipantRole** |
| Multiple participants in one event | **Co-participation** |
| Ordering, before/after | **Sequence** |
| Events with who/what/when/where | **EventCore** |
| Plans and their execution | **BasicPlan**, **BasicPlanExecution** |
| Task assignment and tracking | **TaskExecution** |
| Workflow branching/ordering | **Controlflow** |
| Entity changes state | **ObjectWithStates**, **Transition** |
| Entity moves location | **Move** |
| Raw material → product | **MaterialTransformation** |
| Relation involving 3+ entities | **Situation**, **NaryParticipation**, **NaryRelationOWL2** |
| Classification changes over time | **TimeIndexedClassification** |
| Concept vs. its instances | **IntensionExtension**, **Classification** |
| Abstract info vs. physical copy | **InformationRealization** |
| Recurring events/schedules | **RecurrentEventSeries**, **PeriodicInterval** |
| Paths/tracks through space-time | **Trajectory** |
| Capability/potential | **Disposition** |
| Tagging or annotation | **Tagging** |
| Data lineage/history | **Provenance** |

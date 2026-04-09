# EEP (Execution-Executor-Procedure)

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:EEP
**OWL Building Block:** https://w3id.org/eep

## Intent

To represent executions made by executors that implement procedures. Executions are events like observations or actuations. Executors are systems like sensors or actuators that produce executions. Executors implement procedures to carry out their goals. Executions and executors are taken over features of interest and their intrinsic properties/qualities.

## Competency Questions

1. What are the observations/actuations performed by a given procedure?
2. What are the observations/actuations performed by a given sensor/actuator?
3. What are the procedures implemented by a given sensor/actuator?
4. What are the features of interest on a given observation/actuation?
5. What are the properties/qualities sensed/actuated by a given observation/actuation?
6. What are the features of interest of a given sensor/actuator?
7. What are the properties/qualities sensed/actuated by a given executor?

## Domains

- Building and Construction
- General
- IoT / Sensor Networks

## Solution Description

The EEP ODP imports the AffectedBy ODP (https://w3id.org/affectedBy), that involves classes for Features of Interest and their intrinsic Properties/Qualities.

The EEP ODP is an adaptation of the Procedure Execution Ontology (PEP) from the SEAS ontology, which in turn is a generalization of the Observation-Sensor-Procedure and Actuation-Actuator-Procedure patterns used in the SOSA and SSN ontologies.

The class Execution and its three functional object properties (eep:madeBy, eep:usedProcedure, eep:onQuality) form the backbone of the ODP. An execution jointly with their three object values can be considered as an n-ary relationship. Since every quality belongs to a unique feature of interest, a feature of interest is also involved in the n-ary relationship.

The remaining properties (eep:implements, eep:hasFeatureOfInterest, eep:forQuality, eep:forFeatureOfInterest) are defined using property chain axioms based on the functional properties.

## Elements

### Classes

- **Execution** — An event (observation, actuation, etc.) made by an executor using a procedure, concerning a quality of a feature of interest.
- **Executor** — A system (sensor, actuator, etc.) that produces executions by implementing procedures.
- **Procedure** — A method or workflow implemented by an executor to carry out executions.
- **FeatureOfInterest** (from AffectedBy) — The real-world entity whose qualities are being observed/actuated.
- **Quality** (from AffectedBy) — An intrinsic property of a feature of interest.

### Object Properties

- **madeBy** (functional) — Links an execution to its executor.
- **usedProcedure** (functional) — Links an execution to the procedure used.
- **onQuality** (functional) — Links an execution to the quality/property concerned.
- **implements** (derived via property chain) — Links executors to the procedures they implement.
- **hasFeatureOfInterest** (derived via property chain) — Links executions to features of interest.
- **forQuality** (derived via property chain) — Links executors to the qualities they sense/actuate.
- **forFeatureOfInterest** (derived via property chain) — Links executors to the features of interest they work with.

## Consequences

Axioms included in the EEP ODP provide inferences that allow answering the competency questions properly, solving some weaknesses of the SOSA/SSN ontologies. Only triples about the four functional object properties (madeBy, usedProcedure, onQuality, and aff:belongsTo) need to be asserted; the remaining triples are inferred by the property axioms.

## Scenarios

No explicit scenarios provided. Typical applications include:
- IoT sensor networks recording temperature observations.
- Building automation systems actuating HVAC controls.
- Environmental monitoring with multiple sensor types and procedures.

## Related Patterns

- **AffectedBy** — Component pattern providing FeatureOfInterest and Quality.
- **Observation** — Simpler observation pattern.
- **SOSA/SSN** — W3C Semantic Sensor Network ontology (EEP generalizes its patterns).
- **PEP (Procedure Execution)** — SEAS ontology pattern from which EEP is adapted.

## Additional Information

- Submitted by: Iker Esnaola-Gonzalez
- Known Uses: https://w3id.org/eepsa
- Reengineered from: PEP (https://w3id.org/pep/pep-1.1), SOSA (http://www.w3.org/ns/sosa/), SSN (http://www.w3.org/ns/ssn/), DUL (http://www.ontologydesignpatterns.org/ont/dul/DUL.owl)
- Has Components: AffectedBy

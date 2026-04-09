# CommunicationEvent

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:CommunicationEvent
**OWL Building Block:** http://www.ontology.se/odp/content/owl/CommunicationEvent.owl

## Intent

To model communication events, such as phone calls, e-mails and meetings, their involved parties and the roles and relations of the parties in the context of the communication events.

## Competency Questions

- What is the status of this event?
- What is the purpose of this communication?
- What are the valid contact mechanisms for this communication?
- What roles did the different parties have in this communication event?
- What are the roles of the parties involved in this relationship?
- What was the contact mechanism used for this communication?
- When did this communication event take place?
- In what relationship context did this communication take place?

## Domains

- Organization
- Business
- Planning
- Participation
- Product Development

## Solution Description

The pattern introduces a specialization of the Participation pattern, where parties hold different roles when participating in communication events. Communication events take place within the context of party relationships, have purposes, use contact mechanisms, and involve parties in specific roles.

## Elements

### Classes

- **CommunicationEvent** — An instance of communication, e.g. a phone call, a meeting, or a conference.
- **Party** — A physical or juridical party, e.g. person or organization.
- **ContactMechanism** — The medium for the communication.
- **CommunicationPurpose** — The purpose or goal of the communication event.
- **CommunicationEventStatus** — The status of an event, e.g. suspended, started, ongoing, planned, proposed.
- **CommunicationEventRole** — The role that this event plays for a specific party, e.g. a conference has the role of transmitting research results for a presenter while generating income for organizers.
- **CommunicationEventPartyRole** — The role of a specific party for a specific communication event, e.g. in this particular meeting John is the chairman.
- **PartyRole** — The role of a party in a relationship, e.g. in a sales relationship one party has the customer role and the other party the provider role.
- **PartyRelationship** — A state of things where two or more parties are involved through different roles, e.g. a buyer-seller relation.
- **RelationshipPartyRole** — The role of a specific party in a relationship, e.g. in this particular buyer-seller relationship company x is the seller.
- **EventDuration** — The time duration of a communication event.
- **RelationshipDuration** — The time duration of a relationship.

#### Communication Type Subclasses

- **EmailCommunication**
- **PhoneCommunication**
- **FaceToFaceCommunication**
- **WebSiteCommunication**
- **LetterCorrespondence**
- **FaxCommunication**

### Object Properties

- **eventHasPurpose** — Relates a communication event to its purpose.
- **purposeOfEvent** — Inverse of eventHasPurpose.
- **throughMedium** — Relates a communication event to the contact mechanism used.
- **mediumOf** — Inverse of throughMedium.
- **hasEventStatus** — Relates a communication event to its status.
- **statusOfEvent** — Inverse of hasEventStatus.
- **eventHasDuration** — Relates a communication event to its duration.
- **isDurationOfEvent** — Inverse of eventHasDuration.
- **eventIncludes** — Relates a communication event to included party roles.
- **eventRoleIncludedIn** — Inverse of eventIncludes.
- **communicationHasSetting** — All communications take place within some relationship between parties.
- **includesCommunication** — Relates a relationship to the communications within it.
- **partyInEvent** — Relates a party to a communication event.
- **inCommunicationEvent** — Inverse of partyInEvent.
- **roleOfParty** — Relates a communication event party role to the party.
- **roleOfEvent** — Relates a communication event party role to the event.
- **partyParticipating** — Relates a party to its participation.
- **partyInRelationship** — Relates a party to a relationship.
- **inRelationship** — Relates a party role to a relationship.
- **roleInRelationship** — Relates a relationship party role to the relationship.
- **relationshipIncludes** — Relates a relationship to its party roles.
- **relationshipHasDuration** — Relates a relationship to its duration.
- **isDurationOfRelationship** — Inverse of relationshipHasDuration.
- **hasValidContactMechanism** — Relates roles of communication events to their valid mediums, e.g. contracts may only be sent by letter or fax.
- **isValidContactMechanismFor** — Inverse of hasValidContactMechanism.

### Data Properties

- **eventStartTime** — Start time of a communication event.
- **eventEndTime** — End time of a communication event.
- **relationshipStartTime** — Start time of a relationship.
- **relationshipEndTime** — End time of a relationship.

### Individuals

- **e-mail** (ContactMechanism)
- **phone** (ContactMechanism)
- **face-to-face** (ContactMechanism)
- **web-site** (ContactMechanism)
- **letter** (ContactMechanism)
- **fax** (ContactMechanism)

## Consequences

- Pattern includes a set of standard communication mechanisms, but can be extended.
- The pattern does not take into account time-indexed participation in relationships, nor time-indexed participation in communication events. All parties are assumed to participate during the whole duration of relationships and events.

## Scenarios

- A sales call between John at company x and Mary at company y took place on January 7, 2009. In the call, John had the role of seller and Mary the role of buyer. The call was made in the context of the long-term relation between companies x and y, where x is the subcontractor of y. The purpose of the call was to agree on a price for a particular order item.
- In today's board meeting, John was elected chairman of the meeting, and Michael was appointed to take the minutes. The meeting involved 6 people: 5 elected members of the board and one invited external party. The purpose was to decide on the price of a new product. The participants did not agree, so the meeting was suspended and will continue tomorrow.

## Related Patterns

- **ParticipantRole** — Parent pattern and component.
- **TimeInterval** — Component pattern for temporal aspects.

## Additional Information

- Submitted by: Eva Blomqvist
- Reengineered from: Data model pattern called "communication events."
- Has Components: ParticipantRole, TimeInterval
- Specialization Of: ParticipantRole

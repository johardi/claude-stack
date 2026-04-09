# Tagging

**Source:** http://ontologydesignpatterns.org/index.php/Submissions:Tagging
**OWL Building Block:** http://ontologydesignpatterns.org/cp/owl/tagging.owl

## Intent

To represent a tagging situation, in which someone uses a term, from a list of a folksonomy, to tag something (or the content of something). We might also want to represent the time and the polarity of the tagging.

## Competency Questions

- Who is tagging (the content of) what by using what term from what folksonomy?
- Which polarity has the tagging?

## Domains

- General
- Web 2.0
- Document Management

## Solution Description

The Tagging pattern exploits the Situation pattern in order to encode Gruber's definition that has tagging as a relation between an agent, a tag from a folksonomy, a content tagged, and a polarity. A Tag is classified as a linguistic object that is used in the context of a Tagging Situation, which also involves a (tagged) Entity, an Agent, and a Folksonomy.

## Elements

### Classes

- **Tagging** (implied from Situation) — The tagging situation linking agent, tag, tagged entity, and folksonomy.
- **Tag** (implied) — A linguistic object used as a tag within the tagging situation.
- **Folksonomy** (implied) — A collection or vocabulary from which tags are drawn.

### Object Properties

- **byAgent** — Relates a tagging to the agent performing the tagging.
- **isTaggingAgentIn** — Inverse; relates an agent to the tagging situations they participate in.
- **usingTag** — Relates a tagging to the tag term used.
- **isTagUsedIn** — Inverse; relates a tag to the tagging situations in which it is used.

## Consequences

We are able to represent data about tagging activities from web 2.0 applications, from document annotation projects, or from RDFa documents.

## Scenarios

- A Flickr picture showing a leopard, tagged with the Tag "leopard."
- A Flickr picture showing a boy surfing with a sombrero hat, tagged with the Tag "cool."
- A Flickr picture tagged as "taken in Sicily."

## Related Patterns

- **Topic** — Topics are related to tagged content.
- **AgentRole** — Component pattern for agents in roles.
- **CollectionEntity** — Component pattern for collections.
- **IntensionExtension** — Component pattern for meaning of tags.
- **TimeIndexedSituation** — Parent pattern (Tagging is a specialization).

## Additional Information

- Submitted by: Aldo Gangemi
- Has Components: AgentRole, CollectionEntity, IntensionExtension
- Specialization Of: TimeIndexedSituation
- Based on: Tom Gruber's tagging ontology (FOL), formalized in OWL by Aldo Gangemi with pattern-based design.

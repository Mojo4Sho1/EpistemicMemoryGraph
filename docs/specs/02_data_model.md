# Core Data Model

## Purpose

Define v0 memory object types, minimum fields, and relationship primitives for durable and transient memory semantics.

## Normative Requirements

- `MUST` represent observations as immutable evidence objects.
- `MUST` model propositions as first-class claims with state/score metadata.
- `MUST` anchor graph structure on entities and explicit edge types.
- `MUST` include episode-level context for bounded task history.
- `SHOULD` keep ontology minimal in v0.
- `MAY` store graph semantics in relational tables for v0.

## Data Objects / Interfaces

- Observation minimum fields:
  - `observation_id`, `timestamp`, `source_id`, `source_type`, `source_independence_group`, `session_id`, `task_id`, `raw_payload`, `parsed_payload`, `ingest_status`
- Entity fields:
  - canonical name, class/type, aliases, timestamps, canonicality status
- Proposition fields:
  - text/structured form, status, confidence, support/contradiction weights, source-group count, recency, volatility, provenance summary
- Additional objects:
  - test, episode
- Minimum edge types:
  - `supports`, `contradicts`, `about`, `predicts`, `tested_by`, `derived_from`, `possible_same_as`, `supersedes`
- Canonical relational tables (v0 default):
  - `entities`, `propositions`, `edges`, `sources`, `belief_states`, `aliases`, `promotion_events`, `episodes`

## Policy Rules / Constraints

- Observation rows are append-only; updates are represented by new observations.
- Entity creation is low-cost; hard merge remains conservative.
- `possible_same_as` is the default identity ambiguity mechanism in v0.

## Edge Cases and Failure Modes

- Entity explosion if merge thresholds are too strict.
- Silent corruption if merges are too aggressive.
- Provenance breakage if proposition-observation linkage is incomplete.

## Open Questions

- Should proposition structured form be normalized in v0 or deferred to v0.2?
- Should episode schema include explicit retention class tags at launch?

## Traceability to `MASTER_DOC.md`

- Source sections: 7.1, 7.3, 8, 15.1
- Notes: Includes canonical object catalog and relational representation choice.

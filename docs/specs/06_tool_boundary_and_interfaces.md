# Tool Boundary and Interfaces

## Purpose

Define the LLM-to-system mutation boundary and initial tool proposal surface for controlled memory actions.

## Normative Requirements

- `MUST` treat all tool calls as proposals.
- `MUST` validate proposals through deterministic policy code before durable writes.
- `MUST` prevent direct LLM writes to canonical memory.
- `MUST` preserve provenance links for all durable mutations.
- `SHOULD` keep tool surface narrow in v0.
- `MAY` reject or downgrade proposals that violate policy constraints.

## Data Objects / Interfaces

- Initial tool surface:
  - `record_observation`
  - `create_or_link_entity_candidate`
  - `propose_proposition`
  - `attach_support`
  - `attach_contradiction`
  - `propose_test`
  - `execute_test_result_ingest`
  - `request_consolidation`
  - `archive_episode`
- Validation outcomes:
  - accepted proposal
  - rejected proposal with reason
  - transformed proposal (policy-normalized)

## Policy Rules / Constraints

- Policy layer owns scoring, transitions, promotion checks.
- Durable write path must be auditable and reproducible.
- Interface design must minimize accidental authority escalation.

## Edge Cases and Failure Modes

- Over-permissive tool validation can bypass governance guarantees.
- Under-specified errors can make LLM behavior unstable under rejection.
- Tool contract drift can decouple runtime behavior from policy tests.

## Open Questions

- Should tool proposal schemas be documented in separate machine-readable spec files now or after schema freeze?
- Should proposal rejection reasons use a fixed code enum in v0?

## Traceability to `MASTER_DOC.md`

- Source sections: 14, 10.4, 10.10, 15.2
- Notes: This file defines mutation authority boundaries.

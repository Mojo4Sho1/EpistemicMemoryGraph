# Tool Boundary and Interfaces

## Purpose

Define the LLM-to-system mutation boundary and initial tool proposal surface for controlled memory actions.

## Normative Requirements

- `MUST` treat all tool calls as proposals.
- `MUST` validate proposals through deterministic policy code before durable writes.
- `MUST` prevent direct LLM writes to canonical memory.
- `MUST` preserve provenance links for all durable mutations.
- `MUST` expose validation outcomes as one of:
  - accepted
  - rejected with fixed code and reason
  - transformed (policy-normalized proposal)
- `MUST` use fixed rejection code enum values:
  - `INVALID_TOOL_NAME`
  - `INVALID_PAYLOAD`
  - `MISSING_PROVENANCE`
  - `POLICY_VIOLATION`
  - `DIRECT_CANONICAL_WRITE_FORBIDDEN`
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
- Validation contracts:
  - proposal schema: `{tool_name, payload}`
  - rejection schema: `{code, reason}`
  - outcome schema: `{status, proposal?, rejection?}`

## Policy Rules / Constraints

- Policy layer owns scoring, transitions, promotion checks.
- Durable write path must be auditable and reproducible.
- Interface design must minimize accidental authority escalation.
- Rejection reasons should be deterministic and machine-loggable.

## Edge Cases and Failure Modes

- Over-permissive tool validation can bypass governance guarantees.
- Under-specified errors can make LLM behavior unstable under rejection.
- Tool contract drift can decouple runtime behavior from policy tests.

## Open Questions

- None for v0.1q proposal schema and rejection enum baseline.

## Traceability to `MASTER_DOC.md`

- Source sections: 14, 10.4, 10.10, 15.2
- Notes: This file defines mutation authority boundaries.

# Risks, Non-Goals, and Deferred Features

## Purpose

Capture known failure risks, explicit non-goals, and deferred features to protect v0 focus and interpretation quality.

## Normative Requirements

- `MUST` preserve explicit v0 non-goals as exclusion criteria.
- `MUST` track known failure modes as active design risks.
- `MUST` document deferred features without pulling them into v0 acceptance.
- `SHOULD` tie mitigations to minimal deterministic architecture choices.
- `MAY` expand risk catalog as new failure patterns appear.

## Data Objects / Interfaces

- Non-goal classes:
  - AGI architecture generalization
  - full scientific reasoning engine
  - embodied sensor fusion
  - multi-agent synchronization
  - learned trust calibration
  - aggressive ontology growth / hard auto-merge
  - production optimization/UI polish
- Deferred feature list maintained separately from milestone commitments.

## Policy Rules / Constraints

- Risk mitigation defaults: small scope, deterministic logic, heavy logging, ablation readiness.
- Deferred features must not leak into v0 Definition of Done.

## Edge Cases and Failure Modes

- Overdesign can cause schema sprawl before claim testing.
- False confidence from correlated sources can bypass naive scoring.
- Premature merges can silently corrupt large memory regions.
- Retrieval-centric evaluation may miss governance regressions.

## Open Questions

- Should each known risk get a mapped detection metric owner during implementation?
- Should deferred features be tagged with dependency prerequisites for post-v0 planning?

## Traceability to `MASTER_DOC.md`

- Source sections: 4.2, 19, 22, 24
- Notes: Guardrails for controlling scope and research validity.

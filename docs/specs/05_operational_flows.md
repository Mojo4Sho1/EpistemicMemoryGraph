# Operational Flows

## Purpose

Define end-to-end runtime workflows for intake, workspace updates, triggered testing, consolidation, and retrieval/reactivation.

## Normative Requirements

- `MUST` execute intake in this order: receive input -> record observations -> parse references/claims -> attach to workspace.
- `MUST` evaluate reinforcement/contradiction against existing propositions before spawning new candidates.
- `MUST` gate hypothesis testing on explicit trigger conditions.
- `MUST` consolidate at task boundaries or scheduled checkpoints.
- `SHOULD` load only relevant canonical subgraphs during reactivation.
- `MAY` defer selected tests when immediate execution cost is too high.

## Data Objects / Interfaces

- Triggered hypothesis testing loop interface:
  - rank competing propositions
  - choose cheapest discriminating action
  - execute via tool/deferred logic
  - ingest result as observation
  - recompute score/state
- Consolidation outputs:
  - promoted records
  - archived episode summary
  - retained unresolved items
  - discarded transient clutter

## Policy Rules / Constraints

- Hypothesis testing is not default for all inputs.
- Consolidation decisions must preserve provenance.
- Retrieval should optimize relevance and minimize unnecessary memory loading.

## Edge Cases and Failure Modes

- Excessive proposition spawning can overwhelm workspace quality.
- Missing test loop on high-impact uncertainty can degrade task correctness.
- Over-broad reactivation can cause context pollution and latency growth.

## Open Questions

- Should trigger conditions be codified as weighted scores or ordered hard rules in v0?
- Should consolidation include a fixed maximum unresolved-item carryover cap?

## Traceability to `MASTER_DOC.md`

- Source sections: 13.1, 13.2, 13.3, 13.4, 13.5, 6
- Notes: Use this as implementation guide for runtime orchestration.

# Operational Flows

## Purpose

Define end-to-end runtime workflows for intake, workspace updates, triggered testing, consolidation, and retrieval/reactivation.

## Normative Requirements

- `MUST` execute intake in this order: receive input -> record observations -> parse references/claims -> attach to workspace.
- `MUST` evaluate reinforcement/contradiction against existing propositions before spawning new candidates.
- `MUST` gate hypothesis testing on ordered hard trigger rules.
- `MUST` trigger testing when any condition is met:
  - action impact is `high` or `irreversible` and top-2 confidence gap < 0.15
  - proposition remains contested for >= 2 consecutive updates
  - unresolved contradiction count for same proposition >= 2
  - high-impact novelty with confidence in `[0.45, 0.70]` and < 2 support groups
- `MUST` suppress testing when action impact is low and estimated test cost exceeds bounded benefit score.
- `MUST` consolidate at task boundaries or every 25 new observations.
- `MUST` cap unresolved carryover at 20 propositions per task and archive overflow with reason code.
- `MUST` require accepted state plus freshness >= 0.35 for canonical promotion.
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
  - overflow archive reason code when carryover cap is exceeded

## Policy Rules / Constraints

- Hypothesis testing is not default for all inputs.
- Trigger logic uses deterministic ordered rules, not free-form weighted heuristics.
- Consolidation decisions must preserve provenance.
- Retrieval should optimize relevance and minimize unnecessary memory loading.

## Edge Cases and Failure Modes

- Excessive proposition spawning can overwhelm workspace quality.
- Missing test loop on high-impact uncertainty can degrade task correctness.
- Over-broad reactivation can cause context pollution and latency growth.
- Missing carryover caps can allow unresolved contradiction accumulation.

## Open Questions

- None for v0.1q trigger ordering, cadence, carryover cap, and promotion gate defaults.

## Traceability to `MASTER_DOC.md`

- Source sections: 13.1, 13.2, 13.3, 13.4, 13.5, 6
- Notes: Use this as implementation guide for runtime orchestration.

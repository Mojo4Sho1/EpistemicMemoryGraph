# Architecture Overview

## Purpose

Specify the three-layer memory architecture and end-to-end data movement boundaries for v0.

## Normative Requirements

- `MUST` implement three distinct layers:
  - immutable observation log
  - transient epistemic workspace
  - canonical long-term memory graph
- `MUST` ingest all external input as observations before interpretation.
- `MUST` keep workspace transient and high-churn.
- `MUST` treat canonical memory as policy-gated durable state.
- `SHOULD` keep workspace and canonical layers aligned on logical object types.
- `MAY` reactivate relevant canonical subgraphs into workspace for new tasks.

## Data Objects / Interfaces

- Layer contracts:
  - observation log: append-only evidence system of record
  - workspace: task/session-scoped active uncertainty graph
  - canonical graph: stabilized entities/propositions/episodes
- Flow anchors:
  - intake -> workspace update -> optional test loop -> consolidation -> later reactivation

## Policy Rules / Constraints

- LLM proposals pass through deterministic policy code.
- Direct model mutation of canonical memory is prohibited.
- Consolidation decides promote/archive/discard outcomes.

## Edge Cases and Failure Modes

- Leaky boundary between workspace and canonical memory can corrupt durable state.
- Missing workspace pruning can increase stale clutter and conflict load.
- Over-eager promotion can reduce contradiction resilience.

## Open Questions

- Should checkpoint cadence for consolidation be fixed or task-adaptive in v0?
- Should workspace eviction thresholds be configurable by domain volatility at v0 launch?

## Traceability to `MASTER_DOC.md`

- Source sections: 6, 7, 13.4, 13.5, 15.1
- Notes: Focused on layer responsibilities and system boundaries.

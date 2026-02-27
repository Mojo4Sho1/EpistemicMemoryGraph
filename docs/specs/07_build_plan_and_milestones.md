# Build Plan and Milestones

## Purpose

Translate v0 implementation sequencing into a practical build roadmap with dependency-aware milestones.

## Normative Requirements

- `MUST` implement persistence and policy boundary before higher-level agent behavior.
- `MUST` prioritize schema/policy freeze before benchmark expansion.
- `MUST` complete policy correctness suite before baseline comparison claims.
- `SHOULD` keep milestone outputs testable and independently verifiable.
- `MAY` split milestones into smaller tracked tasks if sequencing is preserved.

## Data Objects / Interfaces

- Default technical choices:
  - SQLite for storage
  - in-memory Python workspace keyed by task/session
  - relational graph semantics
  - deterministic weighted heuristic scoring
  - conservative identity with alias + `possible_same_as`
- Milestone sequence:
  - schema/constants freeze
  - observation + persistence
  - workspace
  - scoring/transitions
  - identity handling
  - tool boundary
  - consolidation/archival
  - policy tests
  - baselines
  - first benchmark/end-to-end trials

## Policy Rules / Constraints

- Do not claim governance gains before ablations/baselines are operational.
- Architecture should remain minimal until core claim signal is established.

## Edge Cases and Failure Modes

- Building end-to-end harness before policy correctness can hide core defects.
- Delaying logging schema can block reliable result interpretation.
- Skipping dependency ordering can create costly refactors.

## Open Questions

- Should milestone completion require explicit sign-off checklists in repo issues?
- Should benchmark harness scaffolding begin in parallel with policy tests or strictly after?

## Traceability to `MASTER_DOC.md`

- Source sections: 15.1, 15.2, 15.3, 23
- Notes: Roadmap-oriented derivative spec for execution planning.

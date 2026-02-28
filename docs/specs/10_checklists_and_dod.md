# Checklists and Definition of Done

## Purpose

Define completion criteria and implementation checklists that gate v0 claims and release readiness.

## Normative Requirements

- `MUST` maintain project checklists for framing, policy, data model, architecture, evaluation, and research hygiene.
- `MUST` meet v0 Definition of Done criteria before claiming successful prototype completion.
- `MUST` verify that policy enforcement is deterministic and code-level, not prompt-level.
- `MUST` require policy correctness micro-suite pass rate of 100%.
- `MUST` require reproducible stress benchmark artifacts using the frozen artifact schema.
- `MUST` require baseline-comparison claim thresholds:
  - >= 10% relative improvement on >= 3 policy metrics versus raw-log baseline
  - <= 3 absolute percentage-point degradation in task success versus raw-log baseline
- `MUST` require long-horizon interpretable benefit on at least one governance metric plus one continuity metric within the same task family.
- `SHOULD` treat checklist completion as objective evidence for milestone closure.
- `MAY` add checklist sub-items if traceability to source criteria is maintained.

## Data Objects / Interfaces

- Master checklist categories:
  - project framing
  - policy freeze
  - data model freeze
  - runtime architecture freeze
  - evaluation definitions
  - research hygiene artifacts
- Definition of Done anchors:
  - end-to-end functionality of three layers
  - policy test pass on micro-scenarios
  - reproducible stress benchmark
  - measurable governance improvement over at least one naive baseline
  - interpretable gain in at least one long-horizon task family
  - sufficient logging/artifacts for failure analysis

## Policy Rules / Constraints

- Claims of success require both functional and evaluative criteria.
- Benchmark reproducibility and artifact quality are mandatory for completion.
- Directional improvement without quantified threshold does not satisfy v0.1q claim criteria.

## Edge Cases and Failure Modes

- Partial completion with missing ablations can lead to weak causal claims.
- Missing reproducibility policy undermines comparability across runs.
- Passing task success with weak governance metrics can mask core failure.

## Open Questions

- None for v0.1q DoD thresholds.

## Traceability to `MASTER_DOC.md`

- Source sections: 20, 21, 23
- Notes: This file is the release gate and audit checklist source.

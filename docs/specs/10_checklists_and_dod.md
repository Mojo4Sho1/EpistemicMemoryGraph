# Checklists and Definition of Done

## Purpose

Define completion criteria and implementation checklists that gate v0 claims and release readiness.

## Normative Requirements

- `MUST` maintain project checklists for framing, policy, data model, architecture, evaluation, and research hygiene.
- `MUST` meet v0 Definition of Done criteria before claiming successful prototype completion.
- `MUST` verify that policy enforcement is deterministic and code-level, not prompt-level.
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

## Edge Cases and Failure Modes

- Partial completion with missing ablations can lead to weak causal claims.
- Missing reproducibility policy undermines comparability across runs.
- Passing task success with weak governance metrics can mask core failure.

## Open Questions

- Should Definition of Done require a minimum threshold delta versus baseline, or only directional improvement in v0?
- Should checklist state be mirrored into machine-readable tracking (for example, YAML) in the next pass?

## Traceability to `MASTER_DOC.md`

- Source sections: 20, 21, 23
- Notes: This file is the release gate and audit checklist source.

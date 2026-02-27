# Evaluation and Metrics

## Purpose

Define staged evaluation methodology, baseline comparisons, ablation plan, and logging requirements for evidence-based claims.

## Normative Requirements

- `MUST` run staged evaluation in order: policy correctness -> governance stress -> baseline comparison -> end-to-end study.
- `MUST` include required ablations to isolate governance components.
- `MUST` record machine-readable run artifacts with configs, seeds, timestamps, and system version.
- `MUST` log proposition transitions with triggering evidence.
- `SHOULD` quantify calibration, contradiction recovery, and stale-belief handling.
- `MAY` add supplementary metrics if they do not replace required core metrics.

## Data Objects / Interfaces

- Stage 1: deterministic micro-scenario policy tests
- Stage 2: governance stress benchmark suite
- Stage 3: baselines:
  - context window only
  - raw text log retrieval
  - summary-only memory
  - simple key-value memory
  - graph memory without governance
  - full governed system
- Stage 4: longer-horizon task families
- Required metric groups:
  - policy metrics
  - identity metrics
  - memory health metrics
  - task metrics

## Policy Rules / Constraints

- Evaluation must target governance quality, not only retrieval strength.
- Ablation outcomes are required for causal interpretation of gains.
- Reproducibility hygiene is mandatory for comparisons.

## Edge Cases and Failure Modes

- Synthetic-only tuning can overfit thresholds and weaken generalization.
- Missing artifact schema can break post-hoc failure analysis.
- Baseline implementations that differ in unrelated dimensions can bias conclusions.

## Open Questions

- Should confidence calibration be reported with reliability diagrams in v0 artifacts?
- Should stage-gate criteria include minimum statistical power targets for benchmark runs?

## Traceability to `MASTER_DOC.md`

- Source sections: 16, 17, 18, 21
- Notes: Evaluation contract for claims and benchmarking discipline.

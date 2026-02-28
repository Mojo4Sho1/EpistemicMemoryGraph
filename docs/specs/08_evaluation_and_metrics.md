# Evaluation and Metrics

## Purpose

Define staged evaluation methodology, baseline comparisons, ablation plan, and logging requirements for evidence-based claims.

## Normative Requirements

- `MUST` run staged evaluation in order: policy correctness -> governance stress -> baseline comparison -> end-to-end study.
- `MUST` include required ablations to isolate governance components.
- `MUST` record machine-readable run artifacts with configs, seeds, timestamps, and system version.
- `MUST` log proposition transitions with triggering evidence and deterministic rule ids.
- `MUST` enforce Stage 1 pass criterion of 100% expected deterministic transitions.
- `MUST` run Stage 2 stress with 5 fixed seeds and identical scenario bundles per system.
- `MUST` enforce Stage 3 fairness parity across systems:
  - same model snapshot
  - same prompt template family
  - same tool availability
  - same token budget
  - same wall-clock timeout
  - same seed set
- `MUST` enforce Stage 3 minimum claim threshold:
  - >= 10% relative improvement on >= 3 policy metrics vs raw-log baseline
  - task success degradation <= 3 absolute percentage points vs raw-log baseline
- `MUST` require Stage 4 interpretable benefit to include improvement on one governance metric and one continuity metric within the same task family.
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
- Required artifact directory template:
  - `artifacts/{date}_{git_sha}_{system}_{seed}/`
- Required files:
  - `manifest.json`
  - `config_snapshot.yaml`
  - `transitions.jsonl`
  - `consolidation_events.jsonl`
  - `scenario_results.jsonl`
  - `metrics_summary.json`

## Policy Rules / Constraints

- Evaluation must target governance quality, not only retrieval strength.
- Ablation outcomes are required for causal interpretation of gains.
- Reproducibility hygiene is mandatory for comparisons.
- Manifest must include model id, git SHA, seed, timestamp, config hash, scenario bundle hash, and reproducibility hash.

## Edge Cases and Failure Modes

- Synthetic-only tuning can overfit thresholds and weaken generalization.
- Missing artifact schema can break post-hoc failure analysis.
- Baseline implementations that differ in unrelated dimensions can bias conclusions.

## Open Questions

- Confidence calibration visualizations are optional in v0.1q; scalar metrics remain required.
- Minimal smoke tests and developer probe scripts are intentionally deferred until `workspace-update-boundary-v0q-v0` is implemented.

## Traceability to `MASTER_DOC.md`

- Source sections: 16, 17, 18, 21
- Notes: Evaluation contract for claims and benchmarking discipline.

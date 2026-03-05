# Evaluation and Metrics

## Purpose

Define staged evaluation methodology, baseline comparisons, ablation plan, and logging requirements for evidence-based claims.

## Normative Requirements

- `MUST` keep nomenclature hierarchy as `sub-task -> task -> stage -> phase` for evaluation planning artifacts.
- `MUST` treat completed legacy Stage 1-4 evaluation work as Phase 1 for continuity, without renumbering historical artifacts.
- `MUST` execute Phase 2 (small/edge uplift) with stage IDs `P2-S1`, `P2-S2A`, `P2-S2B`, `P2-S3`, and `P2-S4`.
- `MUST` enforce `P2-S4` decision gate status as one of `OPEN`, `LOCKED_PROCEED`, or `LOCKED_DEFER` in handoff docs.
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
- `MUST` enforce Phase 2 statistical gate criteria for key claims:
  - 95% bootstrap confidence interval on paired deltas
  - paired nonparametric test
  - effect-size threshold gate
- `MUST` emit a human-readable markdown findings report (`findings_summary.md`) for each Phase 2 experiment bundle.
- `MUST` enforce non-China-origin compliance policy for all execution environments in the active Phase 2 cycle.
- `SHOULD` quantify calibration, contradiction recovery, and stale-belief handling.
- `MAY` add supplementary metrics if they do not replace required core metrics.

## Data Objects / Interfaces

- Phase mapping:
  - Phase 1: legacy Stage 1-4 execution and evidence (already completed)
  - Phase 2: local-first small/edge model uplift with stage IDs `P2-S1`, `P2-S2A`, `P2-S2B`, `P2-S3`, `P2-S4`
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
- Phase 2 local screening model panel (`P2-S2A`):
  - `meta_llama3.2_1b_instruct`
  - `google_gemma3_1b`
  - `microsoft_phi4_mini`
- Phase 2 policy-ablation stage (`P2-S2B`) applies required policy-mechanism ablations to top local performers before any server-scale runs.
- Required artifact directory template:
  - `artifacts/{date}_{git_sha}_{system}_{seed}/`
- Required files:
  - `manifest.json`
  - `config_snapshot.yaml`
  - `transitions.jsonl`
  - `consolidation_events.jsonl`
  - `scenario_results.jsonl`
  - `metrics_summary.json`
  - `findings_summary.md`

## Policy Rules / Constraints

- Evaluation must target governance quality, not only retrieval strength.
- Ablation outcomes are required for causal interpretation of gains.
- Reproducibility hygiene is mandatory for comparisons.
- Manifest must include model id, git SHA, seed, timestamp, config hash, scenario bundle hash, and reproducibility hash.
- Manifest should include model compliance metadata (`provider_org`, `origin_country`, `compliance_class`) for Phase 2 local-screening traceability.
- Phase 2 progression beyond `P2-S4` is blocked until gate status is explicitly locked in handoff docs.

## Edge Cases and Failure Modes

- Synthetic-only tuning can overfit thresholds and weaken generalization.
- Missing artifact schema can break post-hoc failure analysis.
- Baseline implementations that differ in unrelated dimensions can bias conclusions.
- Missing findings summary reports can prevent paper-quality interpretation traceability.

## Open Questions

- Confidence calibration visualizations are optional in v0.1q; scalar metrics remain required.
- Minimal smoke tests and developer probe scripts are intentionally deferred until `workspace-update-boundary-v0q-v0` is implemented.

## Traceability to `MASTER_DOC.md`

- Source sections: 16, 17, 18, 21
- Notes: Evaluation contract for claims and benchmarking discipline.

# Task Queue

LAST_UPDATED: 2026-03-05
QUEUE_PHASE: implementation
QUEUE_POLICY: Keep one `READY: YES` task at a time; all other staged tasks remain `READY: NO`.
PHASE_MAPPING:
- Phase 1: legacy Stage 1-4 evaluation work (completed; historical labels retained).
- Phase 2: small/edge uplift work using stage IDs `P2-S1`, `P2-S2A`, `P2-S2B`, `P2-S3`, `P2-S4`.

## Queue Entry 1
TASK_ID: phase2-small-edge-uplift-v0
MILESTONE: Phase 2 Stage P2-S1
OBJECTIVE: Implement model/backend integration surfaces and fairness-lock verification for Phase 2 small/edge uplift.
PREREQUISITES:
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
- `configs/eval_v0q.yaml`
- `docs/specs/08_evaluation_and_metrics.md`
PRIMARY_DOCS:
- `docs/specs/08_evaluation_and_metrics.md`
- `docs/specs/10_checklists_and_dod.md`
- `MASTER_DOC.md` sections 16-17
TARGET_FILES:
- `src/eval/`
- `tests/test_eval_phase2.py`
- `configs/eval_v0q.yaml`
- `docs/templates/EXPERIMENT_FINDINGS_TEMPLATE.md`
- `docs/handoff/`
ACCEPTANCE_CRITERIA:
- Phase 2 runner scaffolding exists and fairness contract is enforced.
- Phase 2 statistical gates and findings report schema/template are implemented and tested.
- `P2_GATE_STATUS` appears in handoff continuity docs and defaults to `OPEN`.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q tests/test_eval_phase2.py tests/test_eval_artifacts.py tests/test_eval_fairness.py`
- `conda run -n emg python -m pytest -q`
- `conda run -n emg python -m mypy src tests`
- `conda run -n emg python -m ruff check src tests`
READY: NO

## Queue Entry 2
TASK_ID: phase2-local-small-screening-v0
MILESTONE: Phase 2 Stage P2-S2A
OBJECTIVE: Execute local non-China 3-model screening scenario-family runs under shared fairness controls.
PREREQUISITES:
- Queue Entry 1 complete
- Phase 2 runner interfaces/tests stable
PRIMARY_DOCS:
- `docs/specs/08_evaluation_and_metrics.md`
- `configs/eval_v0q.yaml`
TARGET_FILES:
- `src/eval/`
- `configs/eval_v0q.yaml`
- `tests/test_eval_phase2.py`
- `tests/test_eval_fairness.py`
- `artifacts/`
- `docs/handoff/OVERVIEW_CHECKLIST.md`
ACCEPTANCE_CRITERIA:
- Runs emitted for all three locked local screening models with required artifacts.
- Compliance metadata and non-China policy enforcement are validated in deterministic tests.
- Fairness parity remains satisfied for compared systems per model.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q tests/test_eval_phase2.py tests/test_eval_artifacts.py tests/test_eval_fairness.py`
- `rg "meta_llama3.2_1b_instruct|google_gemma3_1b|microsoft_phi4_mini" configs/eval_v0q.yaml`
- `rg "provider_org|origin_country|compliance_class" src/eval/phase2_edge.py`
READY: YES

## Queue Entry 3
TASK_ID: phase2-local-policy-ablations-v0
MILESTONE: Phase 2 Stage P2-S2B
OBJECTIVE: Execute local policy-mechanism ablations for top local screening performers before any server-scale model execution.
PREREQUISITES:
- Queue Entry 2 complete
- Local screening artifacts available
PRIMARY_DOCS:
- `docs/specs/08_evaluation_and_metrics.md`
- `configs/eval_v0q.yaml`
TARGET_FILES:
- `src/eval/phase2_edge.py`
- `tests/test_eval_phase2.py`
- `artifacts/`
- `docs/handoff/OVERVIEW_CHECKLIST.md`
ACCEPTANCE_CRITERIA:
- Required ablations are executed in configured order for selected local models.
- Causal-delta summaries are recorded for each ablation/model combination.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q tests/test_eval_phase2.py`
- `rg "policy_ablations|P2-S2B" configs/eval_v0q.yaml src/eval/phase2_edge.py`
READY: NO

## Queue Entry 4
TASK_ID: phase2-small-edge-analysis-v0
MILESTONE: Phase 2 Stage P2-S3
OBJECTIVE: Complete statistical analysis and human-readable findings reports for Phase 2 bundles.
PREREQUISITES:
- Queue Entry 3 complete
- Phase 2 artifact bundles available
PRIMARY_DOCS:
- `docs/specs/08_evaluation_and_metrics.md`
- `docs/templates/EXPERIMENT_FINDINGS_TEMPLATE.md`
TARGET_FILES:
- `src/eval/stats.py`
- `src/eval/reporting.py`
- `artifacts/`
- `docs/handoff/OVERVIEW_CHECKLIST.md`
ACCEPTANCE_CRITERIA:
- CI + paired nonparametric + effect-size gates computed for required metrics.
- `findings_summary.md` exists for every Phase 2 model bundle.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q tests/test_eval_phase2.py`
- `rg "Decision Gate Status" artifacts -g "findings_summary.md"`
READY: NO

## Queue Entry 5
TASK_ID: phase2-decision-gate-v0
MILESTONE: Phase 2 Stage P2-S4
OBJECTIVE: Resolve Phase 2 decision gate and lock continuation status without auto-progressing into any subsequent phase.
PREREQUISITES:
- Queue Entry 4 complete
- Phase 2 findings summaries reviewed
PRIMARY_DOCS:
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
- `docs/handoff/OVERVIEW_CHECKLIST.md`
TARGET_FILES:
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
- `docs/handoff/TASK_QUEUE.md`
- `docs/handoff/OVERVIEW_CHECKLIST.md`
- `docs/handoff/DECISION_LOG.md`
ACCEPTANCE_CRITERIA:
- `P2_GATE_STATUS` is locked to `LOCKED_PROCEED` or `LOCKED_DEFER` with evidence.
- Queue continuity reflects gate outcome and no automatic post-Phase-2 task activation.
VALIDATION_COMMANDS:
- `rg "^P2_GATE_STATUS:" docs/handoff/CURRENT_STATUS.md`
- `rg "phase2-decision-gate-v0|LOCKED_PROCEED|LOCKED_DEFER" docs/handoff/*`
READY: NO

## Queue Update Rules
- Keep one and only one queue entry with `READY: YES`.
- `CURRENT_STATUS.md:ACTIVE_QUEUE_TASK_ID` must match the `TASK_ID` of the `READY: YES` queue entry.
- `NEXT_TASK.md:TASK_ID` must match `CURRENT_STATUS.md:NEXT_TASK_ID` and `ACTIVE_QUEUE_TASK_ID`.
- Keep queue entries concise and operational; avoid narrative logs.

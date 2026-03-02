# Task Queue

LAST_UPDATED: 2026-03-02
QUEUE_PHASE: implementation
QUEUE_POLICY: Keep one `READY: YES` task at a time; all other staged tasks remain `READY: NO`.

## Queue Entry 1
TASK_ID: consolidation-archival-determinism-v0
MILESTONE: M7
OBJECTIVE: Finish deterministic consolidation cadence/carryover/promotion boundary evidence and close M7.
PREREQUISITES:
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
- `docs/handoff/OVERVIEW_CHECKLIST.md`
- `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md`
PRIMARY_DOCS:
- `docs/specs/05_operational_flows.md`
- `docs/specs/03_policy_and_state_machine.md`
- `docs/specs/04_scoring_and_trust.md`
- `docs/specs/10_checklists_and_dod.md`
TARGET_FILES:
- `src/workspace/consolidation.py`
- `tests/test_workspace_consolidation.py`
- `tests/TEST_INDEX.md`
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
- `docs/handoff/OVERVIEW_CHECKLIST.md`
ACCEPTANCE_CRITERIA:
- Deterministic cadence boundary tests include exact 25-observation trigger behavior and rule-id checks.
- Carryover cap tests enforce deterministic retained ordering and overflow reason-code output.
- Promotion eligibility tests enforce `accepted` + freshness threshold boundary behavior.
- Quality gates pass and handoff docs stay continuous.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q tests/test_workspace_consolidation.py`
- `conda run -n emg python -m pytest -q`
- `conda run -n emg python -m mypy src tests`
- `conda run -n emg python -m ruff check src tests`
- `rg "^OWNER_CHECK_IDS:|^SPEC_MUST_IDS:" docs/handoff/NEXT_TASK.md`
READY: NO

## Queue Entry 2
TASK_ID: identity-alias-possible-same-as-v0
MILESTONE: M5
OBJECTIVE: Implement conservative identity handling with alias linking and `possible_same_as` behavior plus deterministic tests/metrics hooks.
PREREQUISITES:
- Queue Entry 1 complete
- `docs/specs/02_data_model.md` reviewed
- `docs/specs/09_risks_non_goals_deferred.md` reviewed
PRIMARY_DOCS:
- `docs/specs/02_data_model.md`
- `docs/specs/09_risks_non_goals_deferred.md`
- `docs/specs/10_checklists_and_dod.md`
TARGET_FILES:
- `src/core/models.py`
- `src/core/constants.py`
- `src/workspace/update.py`
- `tests/test_core_models.py`
- `tests/test_workspace_update.py`
- `tests/TEST_INDEX.md`
ACCEPTANCE_CRITERIA:
- Identity ambiguity is represented with alias + `possible_same_as` behaviors.
- Deterministic tests cover duplicate-entity and false-merge guardrails.
- Checklist rows `C20-DATA-03` and `C20-DATA-04` advance with evidence.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q tests/test_core_models.py tests/test_workspace_update.py`
- `conda run -n emg python -m pytest -q`
- `conda run -n emg python -m mypy src tests`
- `conda run -n emg python -m ruff check src tests`
READY: NO

## Queue Entry 3
TASK_ID: retrieval-reactivation-boundary-v0
MILESTONE: Runtime freeze dependency
OBJECTIVE: Implement retrieval/reactivation workflow to close remaining runtime architecture freeze requirements.
PREREQUISITES:
- Queue Entry 2 complete
- Core identity/episode shape stabilized
PRIMARY_DOCS:
- `docs/specs/01_architecture_overview.md`
- `docs/specs/05_operational_flows.md`
- `docs/specs/02_data_model.md`
TARGET_FILES:
- `src/workspace/` (reactivation boundary module)
- `src/store/` (read/query interfaces as required)
- `tests/test_workspace_state.py`
- `tests/test_workspace_update.py`
- `tests/smoke/test_workspace_update_smoke.py`
ACCEPTANCE_CRITERIA:
- Reactivation loads relevant canonical subgraph only.
- Deterministic interface and tests close `C20-RUNTIME-04` and advance `C21-02`.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q tests/test_workspace_state.py tests/test_workspace_update.py tests/smoke/test_workspace_update_smoke.py`
- `conda run -n emg python -m pytest -q`
- `conda run -n emg python -m mypy src tests`
- `conda run -n emg python -m ruff check src tests`
READY: YES

## Queue Entry 4
TASK_ID: baseline-variants-core-v0
MILESTONE: M9
OBJECTIVE: Implement runnable baseline memory systems listed in `configs/baselines_v0q.yaml` under fair shared controls.
PREREQUISITES:
- Queue Entry 3 complete
- Evaluation artifacts + fairness contracts remain frozen
PRIMARY_DOCS:
- `docs/specs/08_evaluation_and_metrics.md`
- `configs/baselines_v0q.yaml`
- `configs/eval_v0q.yaml`
TARGET_FILES:
- `src/eval/` baseline adapters
- `scripts/` benchmark runner scaffolds
- `tests/test_eval_fairness.py`
- `tests/TEST_INDEX.md`
- `scripts/SCRIPTS_INDEX.md`
ACCEPTANCE_CRITERIA:
- All six baseline systems are runnable through one deterministic interface.
- Fairness preflight blocks mismatched run specs.
- Checklist row `C20-EVAL-03` transitions to DONE.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q tests/test_eval_fairness.py`
- `conda run -n emg python -m pytest -q`
- `conda run -n emg python -m mypy src tests`
- `conda run -n emg python -m ruff check src tests`
READY: NO

## Queue Entry 5
TASK_ID: governance-stress-suite-v0
MILESTONE: M10 Stage 2
OBJECTIVE: Implement governance stress scenarios and deterministic seed execution harness with required artifact output.
PREREQUISITES:
- Queue Entry 4 complete
- Baseline execution interface stabilized
PRIMARY_DOCS:
- `docs/specs/08_evaluation_and_metrics.md`
- `configs/eval_v0q.yaml`
- `MASTER_DOC.md` section 16.2
TARGET_FILES:
- `src/eval/`
- `scripts/`
- `tests/test_eval_artifacts.py`
- `tests/smoke/test_eval_artifact_smoke.py`
ACCEPTANCE_CRITERIA:
- Stage 2 scenario suite covers required stress failure modes.
- Harness runs fixed seeds `[101, 202, 303, 404, 505]` deterministically.
- Required artifact files are emitted for each run.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q tests/test_eval_artifacts.py tests/smoke/test_eval_artifact_smoke.py`
- `conda run -n emg python -m pytest -q`
- `conda run -n emg python -m mypy src tests`
- `conda run -n emg python -m ruff check src tests`
READY: NO

## Queue Entry 6
TASK_ID: baseline-comparison-claims-v0
MILESTONE: M10 Stage 3
OBJECTIVE: Execute fairness-locked baseline comparison and compute Stage 3 claim-threshold outcomes.
PREREQUISITES:
- Queue Entry 5 complete
- Baseline systems + stress harness stable
PRIMARY_DOCS:
- `docs/specs/08_evaluation_and_metrics.md`
- `docs/specs/10_checklists_and_dod.md`
- `configs/eval_v0q.yaml`
TARGET_FILES:
- `src/eval/`
- `scripts/`
- `artifacts/` (run outputs)
- `docs/handoff/OVERVIEW_CHECKLIST.md`
ACCEPTANCE_CRITERIA:
- Stage 3 fairness parity verified before comparisons.
- Relative governance improvement and non-degradation thresholds computed and reported.
- Checklist rows `C21-05` and `C21-06` updated with evidence.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q tests/test_eval_fairness.py tests/test_eval_artifacts.py`
- `conda run -n emg python -m pytest -q`
- `conda run -n emg python -m mypy src tests`
- `conda run -n emg python -m ruff check src tests`
READY: NO

## Queue Entry 7
TASK_ID: long-horizon-study-v0
MILESTONE: M10 Stage 4
OBJECTIVE: Run end-to-end long-horizon task study and verify paired governance + continuity improvements.
PREREQUISITES:
- Queue Entry 6 complete
- Stage 3 comparison evidence available
PRIMARY_DOCS:
- `docs/specs/08_evaluation_and_metrics.md`
- `docs/specs/10_checklists_and_dod.md`
- `MASTER_DOC.md` section 16.4
TARGET_FILES:
- `src/eval/`
- `scripts/`
- `artifacts/`
- `docs/handoff/OVERVIEW_CHECKLIST.md`
ACCEPTANCE_CRITERIA:
- At least one task family shows paired governance and continuity improvement.
- Long-horizon evidence updates `C21-07` with artifact links.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q tests/test_eval_artifacts.py`
- `conda run -n emg python -m pytest -q`
- `conda run -n emg python -m mypy src tests`
- `conda run -n emg python -m ruff check src tests`
READY: NO

## Queue Entry 8
TASK_ID: dod-evidence-closeout-v0
MILESTONE: M10 closeout
OBJECTIVE: Verify all checklist/DoD rows are evidence-complete, close open documentation decisions, and freeze final status.
PREREQUISITES:
- Queue Entries 1-7 complete
- All required artifacts archived and indexed
PRIMARY_DOCS:
- `docs/specs/10_checklists_and_dod.md`
- `docs/handoff/OVERVIEW_CHECKLIST.md`
- `docs/handoff/DECISION_LOG.md`
- `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md`
TARGET_FILES:
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
- `docs/handoff/OVERVIEW_CHECKLIST.md`
- `docs/handoff/DECISION_LOG.md`
- `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md`
ACCEPTANCE_CRITERIA:
- All Section B/C rows are either DONE with evidence or explicitly BLOCKED with rationale.
- Open decisions are resolved or explicitly deferred beyond v0.
- Final DoD readiness state is evidence-backed and auditable.
VALIDATION_COMMANDS:
- `rg "^CHECK_ID:" docs/handoff/OVERVIEW_CHECKLIST.md`
- `rg "^DECISION_ID:|^STATUS:" docs/handoff/DECISION_LOG.md`
- `rg "^SPEC_MUST_ID:" docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md`
- `rg "^NEXT_TASK_ID:|^ACTIVE_QUEUE_TASK_ID:" docs/handoff/CURRENT_STATUS.md`
READY: NO

## Queue Update Rules
- Keep one and only one queue entry with `READY: YES`.
- `CURRENT_STATUS.md:ACTIVE_QUEUE_TASK_ID` must match the `TASK_ID` of the `READY: YES` queue entry.
- `NEXT_TASK.md:TASK_ID` must match `CURRENT_STATUS.md:NEXT_TASK_ID` and `ACTIVE_QUEUE_TASK_ID`.
- Keep queue entries concise and operational; avoid narrative logs.

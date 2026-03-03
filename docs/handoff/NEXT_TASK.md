# Next Task

TASK_ID: baseline-comparison-claims-v0
TASK_TITLE: Execute baseline comparison and Stage 3 claim-threshold computation
OBJECTIVE: Run fairness-locked Stage 3 baseline comparison and compute/report required v0.1q claim thresholds against raw-log baseline.
OWNER_CHECK_IDS:
- C20-EVAL-05
- C21-05
- C21-06
SPEC_MUST_IDS:
- S08-M02
- S08-M08
IN_SCOPE:
- Implement Stage 3 comparison workflow interfaces under `src/eval/`.
- Compute threshold checks for relative governance improvements and non-degradation task success constraints.
- Keep fairness parity checks active before Stage 3 comparisons.
- Extend deterministic tests in `tests/test_eval_fairness.py` and `tests/test_eval_artifacts.py` as needed.
- Update `scripts/` scaffolds only if needed for deterministic Stage 3 entrypoints.
OUT_OF_SCOPE:
- Stage 4 long-horizon study execution and claim updates.
- Policy/state-machine/scoring threshold changes.
- Any edits to frozen `configs/*.yaml`.
TARGET_FILES:
- `src/eval/`
- `scripts/`
- `tests/test_eval_fairness.py`
- `tests/test_eval_artifacts.py`
- `tests/TEST_INDEX.md`
- `scripts/SCRIPTS_INDEX.md`
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
- `docs/handoff/OVERVIEW_CHECKLIST.md`
- `docs/handoff/TASK_QUEUE.md`
- `docs/handoff/DECISION_LOG.md`
- `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md`
PREREQUISITES:
- Review `docs/handoff/CURRENT_STATUS.md`, `docs/handoff/TASK_QUEUE.md`, and this file.
- Confirm `TASK_ID` continuity across `CURRENT_STATUS.md:NEXT_TASK_ID`, `CURRENT_STATUS.md:ACTIVE_QUEUE_TASK_ID`, and queue `READY: YES` row.
- Read `docs/specs/08_evaluation_and_metrics.md` and `docs/specs/10_checklists_and_dod.md`.
- Read `configs/eval_v0q.yaml`, `tests/TEST_INDEX.md`, and `scripts/SCRIPTS_INDEX.md`.
- Read `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md` entries listed in `SPEC_MUST_IDS`.
- Preserve fixed gate order and single-task scope.
IMPLEMENTATION_SUBTASKS:
1. Implement deterministic Stage 3 comparison runner interfaces for baseline outcome aggregation.
2. Enforce fairness parity checks before threshold computation.
3. Compute and emit Stage 3 claim-threshold outcomes versus raw-log baseline.
4. Add deterministic unit coverage for fairness-locked comparison and threshold evaluation.
5. Confirm `tests/TEST_INDEX.md` and `scripts/SCRIPTS_INDEX.md` remain accurate (or update if mapped surfaces change).
6. Update `OWNER_CHECK_IDS` and `SPEC_MUST_IDS` evidence/state rows in handoff checklists.
7. Run quality gates in fixed order and capture outcomes.
8. Update handoff docs for loop completion and task continuity.
QUALITY_GATES:
1) Unit tests and/or smoke scripts
2) Type checking
3) Linting
4) Spec conformance check
5) Documentation + handoff updates
ACCEPTANCE_CRITERIA:
- [ ] Stage 3 comparison workflow executes deterministically across required baseline systems.
- [ ] Fairness parity is checked before Stage 3 threshold calculations.
- [ ] Relative governance-improvement and task-success non-degradation thresholds are computed.
- [ ] `docs/handoff/OVERVIEW_CHECKLIST.md` rows in `OWNER_CHECK_IDS` are updated with current evidence/state.
- [ ] `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md` rows in `SPEC_MUST_IDS` are updated with current evidence/state.
- [ ] `conda run -n emg python -m pytest -q tests/test_eval_fairness.py tests/test_eval_artifacts.py` passes.
- [ ] `conda run -n emg python -m pytest -q` passes.
- [ ] `conda run -n emg python -m mypy src tests` passes.
- [ ] `conda run -n emg python -m ruff check src tests` passes.
- [ ] Handoff docs are updated and task IDs remain continuous.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q tests/test_eval_fairness.py tests/test_eval_artifacts.py`
- `conda run -n emg python -m pytest -q`
- `conda run -n emg python -m mypy src tests`
- `conda run -n emg python -m ruff check src tests`
- `rg --files src tests scripts docs/handoff`
- `rg "^TASK_ID:|^OWNER_CHECK_IDS:|^SPEC_MUST_IDS:" docs/handoff/NEXT_TASK.md`
- `rg "^NEXT_TASK_ID:|^ACTIVE_QUEUE_TASK_ID:" docs/handoff/CURRENT_STATUS.md`
- `rg "^TASK_ID:|^READY:" docs/handoff/TASK_QUEUE.md`
- `git status --short`
DONE_UPDATE_REQUIREMENTS:
- Update `docs/handoff/CURRENT_STATUS.md` with completed-task facts and gate outcomes.
- Update `docs/handoff/NEXT_TASK.md` with the next single-task contract.
- Update `docs/handoff/OVERVIEW_CHECKLIST.md` for owner-check continuity.
- Update `docs/handoff/TASK_QUEUE.md` for queue readiness continuity.
- Update `docs/handoff/DECISION_LOG.md` for any decision status/count changes.
- Update `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md` for referenced MUST-row continuity.
- Keep handoff updates concise and operational.
FAILURE_PROTOCOL:
- If a gate fails, record `FAIL` with one-line cause and fix in-scope issues only.
- If environment/tooling becomes unavailable, record `UNKNOWN` with exact blocker.
- If unexpected repo changes appear, pause and request user direction.

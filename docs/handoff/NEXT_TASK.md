# Next Task

TASK_ID: workspace-update-boundary-v0q-v0
TASK_TITLE: Compose deterministic workspace update boundary with v0.1q gates
OBJECTIVE: Implement one deterministic workspace boundary call that ingests an observation, updates the `(session_id, task_id)` observation index, and returns consolidation/promotion eligibility metadata using frozen v0.1q helpers.
IN_SCOPE:
- Add `src/workspace/update.py` with typed request/result objects for composed update behavior.
- Compose `WorkspaceObservationIntake` and `InMemoryWorkspaceObservationIndex` in one boundary call.
- Integrate `should_run_consolidation` and `evaluate_promotion_eligibility` into result metadata.
- Ensure deterministic handling of fresh and duplicate intake paths.
- Add focused tests for intake/index integration and cadence/promotion eligibility outputs.
OUT_OF_SCOPE:
- Benchmark runner execution or baseline-comparison runs.
- Identity merge or alias-resolution logic.
- Broader orchestration beyond single-call workspace update behavior.
TARGET_FILES:
- `src/workspace/update.py`
- `src/workspace/__init__.py`
- `tests/test_workspace_update.py`
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
- `docs/handoff/OVERVIEW_CHECKLIST.md`
PREREQUISITES:
- Review `docs/handoff/CURRENT_STATUS.md` and this file.
- Read `docs/specs/05_operational_flows.md` and `configs/policy_v0q.yaml`.
- Preserve fixed gate order and single-task scope.
IMPLEMENTATION_SUBTASKS:
1. Add `src/workspace/update.py` with deterministic composed intake/index/update flow and typed request/result models.
2. Export update-path symbols from `src/workspace/__init__.py`.
3. Add `tests/test_workspace_update.py` for fresh/duplicate intake plus consolidation cadence and promotion-eligibility output behavior.
4. Run quality gates in fixed order and capture outcomes.
5. Update handoff docs for loop completion and next-task continuity.
QUALITY_GATES:
1) Unit tests and/or smoke scripts
2) Type checking
3) Linting
4) Spec conformance check
5) Documentation + handoff updates
ACCEPTANCE_CRITERIA:
- [ ] `src/workspace/update.py` defines typed composed update request/result structures.
- [ ] Composed boundary deterministically records intake outcome and session/task index state.
- [ ] Composed result includes consolidation cadence decision and promotion-eligibility metadata.
- [ ] Tests validate fresh and duplicate intake/index behavior plus cadence/promotion outputs.
- [ ] `conda run -n emg python -m pytest -q` passes.
- [ ] `conda run -n emg python -m mypy src tests` passes.
- [ ] `conda run -n emg python -m ruff check src tests` passes.
- [ ] Handoff docs are updated and task IDs remain continuous.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q`
- `conda run -n emg python -m mypy src tests`
- `conda run -n emg python -m ruff check src tests`
- `rg --files src tests`
- `git status --short`
DONE_UPDATE_REQUIREMENTS:
- Update `docs/handoff/CURRENT_STATUS.md` with completed-task facts and gate outcomes.
- Update `docs/handoff/NEXT_TASK.md` with the next single-task contract.
- Update `docs/handoff/OVERVIEW_CHECKLIST.md` for owner-task continuity.
- Keep handoff updates concise and operational.
FAILURE_PROTOCOL:
- If a gate fails, record `FAIL` with one-line cause and fix in-scope issues only.
- If environment/tooling becomes unavailable, record `UNKNOWN` with exact blocker.
- If unexpected repo changes appear, pause and request user direction.

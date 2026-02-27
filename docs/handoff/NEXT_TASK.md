# Next Task

TASK_ID: workspace-intake-index-update-path-v0
TASK_TITLE: Wire deterministic intake and index update path
OBJECTIVE: Add a minimal workspace boundary that executes observation intake and session/task observation-id index registration in one deterministic in-memory operation.
IN_SCOPE:
- Add a small coordinator module under `src/workspace/` that composes `WorkspaceObservationIntake` and `InMemoryWorkspaceObservationIndex`.
- Define typed request/result shape for the combined update call.
- Ensure deterministic behavior for both fresh and repeated observation processing.
- Add focused tests for ingest-and-register behavior and duplicate handling behavior.
OUT_OF_SCOPE:
- Policy transitions, scoring, or consolidation decisions.
- Proposition/entity mutation logic.
- Multi-step orchestration beyond deterministic intake + index updates.
TARGET_FILES:
- `src/workspace/update.py`
- `src/workspace/__init__.py`
- `tests/test_workspace_update.py`
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
PREREQUISITES:
- Review `docs/handoff/CURRENT_STATUS.md` and this file.
- Read `docs/specs/01_architecture_overview.md` and `docs/specs/05_operational_flows.md`.
- Preserve fixed gate order and single-task scope.
IMPLEMENTATION_SUBTASKS:
1. Add `src/workspace/update.py` with a deterministic intake-and-index workspace boundary.
2. Export update-path symbols from `src/workspace/__init__.py`.
3. Add `tests/test_workspace_update.py` for ingest-and-register and duplicate-path behavior.
4. Run quality gates in fixed order and capture outcomes.
5. Update handoff docs for loop completion and next task continuity.
QUALITY_GATES:
1) Unit tests and/or smoke scripts
2) Type checking
3) Linting
4) Spec conformance check
5) Documentation + handoff updates
ACCEPTANCE_CRITERIA:
- [ ] Workspace update module exists with typed combined request/result structures.
- [ ] Combined boundary deterministically records intake outcome and session/task index state.
- [ ] Tests validate ingest-and-register behavior and duplicate behavior.
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

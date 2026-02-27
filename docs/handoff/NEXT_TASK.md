# Next Task

TASK_ID: workspace-observation-intake-v0
TASK_TITLE: Add minimal workspace observation-intake boundary
OBJECTIVE: Add a minimal workspace intake component that records incoming observations through the store interface and returns deterministic intake results for downstream workflow wiring.
IN_SCOPE:
- Add a small workspace intake module under `src/workspace/`.
- Define a typed intake request/result shape for observation ingest.
- Wire intake to `ObservationStore.append` and id lookup only.
- Add focused tests for successful ingest and duplicate-observation handling.
OUT_OF_SCOPE:
- Policy transitions, scoring, or consolidation decisions.
- Proposition/entity mutation logic.
- Multi-step orchestration beyond single observation intake.
TARGET_FILES:
- `src/workspace/intake.py`
- `src/workspace/__init__.py`
- `tests/test_workspace_intake.py`
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
PREREQUISITES:
- Review `docs/handoff/CURRENT_STATUS.md` and this file.
- Read `docs/specs/01_architecture_overview.md` and `docs/specs/05_operational_flows.md`.
- Preserve fixed gate order and single-task scope.
IMPLEMENTATION_SUBTASKS:
1. Add `src/workspace/intake.py` with a minimal intake function/class that writes observations via `ObservationStore`.
2. Export intake symbols from `src/workspace/__init__.py`.
3. Add `tests/test_workspace_intake.py` for success and duplicate-id failure behavior.
4. Run quality gates in fixed order and capture outcomes.
5. Update both handoff docs for loop completion and next task continuity.
QUALITY_GATES:
1) Unit tests and/or smoke scripts
2) Type checking
3) Linting
4) Spec conformance check
5) Documentation + handoff updates
ACCEPTANCE_CRITERIA:
- [ ] Workspace intake module exists with typed request/result structures.
- [ ] Intake writes through `ObservationStore` and reports deterministic status.
- [ ] Tests validate successful ingest and duplicate handling.
- [ ] `conda run -n emg python -m pytest -q` passes.
- [ ] `conda run -n emg python -m mypy src tests` passes.
- [ ] `conda run -n emg python -m ruff check src tests` passes.
- [ ] Both handoff docs are updated and task IDs remain continuous.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q`
- `conda run -n emg python -m mypy src tests`
- `conda run -n emg python -m ruff check src tests`
- `rg --files src tests`
- `git status --short`
DONE_UPDATE_REQUIREMENTS:
- Update `docs/handoff/CURRENT_STATUS.md` with completed-task facts and gate outcomes.
- Update `docs/handoff/NEXT_TASK.md` with the next single-task contract.
- Keep both files concise and operational.
FAILURE_PROTOCOL:
- If a gate fails, record `FAIL` with one-line cause and fix in-scope issues only.
- If environment/tooling becomes unavailable, record `UNKNOWN` with exact blocker.
- If unexpected repo changes appear, pause and request user direction.

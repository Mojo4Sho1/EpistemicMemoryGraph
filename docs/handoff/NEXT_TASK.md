# Next Task

TASK_ID: workspace-session-observation-index-v0
TASK_TITLE: Add minimal session/task observation index in workspace
OBJECTIVE: Add a minimal in-memory workspace index keyed by session and task that records ingested observation ids for deterministic downstream workspace wiring.
IN_SCOPE:
- Add a small in-memory workspace index module under `src/workspace/`.
- Define typed request/result shape for registering observation ids to a session/task key.
- Support deterministic append semantics for observation id lists per key.
- Add focused tests for new key creation and repeated-key append behavior.
OUT_OF_SCOPE:
- Policy transitions, scoring, or consolidation decisions.
- Proposition/entity mutation logic.
- Multi-step orchestration beyond deterministic index updates.
TARGET_FILES:
- `src/workspace/state.py`
- `src/workspace/__init__.py`
- `tests/test_workspace_state.py`
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
PREREQUISITES:
- Review `docs/handoff/CURRENT_STATUS.md` and this file.
- Read `docs/specs/01_architecture_overview.md` and `docs/specs/05_operational_flows.md`.
- Preserve fixed gate order and single-task scope.
IMPLEMENTATION_SUBTASKS:
1. Add `src/workspace/state.py` with a minimal workspace session/task index for observation ids.
2. Export state symbols from `src/workspace/__init__.py`.
3. Add `tests/test_workspace_state.py` for key initialization and deterministic append behavior.
4. Run quality gates in fixed order and capture outcomes.
5. Update both handoff docs for loop completion and next task continuity.
QUALITY_GATES:
1) Unit tests and/or smoke scripts
2) Type checking
3) Linting
4) Spec conformance check
5) Documentation + handoff updates
ACCEPTANCE_CRITERIA:
- [ ] Workspace state module exists with typed request/result structures.
- [ ] Session/task index records observation ids deterministically.
- [ ] Tests validate key creation and repeated-key append behavior.
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

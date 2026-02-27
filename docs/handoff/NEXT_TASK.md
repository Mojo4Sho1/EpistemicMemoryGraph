# Next Task

TASK_ID: observation-store-interface-v0
TASK_TITLE: Add minimal observation store interface scaffolding
OBJECTIVE: Define a minimal typed store boundary for appending observations so policy and workflow layers can depend on stable persistence interfaces before full schema implementation.
IN_SCOPE:
- Add a small `src/store/observation_store.py` interface module.
- Define protocol/ABC methods for append and lookup by `observation_id` only.
- Add in-memory stub implementation for test-time behavior.
- Add focused tests for append immutability semantics and lookup behavior.
OUT_OF_SCOPE:
- SQLite wiring or migrations.
- Full repository/query layer across all object types.
- Policy transition logic or scoring behavior.
TARGET_FILES:
- `src/store/observation_store.py`
- `src/store/__init__.py`
- `tests/test_observation_store.py`
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
PREREQUISITES:
- Review `docs/handoff/CURRENT_STATUS.md` and this file.
- Read `docs/specs/02_data_model.md` and `docs/specs/01_architecture_overview.md`.
- Preserve fixed gate order and single-task scope.
IMPLEMENTATION_SUBTASKS:
1. Create `src/store/observation_store.py` with a minimal append/get interface and an in-memory stub implementation.
2. Export store interfaces from `src/store/__init__.py`.
3. Add `tests/test_observation_store.py` validating append-only behavior and retrieval by id.
4. Run quality gates in fixed order and capture outcomes.
5. Update both handoff docs for loop completion and next task continuity.
QUALITY_GATES:
1) Unit tests and/or smoke scripts
2) Type checking
3) Linting
4) Spec conformance check
5) Documentation + handoff updates
ACCEPTANCE_CRITERIA:
- [ ] Observation store interface module exists and is typed.
- [ ] In-memory stub supports append and id lookup.
- [ ] Tests validate append/lookup behavior and pass under pytest.
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

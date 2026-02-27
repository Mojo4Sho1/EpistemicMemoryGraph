# Next Task

TASK_ID: observation-sqlite-store-v0
TASK_TITLE: Add minimal SQLite-backed observation store
OBJECTIVE: Implement a minimal SQLite observation store adapter that honors append-only observation semantics and lookup by `observation_id` through the existing store interface.
IN_SCOPE:
- Add a SQLite-backed implementation in `src/store/observation_store.py`.
- Keep schema minimal and local to observation fields required by v0 primitives.
- Add focused tests for append, duplicate-id rejection, and id lookup using temporary DB files.
- Keep interface compatibility with existing in-memory store.
OUT_OF_SCOPE:
- Migrations framework or multi-table relational schema rollout.
- Persistence for entities, propositions, edges, or episodes.
- Policy transitions, scoring, and consolidation behavior.
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
1. Add `SQLiteObservationStore` implementation with minimal table creation and append/get operations.
2. Keep `ObservationStore` interface and existing in-memory store behavior stable.
3. Extend `tests/test_observation_store.py` with SQLite adapter tests using `tmp_path`.
4. Run quality gates in fixed order and capture outcomes.
5. Update both handoff docs for loop completion and next task continuity.
QUALITY_GATES:
1) Unit tests and/or smoke scripts
2) Type checking
3) Linting
4) Spec conformance check
5) Documentation + handoff updates
ACCEPTANCE_CRITERIA:
- [ ] `SQLiteObservationStore` exists and conforms to store interface methods.
- [ ] SQLite adapter preserves append-only behavior and lookup by id.
- [ ] Store tests cover in-memory + SQLite behaviors and pass under pytest.
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

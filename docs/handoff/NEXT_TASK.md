# Next Task

TASK_ID: observation-sqlite-store-v0
TASK_TITLE: Harden SQLite observation-store persistence contract
OBJECTIVE: Expand deterministic SQLite persistence evidence so the observation-log milestone has stronger append/lookup conformance coverage.
IN_SCOPE:
- Extend `tests/test_observation_store.py` with deterministic SQLite coverage for persistence across store re-instantiation on the same database path.
- Add deterministic SQLite timestamp round-trip assertions for naive and timezone-aware timestamps.
- If tests expose a gap, apply minimal in-scope fixes in `src/store/observation_store.py`.
- Update `tests/TEST_INDEX.md` only if the test surface description changes.
- Preserve append-only duplicate protection behavior.
OUT_OF_SCOPE:
- Workspace update boundary behavior changes.
- Smoke-suite additions beyond existing files in `tests/smoke/`.
- Policy/evaluation threshold changes in `configs/*.yaml`.
TARGET_FILES:
- `src/store/observation_store.py`
- `tests/test_observation_store.py`
- `tests/TEST_INDEX.md`
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
- `docs/handoff/OVERVIEW_CHECKLIST.md`
PREREQUISITES:
- Review `docs/handoff/CURRENT_STATUS.md` and this file.
- Read `docs/specs/02_data_model.md` and `docs/specs/10_checklists_and_dod.md`.
- Read `tests/TEST_INDEX.md` and `configs/CONFIG_INDEX.md`.
- Preserve fixed gate order and single-task scope.
IMPLEMENTATION_SUBTASKS:
1. Add deterministic SQLite persistence tests for reopen behavior and timestamp round-trip invariants in `tests/test_observation_store.py`.
2. Patch `src/store/observation_store.py` only if required to satisfy deterministic contract expectations.
3. Confirm test index accuracy in `tests/TEST_INDEX.md`.
4. Run quality gates in fixed order and capture outcomes.
5. Update handoff docs for loop completion and task continuity.
QUALITY_GATES:
1) Unit tests and/or smoke scripts
2) Type checking
3) Linting
4) Spec conformance check
5) Documentation + handoff updates
ACCEPTANCE_CRITERIA:
- [ ] `tests/test_observation_store.py` includes deterministic SQLite reopen and timestamp round-trip conformance checks.
- [ ] `src/store/observation_store.py` remains append-only and duplicate-safe.
- [ ] `conda run -n emg python -m pytest -q tests/test_observation_store.py` passes.
- [ ] `conda run -n emg python -m pytest -q` passes.
- [ ] `conda run -n emg python -m mypy src tests` passes.
- [ ] `conda run -n emg python -m ruff check src tests` passes.
- [ ] Handoff docs are updated and task IDs remain continuous.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q tests/test_observation_store.py`
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

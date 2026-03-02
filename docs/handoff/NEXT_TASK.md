# Next Task

TASK_ID: retrieval-reactivation-boundary-v0
TASK_TITLE: Implement retrieval/reactivation workflow boundary
OBJECTIVE: Add deterministic retrieval/reactivation boundary behavior that loads only relevant canonical subgraph context and advances runtime architecture closure targets.
OWNER_CHECK_IDS:
- C20-RUNTIME-04
- C21-02
SPEC_MUST_IDS:
- S01-M01
- S01-M04
- S05-M01
IN_SCOPE:
- Add deterministic retrieval/reactivation boundary module(s) under `src/workspace/` for loading canonical context by session/task-scoped relevance keys.
- Extend workspace update orchestration only as needed to wire retrieval/reactivation inputs/outputs without changing frozen policy scoring thresholds.
- Add deterministic retrieval/reactivation coverage in `tests/test_workspace_state.py` and `tests/test_workspace_update.py`.
- Update `tests/TEST_INDEX.md` only if the test surface map changes.
- Keep `configs/*.yaml` unchanged.
OUT_OF_SCOPE:
- Consolidation cadence/carryover/promotion behavior changes.
- Identity merge-policy changes beyond existing no-hard-auto-merge behavior.
- New baseline variants, benchmark harness work, or long-horizon studies.
- Any changes to frozen policy/eval/baseline YAML files.
TARGET_FILES:
- `src/workspace/` (reactivation boundary module(s))
- `src/store/` (read/query interfaces as required)
- `src/workspace/update.py`
- `tests/test_workspace_state.py`
- `tests/test_workspace_update.py`
- `tests/smoke/test_workspace_update_smoke.py`
- `tests/TEST_INDEX.md`
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
- `docs/handoff/OVERVIEW_CHECKLIST.md`
- `docs/handoff/TASK_QUEUE.md`
- `docs/handoff/DECISION_LOG.md`
- `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md`
PREREQUISITES:
- Review `docs/handoff/CURRENT_STATUS.md`, `docs/handoff/TASK_QUEUE.md`, and this file.
- Confirm `TASK_ID` continuity across `CURRENT_STATUS.md:NEXT_TASK_ID`, `CURRENT_STATUS.md:ACTIVE_QUEUE_TASK_ID`, and queue `READY: YES` row.
- Read `docs/specs/01_architecture_overview.md`, `docs/specs/05_operational_flows.md`, `docs/specs/02_data_model.md`, and `docs/specs/10_checklists_and_dod.md`.
- Read `tests/TEST_INDEX.md` and `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md` entries listed in `SPEC_MUST_IDS`.
- Preserve fixed gate order and single-task scope.
IMPLEMENTATION_SUBTASKS:
1. Implement retrieval/reactivation boundary primitives that deterministically select relevant canonical context without full-graph hydration.
2. Wire retrieval/reactivation boundary outputs into `src/workspace/update.py` interfaces as required while preserving existing deterministic update behavior.
3. Add deterministic retrieval/reactivation micro-scenarios in `tests/test_workspace_state.py`, `tests/test_workspace_update.py`, and smoke coverage as needed.
4. Confirm `tests/TEST_INDEX.md` remains accurate (or update if the mapped surface changes).
5. Update `OWNER_CHECK_IDS` and `SPEC_MUST_IDS` evidence/state rows in handoff checklists.
6. Run quality gates in fixed order and capture outcomes.
7. Update handoff docs for loop completion and task continuity.
QUALITY_GATES:
1) Unit tests and/or smoke scripts
2) Type checking
3) Linting
4) Spec conformance check
5) Documentation + handoff updates
ACCEPTANCE_CRITERIA:
- [ ] Retrieval/reactivation boundary code under `src/workspace/` loads relevant canonical context deterministically and avoids full-graph indiscriminate hydration.
- [ ] `src/workspace/update.py` integration preserves deterministic intake/index/consolidation/promotion behavior while adding retrieval/reactivation hooks.
- [ ] `tests/test_workspace_state.py` and `tests/test_workspace_update.py` include deterministic retrieval/reactivation boundary coverage.
- [ ] `docs/handoff/OVERVIEW_CHECKLIST.md` rows in `OWNER_CHECK_IDS` are updated with current evidence/state.
- [ ] `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md` rows in `SPEC_MUST_IDS` are updated with current evidence/state.
- [ ] `conda run -n emg python -m pytest -q tests/test_workspace_state.py tests/test_workspace_update.py tests/smoke/test_workspace_update_smoke.py` passes.
- [ ] `conda run -n emg python -m pytest -q` passes.
- [ ] `conda run -n emg python -m mypy src tests` passes.
- [ ] `conda run -n emg python -m ruff check src tests` passes.
- [ ] Handoff docs are updated and task IDs remain continuous.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q tests/test_workspace_state.py tests/test_workspace_update.py tests/smoke/test_workspace_update_smoke.py`
- `conda run -n emg python -m pytest -q`
- `conda run -n emg python -m mypy src tests`
- `conda run -n emg python -m ruff check src tests`
- `rg --files src tests docs/handoff`
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

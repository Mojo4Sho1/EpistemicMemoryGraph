# Next Task

TASK_ID: identity-alias-possible-same-as-v0
TASK_TITLE: Implement conservative identity ambiguity boundaries
OBJECTIVE: Add deterministic alias-linking and `possible_same_as` handling without hard auto-merge, with focused model/update coverage under frozen v0.1q defaults.
OWNER_CHECK_IDS:
- C20-DATA-03
- C20-DATA-04
SPEC_MUST_IDS:
- S02-M03
IN_SCOPE:
- Add/extend deterministic identity model support for alias and `possible_same_as` links in `src/core/models.py` and `src/core/constants.py`.
- Add/extend deterministic workspace update boundary handling in `src/workspace/update.py` that preserves conservative no-hard-auto-merge behavior.
- Extend `tests/test_core_models.py` and `tests/test_workspace_update.py` with duplicate-entity and false-merge guardrail micro-scenarios.
- Update `tests/TEST_INDEX.md` only if the test surface map changes.
- Keep `configs/*.yaml` unchanged.
OUT_OF_SCOPE:
- Retrieval/reactivation workflow implementation.
- Consolidation cadence/carryover/promotion behavior changes.
- New baseline variants, benchmark harness work, or long-horizon studies.
- Any changes to frozen policy/eval/baseline YAML files.
TARGET_FILES:
- `src/core/models.py`
- `src/core/constants.py`
- `src/workspace/update.py`
- `tests/test_core_models.py`
- `tests/test_workspace_update.py`
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
- Read `docs/specs/02_data_model.md`, `docs/specs/09_risks_non_goals_deferred.md`, and `docs/specs/10_checklists_and_dod.md`.
- Read `tests/TEST_INDEX.md`, `configs/CONFIG_INDEX.md`, and `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md` entries listed in `SPEC_MUST_IDS`.
- Preserve fixed gate order and single-task scope.
IMPLEMENTATION_SUBTASKS:
1. Implement or refine alias/`possible_same_as` identity representations in `src/core/models.py` and supporting constants.
2. Implement conservative identity handling in `src/workspace/update.py` that avoids hard auto-merge while retaining ambiguity links.
3. Add deterministic model-level edge-case coverage in `tests/test_core_models.py`.
4. Add deterministic workspace update guardrail coverage in `tests/test_workspace_update.py`.
5. Confirm `tests/TEST_INDEX.md` remains accurate (or update if the mapped surface changes).
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
- [ ] `src/core/models.py`, `src/core/constants.py`, and `src/workspace/update.py` implement conservative alias/`possible_same_as` handling with no hard auto-merge path.
- [ ] `tests/test_core_models.py` and `tests/test_workspace_update.py` include deterministic identity ambiguity/false-merge guardrail coverage expansions.
- [ ] `docs/handoff/OVERVIEW_CHECKLIST.md` rows in `OWNER_CHECK_IDS` are updated with current evidence/state.
- [ ] `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md` rows in `SPEC_MUST_IDS` are updated with current evidence/state.
- [ ] `conda run -n emg python -m pytest -q tests/test_core_models.py tests/test_workspace_update.py` passes.
- [ ] `conda run -n emg python -m pytest -q` passes.
- [ ] `conda run -n emg python -m mypy src tests` passes.
- [ ] `conda run -n emg python -m ruff check src tests` passes.
- [ ] Handoff docs are updated and task IDs remain continuous.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q tests/test_core_models.py tests/test_workspace_update.py`
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

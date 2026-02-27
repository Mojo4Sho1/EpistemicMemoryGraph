# Next Task

TASK_ID: emg-loop-0001
TASK_TITLE: Bootstrap minimal runtime scaffold and schema constants entrypoint
OBJECTIVE: Create the first minimal runtime scaffold so future loops can implement policy logic incrementally. This cycle should only establish initial package structure and schema/policy constants placeholders aligned with existing docs.
IN_SCOPE:
- Create initial runtime directories and placeholder module files under `src/`.
- Add a minimal constants/schema placeholder module aligned to v0 docs.
- Add minimal tests folder scaffold with one placeholder test for import wiring.
- Update docs if paths/contracts change.
OUT_OF_SCOPE:
- Full policy engine implementation.
- Database migrations or full SQLite schema implementation.
- End-to-end benchmark harness code.
TARGET_FILES:
- `src/core/__init__.py`
- `src/store/__init__.py`
- `src/workspace/__init__.py`
- `src/tools/__init__.py`
- `src/core/constants.py`
- `tests/test_scaffold_imports.py`
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
PREREQUISITES:
- Review `docs/specs/07_build_plan_and_milestones.md` for sequencing.
- Review `docs/specs/02_data_model.md` and `docs/specs/03_policy_and_state_machine.md` for naming.
- Keep scope to one-loop bootstrap only.
IMPLEMENTATION_SUBTASKS:
1. Create `src/` package directories and `__init__.py` files for `core`, `store`, `workspace`, and `tools`.
2. Add `src/core/constants.py` with clearly labeled placeholder constants for belief states and edge types from specs.
3. Create `tests/test_scaffold_imports.py` verifying scaffold imports and constants presence.
4. Run quality gates in order and capture outcomes.
5. Ensure any new names remain consistent with docs/spec terminology.
6. Update both handoff docs with completed state and define next single task.
QUALITY_GATES:
1) Unit tests and/or smoke scripts
2) Type checking
3) Linting
4) Spec conformance check
5) Documentation + handoff updates
ACCEPTANCE_CRITERIA:
- [ ] All listed `TARGET_FILES` exist with intentional content.
- [ ] Placeholder constants include documented belief states and edge types only.
- [ ] At least one test executes for scaffold/import sanity.
- [ ] Quality gate outcomes are recorded (pass/fail/unknown with reason).
- [ ] Handoff docs are updated for the next fresh agent loop.
VALIDATION_COMMANDS:
- `rg --files src tests`
- `python -m pytest -q`
- `rg "tentative|provisional|accepted|contested|deprecated|rejected" src/core/constants.py`
- `rg "supports|contradicts|about|predicts|tested_by|derived_from|possible_same_as|supersedes" src/core/constants.py`
- `git status --short`
DONE_UPDATE_REQUIREMENTS:
- Update `docs/handoff/CURRENT_STATUS.md` keys to reflect post-task reality.
- Replace this file with the next single-task contract.
- Keep both files concise and free of historical narrative.
FAILURE_PROTOCOL:
- If scope expands, stop and reduce to minimal scaffold deliverable.
- If any gate cannot run, record `UNKNOWN` with reason and required follow-up.
- If unexpected repo changes are detected, pause and request user direction before proceeding.

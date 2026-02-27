# Next Task

TASK_ID: core-model-primitives-v0
TASK_TITLE: Add minimal typed v0 core model primitives
OBJECTIVE: Create minimal, spec-aligned typed model primitives for core memory objects so upcoming policy and persistence work can build on stable interfaces.
IN_SCOPE:
- Add a small `src/core/models.py` module for v0 primitives.
- Define minimal typed structures for `Observation`, `Entity`, and `Proposition` fields required by v0 specs.
- Add focused tests validating required fields and belief-state compatibility.
- Keep interfaces implementation-light (no persistence or scoring logic yet).
OUT_OF_SCOPE:
- Policy transition engine implementation.
- Database schema/migrations.
- Runtime orchestration, workspace flows, or tool-boundary integration.
TARGET_FILES:
- `src/core/models.py`
- `src/core/__init__.py`
- `tests/test_core_models.py`
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
PREREQUISITES:
- Review `docs/handoff/CURRENT_STATUS.md` and this file.
- Read `docs/specs/02_data_model.md` and `docs/specs/03_policy_and_state_machine.md`.
- Preserve fixed gate order and single-task scope.
IMPLEMENTATION_SUBTASKS:
1. Create `src/core/models.py` with minimal dataclass-style typed primitives for `Observation`, `Entity`, and `Proposition`.
2. Export model primitives from `src/core/__init__.py`.
3. Add `tests/test_core_models.py` for basic construction/required-field validation and belief-state-set compatibility.
4. Run quality gates in fixed order and capture outcomes.
5. Update both handoff docs for loop completion and next task continuity.
QUALITY_GATES:
1) Unit tests and/or smoke scripts
2) Type checking
3) Linting
4) Spec conformance check
5) Documentation + handoff updates
ACCEPTANCE_CRITERIA:
- [ ] `Observation`, `Entity`, and `Proposition` primitives exist with explicit typed fields.
- [ ] New tests validate required fields and pass under pytest.
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

# Next Task

TASK_ID: policy-correctness-micro-suite-v0
TASK_TITLE: Expand policy correctness micro-scenario coverage
OBJECTIVE: Increase deterministic evidence for state-transition thresholds and hypothesis-test trigger ordering under frozen v0.1q policy defaults.
IN_SCOPE:
- Extend `tests/test_state_machine.py` with deterministic edge-case scenarios around accepted/rejected/deprecated threshold boundaries.
- Extend `tests/test_test_trigger.py` with deterministic trigger-order and low-impact cost-suppression scenarios.
- If tests expose a gap, apply minimal in-scope fixes in `src/core/state_machine.py` and/or `src/core/test_trigger.py`.
- Update `tests/TEST_INDEX.md` only if the test surface description changes.
- Keep `configs/*.yaml` unchanged.
OUT_OF_SCOPE:
- Workspace update boundary and consolidation behavior changes.
- New smoke tests or probe scripts.
- Any changes to frozen policy/eval/baseline YAML files.
TARGET_FILES:
- `src/core/state_machine.py`
- `src/core/test_trigger.py`
- `tests/test_state_machine.py`
- `tests/test_test_trigger.py`
- `tests/TEST_INDEX.md`
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
- `docs/handoff/OVERVIEW_CHECKLIST.md`
PREREQUISITES:
- Review `docs/handoff/CURRENT_STATUS.md` and this file.
- Read `docs/specs/03_policy_and_state_machine.md`, `docs/specs/04_scoring_and_trust.md`, `docs/specs/05_operational_flows.md`, and `docs/specs/10_checklists_and_dod.md`.
- Read `tests/TEST_INDEX.md`, `configs/CONFIG_INDEX.md`, and `configs/policy_v0q.yaml`.
- Preserve fixed gate order and single-task scope.
IMPLEMENTATION_SUBTASKS:
1. Add deterministic micro-scenarios to `tests/test_state_machine.py` for threshold-boundary transition behavior.
2. Add deterministic micro-scenarios to `tests/test_test_trigger.py` for ordered trigger precedence and suppression behavior.
3. Patch `src/core/state_machine.py` and/or `src/core/test_trigger.py` only if required to satisfy deterministic policy contract expectations.
4. Confirm test index accuracy in `tests/TEST_INDEX.md`.
5. Run quality gates in fixed order and capture outcomes.
6. Update handoff docs for loop completion and task continuity.
QUALITY_GATES:
1) Unit tests and/or smoke scripts
2) Type checking
3) Linting
4) Spec conformance check
5) Documentation + handoff updates
ACCEPTANCE_CRITERIA:
- [ ] `tests/test_state_machine.py` and `tests/test_test_trigger.py` include deterministic policy micro-scenario coverage expansions.
- [ ] `src/core/state_machine.py` and `src/core/test_trigger.py` preserve deterministic transition/trigger behavior.
- [ ] `conda run -n emg python -m pytest -q tests/test_state_machine.py tests/test_test_trigger.py` passes.
- [ ] `conda run -n emg python -m pytest -q` passes.
- [ ] `conda run -n emg python -m mypy src tests` passes.
- [ ] `conda run -n emg python -m ruff check src tests` passes.
- [ ] Handoff docs are updated and task IDs remain continuous.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q tests/test_state_machine.py tests/test_test_trigger.py`
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

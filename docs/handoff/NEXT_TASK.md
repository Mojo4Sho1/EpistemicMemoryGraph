# Next Task

TASK_ID: consolidation-archival-determinism-v0
TASK_TITLE: Harden consolidation and archival deterministic boundaries
OBJECTIVE: Increase deterministic evidence for consolidation cadence, unresolved-carryover cap behavior, and promotion eligibility thresholds under frozen v0.1q policy defaults.
IN_SCOPE:
- Extend `tests/test_workspace_consolidation.py` with deterministic edge-case scenarios around cadence boundaries, carryover-cap overflow handling, and promotion eligibility thresholds.
- If tests expose a gap, apply minimal in-scope fixes in `src/workspace/consolidation.py`.
- Update `tests/TEST_INDEX.md` only if the test surface description changes.
- Keep `configs/*.yaml` unchanged.
OUT_OF_SCOPE:
- Policy/state-machine and test-trigger behavior changes.
- New smoke tests or probe scripts.
- Any changes to frozen policy/eval/baseline YAML files.
TARGET_FILES:
- `src/workspace/consolidation.py`
- `tests/test_workspace_consolidation.py`
- `tests/TEST_INDEX.md`
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
- `docs/handoff/OVERVIEW_CHECKLIST.md`
PREREQUISITES:
- Review `docs/handoff/CURRENT_STATUS.md` and this file.
- Read `docs/specs/05_operational_flows.md`, `docs/specs/10_checklists_and_dod.md`, `docs/specs/03_policy_and_state_machine.md`, and `docs/specs/04_scoring_and_trust.md`.
- Read `tests/TEST_INDEX.md`, `configs/CONFIG_INDEX.md`, and `configs/policy_v0q.yaml`.
- Preserve fixed gate order and single-task scope.
IMPLEMENTATION_SUBTASKS:
1. Add deterministic micro-scenarios to `tests/test_workspace_consolidation.py` for cadence boundary behavior and deterministic rule-id expectations.
2. Add deterministic micro-scenarios to `tests/test_workspace_consolidation.py` for unresolved-carryover cap edge cases, deterministic ordering, and overflow reason-code handling.
3. Add deterministic micro-scenarios to `tests/test_workspace_consolidation.py` for promotion threshold boundaries (`accepted` + freshness gate).
4. Patch `src/workspace/consolidation.py` only if required to satisfy deterministic policy contract expectations.
5. Confirm test index accuracy in `tests/TEST_INDEX.md`.
6. Run quality gates in fixed order and capture outcomes.
7. Update handoff docs for loop completion and task continuity.
QUALITY_GATES:
1) Unit tests and/or smoke scripts
2) Type checking
3) Linting
4) Spec conformance check
5) Documentation + handoff updates
ACCEPTANCE_CRITERIA:
- [ ] `tests/test_workspace_consolidation.py` includes deterministic consolidation cadence/carryover/promotion micro-scenario coverage expansions.
- [ ] `src/workspace/consolidation.py` preserves deterministic consolidation and promotion behavior.
- [ ] `conda run -n emg python -m pytest -q tests/test_workspace_consolidation.py` passes.
- [ ] `conda run -n emg python -m pytest -q` passes.
- [ ] `conda run -n emg python -m mypy src tests` passes.
- [ ] `conda run -n emg python -m ruff check src tests` passes.
- [ ] Handoff docs are updated and task IDs remain continuous.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q tests/test_workspace_consolidation.py`
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

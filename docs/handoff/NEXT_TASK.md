# Next Task

TASK_ID: workspace-smoke-suite-v0q-v0
TASK_TITLE: Add minimal smoke suite and workspace update probe
OBJECTIVE: Add first smoke-layer runtime checks for the composed workspace update boundary and commit one deterministic probe script for developer diagnostics.
IN_SCOPE:
- Add `tests/smoke/test_workspace_update_smoke.py` covering deterministic end-to-end composed boundary behavior.
- Add `tests/smoke/test_eval_artifact_smoke.py` for minimal eval-artifact contract smoke validation.
- Add `scripts/probes/workspace_update_probe.py` with deterministic JSON output for manual workspace-boundary checks.
- Update `tests/TEST_INDEX.md` and `scripts/SCRIPTS_INDEX.md` to register new smoke/probe assets.
- Keep smoke coverage deterministic and scoped to in-memory/local fixtures.
OUT_OF_SCOPE:
- Benchmark runner execution or baseline comparisons.
- Any policy threshold/config changes in `configs/*.yaml`.
- Canonical-memory promotion/archive orchestration beyond smoke validation.
TARGET_FILES:
- `tests/smoke/test_workspace_update_smoke.py`
- `tests/smoke/test_eval_artifact_smoke.py`
- `scripts/probes/workspace_update_probe.py`
- `tests/TEST_INDEX.md`
- `scripts/SCRIPTS_INDEX.md`
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
- `docs/handoff/OVERVIEW_CHECKLIST.md`
PREREQUISITES:
- Review `docs/handoff/CURRENT_STATUS.md` and this file.
- Read `docs/specs/05_operational_flows.md`, `docs/specs/08_evaluation_and_metrics.md`, and `configs/policy_v0q.yaml`.
- Read `tests/TEST_INDEX.md` and `scripts/SCRIPTS_INDEX.md`.
- Preserve fixed gate order and single-task scope.
IMPLEMENTATION_SUBTASKS:
1. Add `tests/smoke/test_workspace_update_smoke.py` with deterministic smoke checks for composed update output invariants.
2. Add `tests/smoke/test_eval_artifact_smoke.py` with minimal artifact-contract smoke assertions.
3. Add `scripts/probes/workspace_update_probe.py` that prints deterministic JSON for one composed update scenario.
4. Run quality gates in fixed order and capture outcomes.
5. Update `tests/TEST_INDEX.md` and `scripts/SCRIPTS_INDEX.md`.
6. Update handoff docs for loop completion and next-task continuity.
QUALITY_GATES:
1) Unit tests and/or smoke scripts
2) Type checking
3) Linting
4) Spec conformance check
5) Documentation + handoff updates
ACCEPTANCE_CRITERIA:
- [ ] `tests/smoke/test_workspace_update_smoke.py` exists and validates deterministic composed boundary behavior.
- [ ] `tests/smoke/test_eval_artifact_smoke.py` exists and validates minimal eval artifact contract behavior.
- [ ] `scripts/probes/workspace_update_probe.py` exists and emits deterministic JSON output.
- [ ] Test/script indexes are updated to include the new smoke/probe paths.
- [ ] `conda run -n emg python -m pytest -q -m smoke` passes.
- [ ] `conda run -n emg python -m pytest -q` passes.
- [ ] `conda run -n emg python -m mypy src tests` passes.
- [ ] `conda run -n emg python -m ruff check src tests` passes.
- [ ] Handoff docs are updated and task IDs remain continuous.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q -m smoke`
- `conda run -n emg python -m pytest -q`
- `conda run -n emg python -m mypy src tests`
- `conda run -n emg python -m ruff check src tests`
- `conda run -n emg python scripts/probes/workspace_update_probe.py`
- `rg --files src tests`
- `rg --files scripts tests/smoke`
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

# Next Task

TASK_ID: baseline-variants-core-v0
TASK_TITLE: Implement runnable baseline variants under shared fairness controls
OBJECTIVE: Build deterministic baseline execution adapters that satisfy the baseline matrix and fairness preflight requirements for M9 progress.
OWNER_CHECK_IDS:
- C20-EVAL-03
SPEC_MUST_IDS:
- S08-M07
IN_SCOPE:
- Implement baseline adapter/runtime interfaces under `src/eval/` aligned to `configs/baselines_v0q.yaml`.
- Enforce fairness preflight parity inputs before baseline run acceptance.
- Add deterministic tests in `tests/test_eval_fairness.py` for baseline interface behavior.
- Update `tests/TEST_INDEX.md` only if the mapped test surface changes.
- Keep `configs/*.yaml` unchanged.
OUT_OF_SCOPE:
- Governance stress suite Stage 2 scenario generation and execution harness wiring.
- Stage 3 claim-threshold reporting and long-horizon study execution.
- Policy/state-machine/scoring threshold changes.
- Any edits to frozen policy/eval/baseline YAML files.
TARGET_FILES:
- `src/eval/`
- `scripts/` benchmark runner scaffolds (only if required by adapter entrypoint integration)
- `tests/test_eval_fairness.py`
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
- Read `docs/specs/08_evaluation_and_metrics.md` and `docs/specs/10_checklists_and_dod.md`.
- Read `configs/baselines_v0q.yaml` and `configs/eval_v0q.yaml`.
- Read `tests/TEST_INDEX.md` and `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md` entries listed in `SPEC_MUST_IDS`.
- Preserve fixed gate order and single-task scope.
IMPLEMENTATION_SUBTASKS:
1. Implement deterministic baseline runtime interfaces for systems listed in `configs/baselines_v0q.yaml`.
2. Enforce shared fairness preflight checks before run acceptance.
3. Add deterministic test coverage in `tests/test_eval_fairness.py` for baseline adapters and parity checks.
4. Confirm `tests/TEST_INDEX.md` remains accurate (or update if mapped test surface changes).
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
- [ ] Baseline runtime interfaces are deterministic and cover systems listed in `configs/baselines_v0q.yaml`.
- [ ] Fairness preflight deterministically blocks parity mismatches before run execution.
- [ ] `tests/test_eval_fairness.py` contains deterministic baseline interface + fairness checks.
- [ ] `docs/handoff/OVERVIEW_CHECKLIST.md` rows in `OWNER_CHECK_IDS` are updated with current evidence/state.
- [ ] `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md` rows in `SPEC_MUST_IDS` are updated with current evidence/state.
- [ ] `conda run -n emg python -m pytest -q tests/test_eval_fairness.py` passes.
- [ ] `conda run -n emg python -m pytest -q` passes.
- [ ] `conda run -n emg python -m mypy src tests` passes.
- [ ] `conda run -n emg python -m ruff check src tests` passes.
- [ ] Handoff docs are updated and task IDs remain continuous.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q tests/test_eval_fairness.py`
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

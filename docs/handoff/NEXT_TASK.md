# Next Task

TASK_ID: dod-evidence-closeout-v0
TASK_TITLE: Close remaining DoD evidence and freeze handoff readiness state
OBJECTIVE: Complete final checklist/spec/decision closeout for v0 by resolving or explicitly deferring remaining open readiness items.
OWNER_CHECK_IDS:
- C20-HYGIENE-05
SPEC_MUST_IDS:
- S10-M02
- S09-M02
IN_SCOPE:
- Implement and link a deterministic failure-analysis template required by research hygiene closeout.
- Reconcile remaining Section B/C checklist rows to `DONE` or explicit `BLOCKED` with evidence.
- Classify open decisions against active closeout acceptance criteria and lock any resolved decisions.
- Synchronize `CURRENT_STATUS.md`, `TASK_QUEUE.md`, and `DECISION_LOG.md` counters/continuity fields.
OUT_OF_SCOPE:
- Changes to frozen policy/state-machine/scoring thresholds.
- Changes to frozen `configs/*.yaml` baselines.
- New benchmark implementation beyond closeout evidence wiring.
TARGET_FILES:
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
- `docs/handoff/TASK_QUEUE.md`
- `docs/handoff/OVERVIEW_CHECKLIST.md`
- `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md`
- `docs/handoff/DECISION_LOG.md`
- `docs/specs/10_checklists_and_dod.md`
- `docs/specs/09_risks_non_goals_deferred.md`
- `docs/`
PREREQUISITES:
- Review `docs/handoff/CURRENT_STATUS.md`, `docs/handoff/TASK_QUEUE.md`, and this file.
- Confirm `TASK_ID` continuity across `CURRENT_STATUS.md:NEXT_TASK_ID`, `CURRENT_STATUS.md:ACTIVE_QUEUE_TASK_ID`, and queue `READY: YES` row.
- Read `docs/specs/10_checklists_and_dod.md`, `docs/specs/09_risks_non_goals_deferred.md`, and `docs/handoff/DECISION_LOG.md`.
- Read `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md` entries listed in `SPEC_MUST_IDS`.
- Preserve fixed gate order and single-task scope.
IMPLEMENTATION_SUBTASKS:
1. Add/verify failure-analysis template evidence for `C20-HYGIENE-05`.
2. Resolve remaining closeout-impacting Section B/C checklist statuses to `DONE` or explicit `BLOCKED` with rationale.
3. Classify every `STATUS: OPEN` decision as blocking/non-blocking for closeout acceptance and lock any resolved entries.
4. Update `SPEC_MUST_IDS` rows with final evidence state.
5. Run quality gates in fixed order and capture outcomes.
6. Update handoff docs for loop completion and continuity.
QUALITY_GATES:
1) Unit tests and/or smoke scripts
2) Type checking
3) Linting
4) Spec conformance check
5) Documentation + handoff updates
ACCEPTANCE_CRITERIA:
- [ ] `C20-HYGIENE-05` is no longer `NOT_STARTED` and includes concrete evidence.
- [ ] `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md` rows in `SPEC_MUST_IDS` are updated with current evidence/state.
- [ ] Open decision handling for closeout is explicitly reflected in `docs/handoff/DECISION_LOG.md` with continuity counts synchronized.
- [ ] `conda run -n emg python -m pytest -q` passes.
- [ ] `conda run -n emg python -m mypy src tests` passes.
- [ ] `conda run -n emg python -m ruff check src tests` passes.
- [ ] Handoff docs are updated and task IDs remain continuous.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q`
- `conda run -n emg python -m mypy src tests`
- `conda run -n emg python -m ruff check src tests`
- `rg "^TASK_ID:|^OWNER_CHECK_IDS:|^SPEC_MUST_IDS:" docs/handoff/NEXT_TASK.md`
- `rg "^NEXT_TASK_ID:|^ACTIVE_QUEUE_TASK_ID:" docs/handoff/CURRENT_STATUS.md`
- `rg "^TASK_ID:|^READY:" docs/handoff/TASK_QUEUE.md`
- `rg "^DECISION_ID:|^STATUS:" docs/handoff/DECISION_LOG.md`
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

# Agent Operations

This file is the canonical operational entrypoint for coding agents working in this repository.

## Purpose

Use this document for agent workflow rules. Human-oriented project overview and setup remain in `README.md`.

## Session Startup Order

1. Read `docs/handoff/CURRENT_STATUS.md`.
2. Read `docs/handoff/NEXT_TASK.md`.
3. Read `docs/handoff/TASK_QUEUE.md`.
4. Read `docs/handoff/DECISION_LOG.md`.
5. Read `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md`.
6. Read `docs/handoff/OVERVIEW_CHECKLIST.md`.
7. Read `docs/INDEX.md`.
8. If the active task touches policy/evaluation/baselines, read relevant `configs/*.yaml` files.
9. If task scope enters `tests/`, `scripts/`, or `configs/`, read the corresponding mini-index (`tests/TEST_INDEX.md`, `scripts/SCRIPTS_INDEX.md`, `configs/CONFIG_INDEX.md`).
10. Read only the relevant `PRIMARY_DOC` specification files required for the active task.

## Execution Loop Contract

- Execute exactly one primary task per cycle.
- Follow the fixed quality gate order:
  1. Unit tests and/or smoke scripts
  2. Type checking
  3. Linting
  4. Spec conformance check
  5. Documentation + handoff updates
- Update all handoff docs at end of cycle:
  - `docs/handoff/CURRENT_STATUS.md`
  - `docs/handoff/NEXT_TASK.md`
  - `docs/handoff/TASK_QUEUE.md`
  - `docs/handoff/DECISION_LOG.md`
  - `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md`
  - `docs/handoff/OVERVIEW_CHECKLIST.md`
- The active `docs/handoff/NEXT_TASK.md:TASK_ID` must be reflected in relevant
  `docs/handoff/OVERVIEW_CHECKLIST.md` `OWNER_TASK_ID` rows.

## Task Continuity

- `docs/handoff/NEXT_TASK.md:TASK_ID` must match `docs/handoff/CURRENT_STATUS.md:NEXT_TASK_ID`.
- `docs/handoff/CURRENT_STATUS.md:ACTIVE_QUEUE_TASK_ID` must match queue `READY: YES` `TASK_ID` in `docs/handoff/TASK_QUEUE.md`.
- Keep task IDs short and stable during a cycle.

## Checklist Continuity

- `docs/handoff/NEXT_TASK.md:TASK_ID` should appear as `OWNER_TASK_ID` for at
  least one `IN_PROGRESS` row in `docs/handoff/OVERVIEW_CHECKLIST.md`.
- `docs/handoff/NEXT_TASK.md:OWNER_CHECK_IDS` must reference valid `CHECK_ID` rows in `docs/handoff/OVERVIEW_CHECKLIST.md`.
- `docs/handoff/NEXT_TASK.md:SPEC_MUST_IDS` must reference valid `SPEC_MUST_ID` rows in `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md`.
- Only set `STATUS: DONE` when both `EXIT_CRITERIA` and `EVIDENCE` are satisfied.

## Decision Escalation Contract

- For each `STATUS: OPEN` row in `docs/handoff/DECISION_LOG.md`, classify impact on the active loop as `BLOCKING` or `NON_BLOCKING`.
- Treat a decision as `BLOCKING` only when active `NEXT_TASK.md` acceptance criteria, `OWNER_CHECK_IDS`, or `SPEC_MUST_IDS` cannot be completed without resolving that decision.
- If `NON_BLOCKING`, continue implementation without asking the user and keep the decision `OPEN`.
- Ask the user for a decision only when `BLOCKING`, and include `DECISION_ID`, affected scope, and consequence of each option.
- Do not escalate decisions outside active task scope unless they directly block a quality gate in the current loop.
- When resolved, set decision `STATUS: LOCKED`, fill `DECISION`, add `EVIDENCE`, and synchronize `OPEN_DECISIONS_COUNT` in `CURRENT_STATUS.md` and `DECISION_LOG.md`.

## Environment Usage

- Environment spec: `environment.yml`
- Environment name: `emg`
- Create/update commands:
  - `conda env create -f environment.yml`
  - `conda env update -f environment.yml --prune`
- Execute Python tooling via:
  - `conda run -n emg python -m pytest -q`
  - `conda run -n emg python -m mypy src tests`
  - `conda run -n emg python -m ruff check src tests`

## Config Baselines

- Policy defaults: `configs/policy_v0q.yaml` (scoring thresholds, transition constants, cadence/promotion gates)
- Evaluation defaults: `configs/eval_v0q.yaml` (stage gates, fairness requirements, claim thresholds)
- Baseline matrix defaults: `configs/baselines_v0q.yaml` (baseline systems and shared fairness inputs)

## Output Style Constraints

- Keep handoff updates brief and operational.
- Do not add historical narrative logs to handoff docs.
- Record gate outcomes as `PASS`, `FAIL`, or `UNKNOWN` with one-line reasons.
- Keep overview checklist updates concise and evidence-linked; no narrative history.

## Closeout Validation

Run before ending a cycle:

- `rg --files docs/handoff`
- `rg "^LAST_UPDATED:|^PROJECT_PHASE:|^REPO_BASELINE:|^NEXT_TASK_ID:|^ACTIVE_QUEUE_TASK_ID:|^OPEN_DECISIONS_COUNT:|^NEXT_TASK_READY:" docs/handoff/CURRENT_STATUS.md`
- `rg "^TASK_ID:|^OBJECTIVE:|^OWNER_CHECK_IDS:|^SPEC_MUST_IDS:|^IMPLEMENTATION_SUBTASKS:|^QUALITY_GATES:|^ACCEPTANCE_CRITERIA:|^VALIDATION_COMMANDS:" docs/handoff/NEXT_TASK.md`
- `rg "^TASK_ID:|^MILESTONE:|^OBJECTIVE:|^PREREQUISITES:|^PRIMARY_DOCS:|^TARGET_FILES:|^ACCEPTANCE_CRITERIA:|^VALIDATION_COMMANDS:|^READY:" docs/handoff/TASK_QUEUE.md`
- `rg "^DECISION_ID:|^STATUS:|^SOURCE_DOC:|^QUESTION:|^DECISION:|^OWNER_TASK_ID:|^EVIDENCE:" docs/handoff/DECISION_LOG.md`
- `rg "^SPEC_MUST_ID:|^SOURCE_SPEC:|^MUST_TEXT:|^STATUS:|^OWNER_TASK_ID:|^EVIDENCE:" docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md`
- `rg "^# v0 Overview Checklist|^## A\\. Build Milestones|^## B\\. Master Implementation Checklist|^## C\\. Definition of Done Readiness|^## D\\. Immediate Next Actions Tracking|^## Update Rules" docs/handoff/OVERVIEW_CHECKLIST.md`
- `rg "handoff_current_status|handoff_next_task|handoff_task_queue|handoff_decision_log|handoff_spec_conformance|agent_runtime_workflow" docs/INDEX.md`
- `rg "handoff_overview_checklist" docs/INDEX.md`
- `rg "configs/" AGENTS.md README.md docs/INDEX.md`

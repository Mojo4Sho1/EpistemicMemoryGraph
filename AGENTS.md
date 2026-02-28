# Agent Operations

This file is the canonical operational entrypoint for coding agents working in this repository.

## Purpose

Use this document for agent workflow rules. Human-oriented project overview and setup remain in `README.md`.

## Session Startup Order

1. Read `docs/handoff/CURRENT_STATUS.md`.
2. Read `docs/handoff/NEXT_TASK.md`.
3. Read `docs/handoff/OVERVIEW_CHECKLIST.md`.
4. Read `docs/INDEX.md`.
5. If the active task touches policy/evaluation/baselines, read relevant `configs/*.yaml` files.
6. Read only the relevant `PRIMARY_DOC` specification files required for the active task.

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
  - `docs/handoff/OVERVIEW_CHECKLIST.md`
- The active `docs/handoff/NEXT_TASK.md:TASK_ID` must be reflected in relevant
  `docs/handoff/OVERVIEW_CHECKLIST.md` `OWNER_TASK_ID` rows.

## Task Continuity

- `docs/handoff/NEXT_TASK.md:TASK_ID` must match `docs/handoff/CURRENT_STATUS.md:NEXT_TASK_ID`.
- Keep task IDs short and stable during a cycle.

## Checklist Continuity

- `docs/handoff/NEXT_TASK.md:TASK_ID` should appear as `OWNER_TASK_ID` for at
  least one `IN_PROGRESS` row in `docs/handoff/OVERVIEW_CHECKLIST.md`.
- Only set `STATUS: DONE` when both `EXIT_CRITERIA` and `EVIDENCE` are satisfied.

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
- `rg "^LAST_UPDATED:|^PROJECT_PHASE:|^REPO_BASELINE:|^NEXT_TASK_ID:|^NEXT_TASK_READY:" docs/handoff/CURRENT_STATUS.md`
- `rg "^TASK_ID:|^OBJECTIVE:|^IMPLEMENTATION_SUBTASKS:|^QUALITY_GATES:|^ACCEPTANCE_CRITERIA:|^VALIDATION_COMMANDS:" docs/handoff/NEXT_TASK.md`
- `rg "^# v0 Overview Checklist|^## A\\. Build Milestones|^## B\\. Master Implementation Checklist|^## C\\. Definition of Done Readiness|^## D\\. Immediate Next Actions Tracking|^## Update Rules" docs/handoff/OVERVIEW_CHECKLIST.md`
- `rg "handoff_current_status|handoff_next_task|agent_runtime_workflow" docs/INDEX.md`
- `rg "handoff_overview_checklist" docs/INDEX.md`
- `rg "configs/" AGENTS.md README.md docs/INDEX.md`

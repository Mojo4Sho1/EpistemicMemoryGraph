# Agent Operations

This file is the canonical operational entrypoint for coding agents working in this repository.

## Purpose

Use this document for agent workflow rules. Human-oriented project overview and setup remain in `README.md`.

## Session Startup Order

1. Read `docs/handoff/CURRENT_STATUS.md`.
2. Read `docs/handoff/NEXT_TASK.md`.
3. Read `docs/INDEX.md`.
4. Read only the relevant `PRIMARY_DOC` specification files required for the active task.

## Execution Loop Contract

- Execute exactly one primary task per cycle.
- Follow the fixed quality gate order:
  1. Unit tests and/or smoke scripts
  2. Type checking
  3. Linting
  4. Spec conformance check
  5. Documentation + handoff updates
- Update both handoff docs at end of cycle:
  - `docs/handoff/CURRENT_STATUS.md`
  - `docs/handoff/NEXT_TASK.md`

## Task Continuity

- `docs/handoff/NEXT_TASK.md:TASK_ID` must match `docs/handoff/CURRENT_STATUS.md:NEXT_TASK_ID`.
- Keep task IDs short and stable during a cycle.

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

## Output Style Constraints

- Keep handoff updates brief and operational.
- Do not add historical narrative logs to handoff docs.
- Record gate outcomes as `PASS`, `FAIL`, or `UNKNOWN` with one-line reasons.

## Closeout Validation

Run before ending a cycle:

- `rg --files docs/handoff`
- `rg "^LAST_UPDATED:|^PROJECT_PHASE:|^REPO_BASELINE:|^NEXT_TASK_ID:|^NEXT_TASK_READY:" docs/handoff/CURRENT_STATUS.md`
- `rg "^TASK_ID:|^OBJECTIVE:|^IMPLEMENTATION_SUBTASKS:|^QUALITY_GATES:|^ACCEPTANCE_CRITERIA:|^VALIDATION_COMMANDS:" docs/handoff/NEXT_TASK.md`
- `rg "handoff_current_status|handoff_next_task|agent_runtime_workflow" docs/INDEX.md`

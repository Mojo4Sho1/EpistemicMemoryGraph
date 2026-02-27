# Documentation System

This directory is the canonical documentation entrypoint for the v0 build.

- Start at `docs/INDEX.md` for keyword-based navigation.
- Use `docs/specs/` for decomposed, task-oriented specifications.
- Keep `MASTER_DOC.md` at repository root as the frozen source of truth.
- Agent runtime workflow and handoff-loop rules are defined in root `AGENTS.md`.

## Naming Convention

- Specs live in `docs/specs/`.
- Prefix spec files with zero-padded numeric order: `NN_topic_name.md`.
- Use lowercase snake case in filenames.
- Keep section headings stable to improve agent retrieval.

## Required Sections For Each Spec

Each spec in `docs/specs/` must include all of the following sections:

1. Purpose
2. Normative Requirements
3. Data Objects / Interfaces
4. Policy Rules / Constraints
5. Edge Cases and Failure Modes
6. Open Questions
7. Traceability to `MASTER_DOC.md`

Use explicit modal language:

- `MUST`: mandatory behavior or constraint
- `SHOULD`: recommended default with allowed exceptions
- `MAY`: optional behavior

## Traceability Rules

- Every normative claim must map to one or more source sections in `MASTER_DOC.md`.
- If a statement extends beyond `MASTER_DOC.md`, label it under `Open Questions`.
- Include a dedicated "Traceability" section in each spec with source section numbers.

## Update Policy

- Treat `MASTER_DOC.md` as canonical for v0 until an explicit version bump.
- Update decomposed specs in the same change when source intent changes.
- Update `docs/INDEX.md` whenever a new topic or spec file is added.
- Avoid moving files without updating all index references.

## Root-Only README Policy

- `README.md` is reserved for repository root only.
- Subdirectories must not use `README.md`.
- Use descriptive filenames in subdirectories, for example:
  - `*_GUIDE.md`
  - `*_POLICY.md`
  - `*_INDEX.md`
  - `*_TEMPLATE.md`

## Handoff Docs Structure

- Handoff docs are stored under `docs/handoff/`.
- Required files:
  - `docs/handoff/CURRENT_STATUS.md`
  - `docs/handoff/NEXT_TASK.md`
- Keep key naming stable for parser/grep reliability.
- For operational workflow policy (execution loop, gate order, closeout), use `AGENTS.md`.

## Lean Content Rule

- Prefer bullets over prose.
- Keep entries short and operational.
- Link to `docs/INDEX.md` or `docs/specs/*` instead of duplicating specification detail.

## Handoff Validation Checks

- `rg --files docs/handoff`
- `rg "^LAST_UPDATED:|^PROJECT_PHASE:|^REPO_BASELINE:|^NEXT_TASK_ID:|^NEXT_TASK_READY:" docs/handoff/CURRENT_STATUS.md`
- `rg "^TASK_ID:|^OBJECTIVE:|^IMPLEMENTATION_SUBTASKS:|^QUALITY_GATES:|^ACCEPTANCE_CRITERIA:|^VALIDATION_COMMANDS:" docs/handoff/NEXT_TASK.md`
- `rg "handoff_current_status|handoff_next_task|agent_runtime_workflow" docs/INDEX.md`
- `rg "AGENTS.md|handoff_current_status|handoff_next_task|agent_runtime_workflow" docs/INDEX.md docs/DOCS_GUIDE.md`

## Python Environment

- Root environment spec is `environment.yml`.
- Preferred environment name is `emg`.
- Create/update locally with:
  - `conda env create -f environment.yml`
  - `conda env update -f environment.yml --prune`
- Prefer executing Python tooling with:
  - `conda run -n emg python -m pytest -q`
  - `conda run -n emg python -m mypy src tests`
  - `conda run -n emg python -m ruff check src tests`

## Docs Navigation Guidance

- Prefer `rg "KEYWORDS:" docs/INDEX.md` to find topic blocks quickly.
- Read only the `PRIMARY_DOC` listed for a documentation task unless constraints require related docs.
- Use `SOURCE_SECTIONS` to confirm design intent against `MASTER_DOC.md`.

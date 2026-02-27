# Documentation System

This directory is the canonical documentation entrypoint for the v0 build.

- Start at `docs/INDEX.md` for keyword-based navigation.
- Use `docs/specs/` for decomposed, task-oriented specifications.
- Keep `MASTER_DOC.md` at repository root as the frozen source of truth.

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

## Handoff Docs Policy

- Handoff docs are required operational docs under `docs/handoff/`.
- Required files:
  - `docs/handoff/CURRENT_STATUS.md`
  - `docs/handoff/NEXT_TASK.md`
- Handoff docs are updated by the agent at the end of each substantive task.
- Exactly one primary task is allowed per loop in `docs/handoff/NEXT_TASK.md`.
- Keep strict key ordering and key names stable for parser/grep reliability.
- Use `TASK_ID`/`NEXT_TASK_ID` for continuity; values should be short and stable
  across a task cycle.
- `docs/handoff/NEXT_TASK.md` must include the fixed gate sequence:
  - tests/smoke
  - type checking
  - linting
  - spec conformance check
  - documentation + handoff updates
- Handoff docs must not contain historical run logs or long command transcripts.
- If a value is unknown, set it to `UNKNOWN`; do not remove required keys.

## Lean Content Rule

- Prefer bullets over prose.
- Keep entries short and operational.
- Link to `docs/INDEX.md` or `docs/specs/*` instead of duplicating specification detail.

## Handoff Validation Checks

- `rg --files docs/handoff`
- `rg "^LAST_UPDATED:|^PROJECT_PHASE:|^REPO_BASELINE:|^NEXT_TASK_ID:|^NEXT_TASK_READY:" docs/handoff/CURRENT_STATUS.md`
- `rg "^TASK_ID:|^OBJECTIVE:|^IMPLEMENTATION_SUBTASKS:|^QUALITY_GATES:|^ACCEPTANCE_CRITERIA:|^VALIDATION_COMMANDS:" docs/handoff/NEXT_TASK.md`
- `rg "handoff_current_status|handoff_next_task" docs/INDEX.md`
- `rg "single primary task|quality gates|blockers|validation commands" docs/INDEX.md docs/DOCS_GUIDE.md`

## Agent Navigation Guidance

- Prefer `rg "KEYWORDS:" docs/INDEX.md` to find topic blocks quickly.
- Read only the `PRIMARY_DOC` listed for a task unless constraints require related docs.
- Use `SOURCE_SECTIONS` to confirm design intent against `MASTER_DOC.md`.

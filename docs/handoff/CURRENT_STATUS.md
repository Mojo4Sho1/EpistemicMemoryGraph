# Current Status

LAST_UPDATED: 2026-03-02
PROJECT_PHASE: implementation
REPO_BASELINE: Repo includes deterministic v0.1q policy/scoring/state-transition/test-trigger modules, tool proposal schema validation, consolidation gate helpers, eval artifact/fairness schemas, frozen config baselines under `configs/`, composed workspace update boundaries, smoke/probe coverage, and expanded handoff controls (`TASK_QUEUE.md`, `DECISION_LOG.md`, `SPEC_CONFORMANCE_CHECKLIST.md`) for zero-context agent execution.
ACTIVE_PRIMARY_OBJECTIVE: Implement retrieval/reactivation workflow boundaries with deterministic canonical-subgraph loading interfaces.
STATUS_SUMMARY:
- Completed `identity-alias-possible-same-as-v0` with deterministic alias linking and `possible_same_as` ambiguity handling while preserving no-hard-auto-merge behavior.
- Advanced checklist coverage: `M5`, `C20-DATA-03`, and `C20-DATA-04` are now `DONE`; `C20-RUNTIME-04` is staged as `IN_PROGRESS` for the next retrieval task.
- Advanced spec conformance: `S02-M03` is now `SATISFIED` with identity-boundary evidence in models/constants/workspace update + tests.
- Maintained fixed-quality-gate compliance: focused + full pytest, `mypy`, and `ruff` all passed in this loop.
QUALITY_GATES:
- Unit tests and/or smoke scripts: PASS - `pytest -q tests/test_core_models.py tests/test_workspace_update.py` and full `pytest -q` passed.
- Type checking: PASS - `mypy src tests` reported no issues.
- Linting: PASS - `ruff check src tests` passed cleanly.
- Spec conformance check: PASS - referenced `SPEC_MUST_ID` rows updated to `SATISFIED` with evidence.
- Documentation + handoff updates: PASS - queue/task continuity and checklist/spec references synchronized.
BLOCKERS: NONE
DECISIONS_LOCKED:
- Keep single primary task per loop.
- Keep fixed quality gate order in every loop.
- Freeze v0.1q scoring constants, state thresholds, and transition precedence in deterministic code and specs.
- Use ordered hard rules for hypothesis-test triggers plus low-impact cost suppression.
- Use consolidation cadence at task boundary plus every 25 observations.
- Cap unresolved carryover at 20 propositions per task with overflow archival reason code.
- Require accepted state plus freshness >= 0.35 for promotion eligibility.
- Enforce baseline fairness parity (model/prompt/tools/budget/timeout/seeds).
- Require reproducibility hash and fixed artifact file set per benchmark run.
- Keep workspace update indexing idempotent per `(session_id, task_id, observation_id)` in composed boundary calls.
- Keep smoke tests and probe output deterministic for stable diagnostics.
- Require queue-driven continuity across `NEXT_TASK_ID`, `ACTIVE_QUEUE_TASK_ID`, and queue `READY: YES` row.
- Keep consolidation cadence fixed at task boundary OR every 25 observations (DEC-0003).
DECISIONS_PENDING:
- Resolve 11 open spec questions tracked in `docs/handoff/DECISION_LOG.md`.
- Decide whether proposition structured form normalization is in-scope for v0 (`DEC-0005`) and whether episode schema needs retention class tags (`DEC-0006`).
RISKS_ACTIVE:
- Runtime retrieval/reactivation milestone remains incomplete pending deterministic boundary + coverage implementation (`C20-RUNTIME-04`, `C21-02`).
- Evaluation milestones M9/M10 remain `NOT_STARTED` until runnable baseline and stress harness implementations are added.
NEXT_TASK_ID: retrieval-reactivation-boundary-v0
ACTIVE_QUEUE_TASK_ID: retrieval-reactivation-boundary-v0
OPEN_DECISIONS_COUNT: 11
NEXT_TASK_READY: YES
REQUIRED_REFERENCES:
1. `docs/handoff/NEXT_TASK.md`
2. `docs/handoff/TASK_QUEUE.md`
3. `docs/handoff/OVERVIEW_CHECKLIST.md`
4. `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md`
5. `docs/handoff/DECISION_LOG.md`
6. `docs/specs/01_architecture_overview.md`
7. `docs/specs/05_operational_flows.md`
8. `docs/specs/02_data_model.md`
9. `docs/specs/10_checklists_and_dod.md`
10. `tests/TEST_INDEX.md`
11. `docs/INDEX.md`
ASSUMPTIONS:
- Python runtime remains available for local command execution.
- Frozen policy/eval/baseline defaults remain unchanged during retrieval/reactivation boundary work.
- Open spec questions remain `OPEN` until explicitly locked with evidence.
HANDOFF_INSTRUCTIONS:
- Read this file first, then execute `docs/handoff/NEXT_TASK.md` exactly.
- Keep scope to one primary task and listed target files.
- Record gate outcomes as PASS/FAIL/UNKNOWN with one-line reasons.
- Keep task continuity synchronized with `docs/handoff/TASK_QUEUE.md`.
- Update handoff docs before ending the loop.
- Keep entries concise; no narrative history or command transcripts.

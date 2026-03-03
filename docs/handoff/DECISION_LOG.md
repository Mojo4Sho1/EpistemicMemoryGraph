# Decision Log

LAST_UPDATED: 2026-03-03
OPEN_DECISIONS_COUNT: 11

## Status Legend
- `OPEN`: unresolved question requiring explicit task closure
- `LOCKED`: resolved decision with linked implementation/doc evidence

## Decisions
DECISION_ID: DEC-0001
STATUS: OPEN
SOURCE_DOC: `docs/specs/00_scope_and_claim.md`
QUESTION: Should a formal v0.1 changelog file be added in `docs/` for scope updates?
DECISION: TBD
OWNER_TASK_ID: dod-evidence-closeout-v0
EVIDENCE: PENDING (`docs/` changelog policy or explicit defer entry)
ACTIVE_LOOP_IMPACT: NON_BLOCKING

DECISION_ID: DEC-0002
STATUS: OPEN
SOURCE_DOC: `docs/specs/00_scope_and_claim.md`
QUESTION: Should non-goals be tagged by "defer until" milestone for planning clarity?
DECISION: TBD
OWNER_TASK_ID: dod-evidence-closeout-v0
EVIDENCE: PENDING (`docs/specs/09_risks_non_goals_deferred.md` tag policy)
ACTIVE_LOOP_IMPACT: NON_BLOCKING

DECISION_ID: DEC-0003
STATUS: LOCKED
SOURCE_DOC: `docs/specs/01_architecture_overview.md`
QUESTION: Should checkpoint cadence for consolidation be fixed or task-adaptive in v0?
DECISION: Keep fixed cadence in v0.1q (task boundary OR every 25 observations), not task-adaptive cadence.
OWNER_TASK_ID: consolidation-archival-determinism-v0
EVIDENCE: `docs/specs/05_operational_flows.md`; `src/workspace/consolidation.py`; `tests/test_workspace_consolidation.py`

DECISION_ID: DEC-0004
STATUS: OPEN
SOURCE_DOC: `docs/specs/01_architecture_overview.md`
QUESTION: Should workspace eviction thresholds be configurable by domain volatility at v0 launch?
DECISION: TBD
OWNER_TASK_ID: retrieval-reactivation-boundary-v0
EVIDENCE: Retrieval/reactivation boundary now implemented (`src/workspace/reactivation.py`, `tests/test_workspace_state.py`); volatility-configurable eviction remains pending.
ACTIVE_LOOP_IMPACT: NON_BLOCKING

DECISION_ID: DEC-0005
STATUS: OPEN
SOURCE_DOC: `docs/specs/02_data_model.md`
QUESTION: Should proposition structured form be normalized in v0 or deferred to v0.2?
DECISION: TBD
OWNER_TASK_ID: dod-evidence-closeout-v0
EVIDENCE: NON_BLOCKING for `identity-alias-possible-same-as-v0`; deferred schema decision pending closeout policy.
ACTIVE_LOOP_IMPACT: NON_BLOCKING

DECISION_ID: DEC-0006
STATUS: OPEN
SOURCE_DOC: `docs/specs/02_data_model.md`
QUESTION: Should episode schema include explicit retention class tags at launch?
DECISION: TBD
OWNER_TASK_ID: consolidation-archival-determinism-v0
EVIDENCE: PENDING (episode schema + archival test coverage)
ACTIVE_LOOP_IMPACT: NON_BLOCKING

DECISION_ID: DEC-0007
STATUS: OPEN
SOURCE_DOC: `docs/specs/07_build_plan_and_milestones.md`
QUESTION: Should milestone completion require explicit sign-off checklists in repo issues?
DECISION: TBD
OWNER_TASK_ID: dod-evidence-closeout-v0
EVIDENCE: PENDING (process policy documented in `AGENTS.md` or handoff docs)
ACTIVE_LOOP_IMPACT: NON_BLOCKING

DECISION_ID: DEC-0008
STATUS: OPEN
SOURCE_DOC: `docs/specs/07_build_plan_and_milestones.md`
QUESTION: Should benchmark harness scaffolding begin in parallel with policy tests or strictly after?
DECISION: TBD
OWNER_TASK_ID: governance-stress-suite-v0
EVIDENCE: PENDING (queue dependency update + rationale in `TASK_QUEUE.md`)
ACTIVE_LOOP_IMPACT: NON_BLOCKING

DECISION_ID: DEC-0009
STATUS: OPEN
SOURCE_DOC: `docs/specs/08_evaluation_and_metrics.md`
QUESTION: Confidence calibration visualizations are optional in v0.1q; scalar metrics remain required.
DECISION: TBD
OWNER_TASK_ID: baseline-comparison-claims-v0
EVIDENCE: PENDING (report schema decision in eval docs)
ACTIVE_LOOP_IMPACT: NON_BLOCKING

DECISION_ID: DEC-0010
STATUS: OPEN
SOURCE_DOC: `docs/specs/08_evaluation_and_metrics.md`
QUESTION: Minimal smoke tests and developer probe scripts are intentionally deferred until `workspace-update-boundary-v0q-v0` is implemented.
DECISION: TBD
OWNER_TASK_ID: governance-stress-suite-v0
EVIDENCE: PENDING (`tests/TEST_INDEX.md` + `scripts/SCRIPTS_INDEX.md` expansion policy)
ACTIVE_LOOP_IMPACT: NON_BLOCKING

DECISION_ID: DEC-0011
STATUS: OPEN
SOURCE_DOC: `docs/specs/09_risks_non_goals_deferred.md`
QUESTION: Should each known risk get a mapped detection metric owner during implementation?
DECISION: TBD
OWNER_TASK_ID: dod-evidence-closeout-v0
EVIDENCE: PENDING (risk-to-metric owner matrix)
ACTIVE_LOOP_IMPACT: NON_BLOCKING

DECISION_ID: DEC-0012
STATUS: OPEN
SOURCE_DOC: `docs/specs/09_risks_non_goals_deferred.md`
QUESTION: Should deferred features be tagged with dependency prerequisites for post-v0 planning?
DECISION: TBD
OWNER_TASK_ID: dod-evidence-closeout-v0
EVIDENCE: PENDING (deferred-feature dependency tags)
ACTIVE_LOOP_IMPACT: NON_BLOCKING

## Update Rules
- Every non-`None` spec open question must appear exactly once in this file.
- `OPEN_DECISIONS_COUNT` must equal the number of `STATUS: OPEN` entries.
- Escalate an `OPEN` decision to the user only when it blocks active `NEXT_TASK.md` acceptance criteria, `OWNER_CHECK_IDS`, or `SPEC_MUST_IDS`.
- If an `OPEN` decision is non-blocking for active scope, keep it `OPEN` and proceed with task execution.
- Lock decisions only with explicit evidence links.

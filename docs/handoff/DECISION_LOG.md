# Decision Log

LAST_UPDATED: 2026-03-02
OPEN_DECISIONS_COUNT: 12

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

DECISION_ID: DEC-0002
STATUS: OPEN
SOURCE_DOC: `docs/specs/00_scope_and_claim.md`
QUESTION: Should non-goals be tagged by "defer until" milestone for planning clarity?
DECISION: TBD
OWNER_TASK_ID: dod-evidence-closeout-v0
EVIDENCE: PENDING (`docs/specs/09_risks_non_goals_deferred.md` tag policy)

DECISION_ID: DEC-0003
STATUS: OPEN
SOURCE_DOC: `docs/specs/01_architecture_overview.md`
QUESTION: Should checkpoint cadence for consolidation be fixed or task-adaptive in v0?
DECISION: TBD
OWNER_TASK_ID: consolidation-archival-determinism-v0
EVIDENCE: PENDING (`docs/specs/01_architecture_overview.md` + tests for chosen mode)

DECISION_ID: DEC-0004
STATUS: OPEN
SOURCE_DOC: `docs/specs/01_architecture_overview.md`
QUESTION: Should workspace eviction thresholds be configurable by domain volatility at v0 launch?
DECISION: TBD
OWNER_TASK_ID: retrieval-reactivation-boundary-v0
EVIDENCE: PENDING (runtime config + boundary tests)

DECISION_ID: DEC-0005
STATUS: OPEN
SOURCE_DOC: `docs/specs/02_data_model.md`
QUESTION: Should proposition structured form be normalized in v0 or deferred to v0.2?
DECISION: TBD
OWNER_TASK_ID: identity-alias-possible-same-as-v0
EVIDENCE: PENDING (data-model update + migration/test note)

DECISION_ID: DEC-0006
STATUS: OPEN
SOURCE_DOC: `docs/specs/02_data_model.md`
QUESTION: Should episode schema include explicit retention class tags at launch?
DECISION: TBD
OWNER_TASK_ID: consolidation-archival-determinism-v0
EVIDENCE: PENDING (episode schema + archival test coverage)

DECISION_ID: DEC-0007
STATUS: OPEN
SOURCE_DOC: `docs/specs/07_build_plan_and_milestones.md`
QUESTION: Should milestone completion require explicit sign-off checklists in repo issues?
DECISION: TBD
OWNER_TASK_ID: dod-evidence-closeout-v0
EVIDENCE: PENDING (process policy documented in `AGENTS.md` or handoff docs)

DECISION_ID: DEC-0008
STATUS: OPEN
SOURCE_DOC: `docs/specs/07_build_plan_and_milestones.md`
QUESTION: Should benchmark harness scaffolding begin in parallel with policy tests or strictly after?
DECISION: TBD
OWNER_TASK_ID: governance-stress-suite-v0
EVIDENCE: PENDING (queue dependency update + rationale in `TASK_QUEUE.md`)

DECISION_ID: DEC-0009
STATUS: OPEN
SOURCE_DOC: `docs/specs/08_evaluation_and_metrics.md`
QUESTION: Confidence calibration visualizations are optional in v0.1q; scalar metrics remain required.
DECISION: TBD
OWNER_TASK_ID: baseline-comparison-claims-v0
EVIDENCE: PENDING (report schema decision in eval docs)

DECISION_ID: DEC-0010
STATUS: OPEN
SOURCE_DOC: `docs/specs/08_evaluation_and_metrics.md`
QUESTION: Minimal smoke tests and developer probe scripts are intentionally deferred until `workspace-update-boundary-v0q-v0` is implemented.
DECISION: TBD
OWNER_TASK_ID: governance-stress-suite-v0
EVIDENCE: PENDING (`tests/TEST_INDEX.md` + `scripts/SCRIPTS_INDEX.md` expansion policy)

DECISION_ID: DEC-0011
STATUS: OPEN
SOURCE_DOC: `docs/specs/09_risks_non_goals_deferred.md`
QUESTION: Should each known risk get a mapped detection metric owner during implementation?
DECISION: TBD
OWNER_TASK_ID: dod-evidence-closeout-v0
EVIDENCE: PENDING (risk-to-metric owner matrix)

DECISION_ID: DEC-0012
STATUS: OPEN
SOURCE_DOC: `docs/specs/09_risks_non_goals_deferred.md`
QUESTION: Should deferred features be tagged with dependency prerequisites for post-v0 planning?
DECISION: TBD
OWNER_TASK_ID: dod-evidence-closeout-v0
EVIDENCE: PENDING (deferred-feature dependency tags)

## Update Rules
- Every non-`None` spec open question must appear exactly once in this file.
- `OPEN_DECISIONS_COUNT` must equal the number of `STATUS: OPEN` entries.
- Escalate an `OPEN` decision to the user only when it blocks active `NEXT_TASK.md` acceptance criteria, `OWNER_CHECK_IDS`, or `SPEC_MUST_IDS`.
- If an `OPEN` decision is non-blocking for active scope, keep it `OPEN` and proceed with task execution.
- Lock decisions only with explicit evidence links.

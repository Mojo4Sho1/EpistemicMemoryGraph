# Spec Conformance Checklist

LAST_UPDATED: 2026-03-02

## Status Legend
- `SATISFIED`: implemented and evidenced
- `IN_PROGRESS`: partially implemented/evidenced
- `NOT_STARTED`: no implementation evidence yet

## Spec 00 (`docs/specs/00_scope_and_claim.md`)
SPEC_MUST_ID: S00-M01
SOURCE_SPEC: `docs/specs/00_scope_and_claim.md`
MUST_TEXT: Preserve the primary research claim for observation-to-proposition-to-belief governance improvement over naive baselines.
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `MASTER_DOC.md` sections 2-3; `docs/specs/00_scope_and_claim.md`

SPEC_MUST_ID: S00-M02
SOURCE_SPEC: `docs/specs/00_scope_and_claim.md`
MUST_TEXT: Keep v0 scoped to a single-agent prototype with text/tool inputs.
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `MASTER_DOC.md` section 4; `docs/specs/00_scope_and_claim.md`

SPEC_MUST_ID: S00-M03
SOURCE_SPEC: `docs/specs/00_scope_and_claim.md`
MUST_TEXT: Do not include deferred capabilities in v0 acceptance criteria.
STATUS: SATISFIED
OWNER_TASK_ID: dod-evidence-closeout-v0
EVIDENCE: `MASTER_DOC.md` sections 4.2, 22; `docs/specs/09_risks_non_goals_deferred.md`; `docs/handoff/OVERVIEW_CHECKLIST.md`

## Spec 01 (`docs/specs/01_architecture_overview.md`)
SPEC_MUST_ID: S01-M01
SOURCE_SPEC: `docs/specs/01_architecture_overview.md`
MUST_TEXT: Implement three distinct layers: immutable observation log, transient workspace, canonical long-term memory graph.
STATUS: IN_PROGRESS
OWNER_TASK_ID: retrieval-reactivation-boundary-v0
EVIDENCE: `src/store/observation_store.py`; `src/workspace/state.py`; `docs/specs/01_architecture_overview.md`

SPEC_MUST_ID: S01-M02
SOURCE_SPEC: `docs/specs/01_architecture_overview.md`
MUST_TEXT: Ingest all external input as observations before interpretation.
STATUS: SATISFIED
OWNER_TASK_ID: workspace-update-boundary-v0q-v0
EVIDENCE: `src/workspace/intake.py`; `src/workspace/update.py`; `tests/test_workspace_intake.py`

SPEC_MUST_ID: S01-M03
SOURCE_SPEC: `docs/specs/01_architecture_overview.md`
MUST_TEXT: Keep workspace transient and high-churn.
STATUS: SATISFIED
OWNER_TASK_ID: workspace-update-boundary-v0q-v0
EVIDENCE: `src/workspace/state.py`; `docs/specs/01_architecture_overview.md`

SPEC_MUST_ID: S01-M04
SOURCE_SPEC: `docs/specs/01_architecture_overview.md`
MUST_TEXT: Treat canonical memory as policy-gated durable state.
STATUS: IN_PROGRESS
OWNER_TASK_ID: retrieval-reactivation-boundary-v0
EVIDENCE: `docs/specs/01_architecture_overview.md`; `docs/specs/06_tool_boundary_and_interfaces.md`

## Spec 02 (`docs/specs/02_data_model.md`)
SPEC_MUST_ID: S02-M01
SOURCE_SPEC: `docs/specs/02_data_model.md`
MUST_TEXT: Represent observations as immutable evidence objects.
STATUS: SATISFIED
OWNER_TASK_ID: observation-sqlite-store-v0
EVIDENCE: `src/core/models.py`; `src/store/observation_store.py`; `tests/test_observation_store.py`

SPEC_MUST_ID: S02-M02
SOURCE_SPEC: `docs/specs/02_data_model.md`
MUST_TEXT: Model propositions as first-class claims with state/score metadata.
STATUS: SATISFIED
OWNER_TASK_ID: core-model-primitives-v0
EVIDENCE: `src/core/models.py`; `src/core/scoring.py`; `src/core/state_machine.py`; `tests/test_core_models.py`

SPEC_MUST_ID: S02-M03
SOURCE_SPEC: `docs/specs/02_data_model.md`
MUST_TEXT: Anchor graph structure on entities and explicit edge types.
STATUS: IN_PROGRESS
OWNER_TASK_ID: identity-alias-possible-same-as-v0
EVIDENCE: `src/core/models.py`; `src/core/constants.py`; `tests/test_scaffold_imports.py`

SPEC_MUST_ID: S02-M04
SOURCE_SPEC: `docs/specs/02_data_model.md`
MUST_TEXT: Include episode-level context for bounded task history.
STATUS: IN_PROGRESS
OWNER_TASK_ID: consolidation-archival-determinism-v0
EVIDENCE: `docs/specs/02_data_model.md`; `src/eval/schemas.py`

## Spec 03 (`docs/specs/03_policy_and_state_machine.md`)
SPEC_MUST_ID: S03-M01
SOURCE_SPEC: `docs/specs/03_policy_and_state_machine.md`
MUST_TEXT: Enforce the ten governance rules in policy code.
STATUS: IN_PROGRESS
OWNER_TASK_ID: retrieval-reactivation-boundary-v0
EVIDENCE: `docs/specs/03_policy_and_state_machine.md`; `src/core/state_machine.py`; `src/tools/schemas.py`

SPEC_MUST_ID: S03-M02
SOURCE_SPEC: `docs/specs/03_policy_and_state_machine.md`
MUST_TEXT: Place every proposition in exactly one primary state.
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `src/core/state_machine.py`; `tests/test_state_machine.py`

SPEC_MUST_ID: S03-M03
SOURCE_SPEC: `docs/specs/03_policy_and_state_machine.md`
MUST_TEXT: Derive belief state from evidence signals rather than direct LLM assertion.
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `src/core/scoring.py`; `src/core/state_machine.py`; `tests/test_state_machine.py`

SPEC_MUST_ID: S03-M04
SOURCE_SPEC: `docs/specs/03_policy_and_state_machine.md`
MUST_TEXT: Preserve contradictory history; contradictions cannot erase prior evidence.
STATUS: SATISFIED
OWNER_TASK_ID: policy-correctness-micro-suite-v0
EVIDENCE: `src/core/state_machine.py`; `tests/test_state_machine.py`

SPEC_MUST_ID: S03-M05
SOURCE_SPEC: `docs/specs/03_policy_and_state_machine.md`
MUST_TEXT: Use fixed transition precedence `rejected -> contested -> accepted -> deprecated -> provisional -> tentative`.
STATUS: SATISFIED
OWNER_TASK_ID: policy-correctness-micro-suite-v0
EVIDENCE: `src/core/state_machine.py`; `tests/test_state_machine.py`

SPEC_MUST_ID: S03-M06
SOURCE_SPEC: `docs/specs/03_policy_and_state_machine.md`
MUST_TEXT: Apply frozen v0.1q transition thresholds for accepted/provisional/contested/rejected/deprecated rules.
STATUS: SATISFIED
OWNER_TASK_ID: policy-correctness-micro-suite-v0
EVIDENCE: `configs/policy_v0q.yaml`; `src/core/policy_config.py`; `src/core/state_machine.py`; `tests/test_state_machine.py`

## Spec 04 (`docs/specs/04_scoring_and_trust.md`)
SPEC_MUST_ID: S04-M01
SOURCE_SPEC: `docs/specs/04_scoring_and_trust.md`
MUST_TEXT: Keep scoring deterministic and inspectable.
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `src/core/scoring.py`; `tests/test_policy_scoring.py`

SPEC_MUST_ID: S04-M02
SOURCE_SPEC: `docs/specs/04_scoring_and_trust.md`
MUST_TEXT: Track support, contradiction, source-group diversity, freshness, and volatility modifiers.
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `src/core/scoring.py`; `tests/test_policy_scoring.py`

SPEC_MUST_ID: S04-M03
SOURCE_SPEC: `docs/specs/04_scoring_and_trust.md`
MUST_TEXT: Saturate repeated reinforcement from the same independence group with 0.70/+0.20/+0.10 capped at 1.00.
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `src/core/policy_config.py`; `src/core/scoring.py`; `tests/test_policy_scoring.py`

SPEC_MUST_ID: S04-M04
SOURCE_SPEC: `docs/specs/04_scoring_and_trust.md`
MUST_TEXT: Compute freshness using `exp(-ln(2) * age_hours / half_life_hours)`.
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `src/core/scoring.py`; `tests/test_policy_scoring.py`

SPEC_MUST_ID: S04-M05
SOURCE_SPEC: `docs/specs/04_scoring_and_trust.md`
MUST_TEXT: Freeze volatility tiers and half-life defaults (`low=168`, `medium=72`, `high=24`).
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `configs/policy_v0q.yaml`; `src/core/policy_config.py`

SPEC_MUST_ID: S04-M06
SOURCE_SPEC: `docs/specs/04_scoring_and_trust.md`
MUST_TEXT: Freeze volatility factors for staleness penalty (`low=0.5`, `medium=1.0`, `high=2.0`).
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `configs/policy_v0q.yaml`; `src/core/policy_config.py`

SPEC_MUST_ID: S04-M07
SOURCE_SPEC: `docs/specs/04_scoring_and_trust.md`
MUST_TEXT: Compute confidence with frozen weighted formula and clamp bounds.
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `src/core/scoring.py`; `tests/test_policy_scoring.py`

SPEC_MUST_ID: S04-M08
SOURCE_SPEC: `docs/specs/04_scoring_and_trust.md`
MUST_TEXT: Compute diversity bonus as `min(0.15, 0.05*(distinct_support_groups-1))`.
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `src/core/scoring.py`; `tests/test_policy_scoring.py`

SPEC_MUST_ID: S04-M09
SOURCE_SPEC: `docs/specs/04_scoring_and_trust.md`
MUST_TEXT: Compute staleness penalty as `min(0.30, (1-freshness)*volatility_factor*0.30)`.
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `src/core/scoring.py`; `tests/test_policy_scoring.py`

## Spec 05 (`docs/specs/05_operational_flows.md`)
SPEC_MUST_ID: S05-M01
SOURCE_SPEC: `docs/specs/05_operational_flows.md`
MUST_TEXT: Execute intake order: receive input -> record observations -> parse references/claims -> attach to workspace.
STATUS: IN_PROGRESS
OWNER_TASK_ID: retrieval-reactivation-boundary-v0
EVIDENCE: `src/workspace/intake.py`; `src/workspace/update.py`; `docs/specs/05_operational_flows.md`

SPEC_MUST_ID: S05-M02
SOURCE_SPEC: `docs/specs/05_operational_flows.md`
MUST_TEXT: Evaluate reinforcement/contradiction before spawning new candidates.
STATUS: NOT_STARTED
OWNER_TASK_ID: retrieval-reactivation-boundary-v0
EVIDENCE: NONE

SPEC_MUST_ID: S05-M03
SOURCE_SPEC: `docs/specs/05_operational_flows.md`
MUST_TEXT: Gate hypothesis testing on ordered hard trigger rules.
STATUS: SATISFIED
OWNER_TASK_ID: policy-correctness-micro-suite-v0
EVIDENCE: `src/core/test_trigger.py`; `tests/test_test_trigger.py`

SPEC_MUST_ID: S05-M04
SOURCE_SPEC: `docs/specs/05_operational_flows.md`
MUST_TEXT: Trigger testing when any required hard condition is met.
STATUS: SATISFIED
OWNER_TASK_ID: policy-correctness-micro-suite-v0
EVIDENCE: `src/core/test_trigger.py`; `tests/test_test_trigger.py`

SPEC_MUST_ID: S05-M05
SOURCE_SPEC: `docs/specs/05_operational_flows.md`
MUST_TEXT: Suppress testing when action impact is low and estimated test cost exceeds bounded benefit score.
STATUS: SATISFIED
OWNER_TASK_ID: policy-correctness-micro-suite-v0
EVIDENCE: `src/core/test_trigger.py`; `tests/test_test_trigger.py`

SPEC_MUST_ID: S05-M06
SOURCE_SPEC: `docs/specs/05_operational_flows.md`
MUST_TEXT: Consolidate at task boundaries or every 25 new observations.
STATUS: SATISFIED
OWNER_TASK_ID: consolidation-archival-determinism-v0
EVIDENCE: `src/workspace/consolidation.py`; `tests/test_workspace_consolidation.py`

SPEC_MUST_ID: S05-M07
SOURCE_SPEC: `docs/specs/05_operational_flows.md`
MUST_TEXT: Cap unresolved carryover at 20 propositions per task and archive overflow with reason code.
STATUS: SATISFIED
OWNER_TASK_ID: consolidation-archival-determinism-v0
EVIDENCE: `src/workspace/consolidation.py`; `tests/test_workspace_consolidation.py`

SPEC_MUST_ID: S05-M08
SOURCE_SPEC: `docs/specs/05_operational_flows.md`
MUST_TEXT: Require accepted state plus freshness >= 0.35 for canonical promotion.
STATUS: SATISFIED
OWNER_TASK_ID: consolidation-archival-determinism-v0
EVIDENCE: `src/workspace/consolidation.py`; `tests/test_workspace_consolidation.py`; `configs/policy_v0q.yaml`

## Spec 06 (`docs/specs/06_tool_boundary_and_interfaces.md`)
SPEC_MUST_ID: S06-M01
SOURCE_SPEC: `docs/specs/06_tool_boundary_and_interfaces.md`
MUST_TEXT: Treat all tool calls as proposals.
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `src/tools/schemas.py`; `tests/test_tool_schemas.py`

SPEC_MUST_ID: S06-M02
SOURCE_SPEC: `docs/specs/06_tool_boundary_and_interfaces.md`
MUST_TEXT: Validate proposals through deterministic policy code before durable writes.
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `src/tools/schemas.py`; `tests/test_tool_schemas.py`

SPEC_MUST_ID: S06-M03
SOURCE_SPEC: `docs/specs/06_tool_boundary_and_interfaces.md`
MUST_TEXT: Prevent direct LLM writes to canonical memory.
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `src/tools/schemas.py`; `tests/test_tool_schemas.py`

SPEC_MUST_ID: S06-M04
SOURCE_SPEC: `docs/specs/06_tool_boundary_and_interfaces.md`
MUST_TEXT: Preserve provenance links for all durable mutations.
STATUS: IN_PROGRESS
OWNER_TASK_ID: retrieval-reactivation-boundary-v0
EVIDENCE: `src/tools/schemas.py`; `src/workspace/update.py`; `tests/test_tool_schemas.py`

SPEC_MUST_ID: S06-M05
SOURCE_SPEC: `docs/specs/06_tool_boundary_and_interfaces.md`
MUST_TEXT: Expose validation outcomes as accepted, rejected_with_reason, or transformed.
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `src/tools/schemas.py`; `tests/test_tool_schemas.py`

SPEC_MUST_ID: S06-M06
SOURCE_SPEC: `docs/specs/06_tool_boundary_and_interfaces.md`
MUST_TEXT: Use fixed rejection code enum values for deterministic rejection semantics.
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `src/tools/schemas.py`; `tests/test_tool_schemas.py`

## Spec 07 (`docs/specs/07_build_plan_and_milestones.md`)
SPEC_MUST_ID: S07-M01
SOURCE_SPEC: `docs/specs/07_build_plan_and_milestones.md`
MUST_TEXT: Implement persistence and policy boundary before higher-level agent behavior.
STATUS: SATISFIED
OWNER_TASK_ID: workspace-update-boundary-v0q-v0
EVIDENCE: `src/store/observation_store.py`; `src/workspace/update.py`; `docs/handoff/OVERVIEW_CHECKLIST.md`

SPEC_MUST_ID: S07-M02
SOURCE_SPEC: `docs/specs/07_build_plan_and_milestones.md`
MUST_TEXT: Prioritize schema/policy freeze before benchmark expansion.
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `docs/specs/03_policy_and_state_machine.md`; `docs/specs/04_scoring_and_trust.md`; `configs/policy_v0q.yaml`

SPEC_MUST_ID: S07-M03
SOURCE_SPEC: `docs/specs/07_build_plan_and_milestones.md`
MUST_TEXT: Complete policy correctness suite before baseline comparison claims.
STATUS: SATISFIED
OWNER_TASK_ID: policy-correctness-micro-suite-v0
EVIDENCE: `tests/test_policy_scoring.py`; `tests/test_state_machine.py`; `tests/test_test_trigger.py`; `docs/handoff/OVERVIEW_CHECKLIST.md`

## Spec 08 (`docs/specs/08_evaluation_and_metrics.md`)
SPEC_MUST_ID: S08-M01
SOURCE_SPEC: `docs/specs/08_evaluation_and_metrics.md`
MUST_TEXT: Run staged evaluation in order: policy correctness -> governance stress -> baseline comparison -> end-to-end study.
STATUS: IN_PROGRESS
OWNER_TASK_ID: governance-stress-suite-v0
EVIDENCE: `configs/eval_v0q.yaml`; `docs/specs/08_evaluation_and_metrics.md`

SPEC_MUST_ID: S08-M02
SOURCE_SPEC: `docs/specs/08_evaluation_and_metrics.md`
MUST_TEXT: Include required ablations to isolate governance components.
STATUS: NOT_STARTED
OWNER_TASK_ID: baseline-comparison-claims-v0
EVIDENCE: NONE

SPEC_MUST_ID: S08-M03
SOURCE_SPEC: `docs/specs/08_evaluation_and_metrics.md`
MUST_TEXT: Record machine-readable run artifacts with configs, seeds, timestamps, and system version.
STATUS: IN_PROGRESS
OWNER_TASK_ID: governance-stress-suite-v0
EVIDENCE: `src/eval/schemas.py`; `src/eval/artifacts.py`; `tests/test_eval_artifacts.py`

SPEC_MUST_ID: S08-M04
SOURCE_SPEC: `docs/specs/08_evaluation_and_metrics.md`
MUST_TEXT: Log proposition transitions with triggering evidence and deterministic rule ids.
STATUS: IN_PROGRESS
OWNER_TASK_ID: governance-stress-suite-v0
EVIDENCE: `src/eval/schemas.py`; `tests/test_eval_artifacts.py`

SPEC_MUST_ID: S08-M05
SOURCE_SPEC: `docs/specs/08_evaluation_and_metrics.md`
MUST_TEXT: Enforce Stage 1 pass criterion of 100% expected deterministic transitions.
STATUS: SATISFIED
OWNER_TASK_ID: policy-correctness-micro-suite-v0
EVIDENCE: `tests/test_policy_scoring.py`; `tests/test_state_machine.py`; `tests/test_test_trigger.py`; `configs/eval_v0q.yaml`

SPEC_MUST_ID: S08-M06
SOURCE_SPEC: `docs/specs/08_evaluation_and_metrics.md`
MUST_TEXT: Run Stage 2 stress with five fixed seeds and identical scenario bundles per system.
STATUS: NOT_STARTED
OWNER_TASK_ID: governance-stress-suite-v0
EVIDENCE: `configs/eval_v0q.yaml`

SPEC_MUST_ID: S08-M07
SOURCE_SPEC: `docs/specs/08_evaluation_and_metrics.md`
MUST_TEXT: Enforce Stage 3 fairness parity across compared systems.
STATUS: IN_PROGRESS
OWNER_TASK_ID: baseline-variants-core-v0
EVIDENCE: `configs/eval_v0q.yaml`; `src/eval/fairness.py`; `tests/test_eval_fairness.py`

SPEC_MUST_ID: S08-M08
SOURCE_SPEC: `docs/specs/08_evaluation_and_metrics.md`
MUST_TEXT: Enforce Stage 3 minimum claim thresholds against raw-log baseline.
STATUS: NOT_STARTED
OWNER_TASK_ID: baseline-comparison-claims-v0
EVIDENCE: `configs/eval_v0q.yaml`

SPEC_MUST_ID: S08-M09
SOURCE_SPEC: `docs/specs/08_evaluation_and_metrics.md`
MUST_TEXT: Require Stage 4 interpretable benefit on one governance metric and one continuity metric in the same task family.
STATUS: NOT_STARTED
OWNER_TASK_ID: long-horizon-study-v0
EVIDENCE: `configs/eval_v0q.yaml`

## Spec 09 (`docs/specs/09_risks_non_goals_deferred.md`)
SPEC_MUST_ID: S09-M01
SOURCE_SPEC: `docs/specs/09_risks_non_goals_deferred.md`
MUST_TEXT: Preserve explicit v0 non-goals as exclusion criteria.
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `docs/specs/09_risks_non_goals_deferred.md`; `docs/specs/00_scope_and_claim.md`; `MASTER_DOC.md` sections 4.2, 22

SPEC_MUST_ID: S09-M02
SOURCE_SPEC: `docs/specs/09_risks_non_goals_deferred.md`
MUST_TEXT: Track known failure modes as active design risks.
STATUS: IN_PROGRESS
OWNER_TASK_ID: dod-evidence-closeout-v0
EVIDENCE: `docs/specs/09_risks_non_goals_deferred.md`; `docs/handoff/CURRENT_STATUS.md`

SPEC_MUST_ID: S09-M03
SOURCE_SPEC: `docs/specs/09_risks_non_goals_deferred.md`
MUST_TEXT: Document deferred features without pulling them into v0 acceptance.
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `docs/specs/09_risks_non_goals_deferred.md`; `MASTER_DOC.md` section 22; `docs/specs/10_checklists_and_dod.md`

## Spec 10 (`docs/specs/10_checklists_and_dod.md`)
SPEC_MUST_ID: S10-M01
SOURCE_SPEC: `docs/specs/10_checklists_and_dod.md`
MUST_TEXT: Maintain project checklists for framing, policy, data model, architecture, evaluation, and research hygiene.
STATUS: SATISFIED
OWNER_TASK_ID: docs-operations-hardening-v0
EVIDENCE: `docs/handoff/OVERVIEW_CHECKLIST.md`

SPEC_MUST_ID: S10-M02
SOURCE_SPEC: `docs/specs/10_checklists_and_dod.md`
MUST_TEXT: Meet v0 Definition of Done criteria before claiming successful prototype completion.
STATUS: IN_PROGRESS
OWNER_TASK_ID: dod-evidence-closeout-v0
EVIDENCE: `docs/specs/10_checklists_and_dod.md`; `docs/handoff/OVERVIEW_CHECKLIST.md`

SPEC_MUST_ID: S10-M03
SOURCE_SPEC: `docs/specs/10_checklists_and_dod.md`
MUST_TEXT: Verify policy enforcement is deterministic and code-level rather than prompt-level.
STATUS: SATISFIED
OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
EVIDENCE: `src/core/scoring.py`; `src/core/state_machine.py`; `src/core/test_trigger.py`; `tests/test_policy_scoring.py`; `tests/test_state_machine.py`; `tests/test_test_trigger.py`

SPEC_MUST_ID: S10-M04
SOURCE_SPEC: `docs/specs/10_checklists_and_dod.md`
MUST_TEXT: Require policy correctness micro-suite pass rate of 100%.
STATUS: SATISFIED
OWNER_TASK_ID: policy-correctness-micro-suite-v0
EVIDENCE: `tests/test_policy_scoring.py`; `tests/test_state_machine.py`; `tests/test_test_trigger.py`; `configs/eval_v0q.yaml`

SPEC_MUST_ID: S10-M05
SOURCE_SPEC: `docs/specs/10_checklists_and_dod.md`
MUST_TEXT: Require reproducible stress benchmark artifacts using the frozen artifact schema.
STATUS: IN_PROGRESS
OWNER_TASK_ID: governance-stress-suite-v0
EVIDENCE: `docs/specs/08_evaluation_and_metrics.md`; `configs/eval_v0q.yaml`; `src/eval/schemas.py`; `src/eval/artifacts.py`

SPEC_MUST_ID: S10-M06
SOURCE_SPEC: `docs/specs/10_checklists_and_dod.md`
MUST_TEXT: Require baseline-comparison claim thresholds (>=10% relative on >=3 policy metrics and <=3pp task-success drop).
STATUS: IN_PROGRESS
OWNER_TASK_ID: baseline-comparison-claims-v0
EVIDENCE: `docs/specs/08_evaluation_and_metrics.md`; `configs/eval_v0q.yaml`; `docs/handoff/OVERVIEW_CHECKLIST.md`

SPEC_MUST_ID: S10-M07
SOURCE_SPEC: `docs/specs/10_checklists_and_dod.md`
MUST_TEXT: Require long-horizon interpretable benefit on at least one governance metric plus one continuity metric.
STATUS: IN_PROGRESS
OWNER_TASK_ID: long-horizon-study-v0
EVIDENCE: `docs/specs/08_evaluation_and_metrics.md`; `docs/handoff/OVERVIEW_CHECKLIST.md`

## Update Rules
- Keep each `SPEC_MUST_ID` unique and stable.
- `NEXT_TASK.md:SPEC_MUST_IDS` entries must reference IDs in this file.
- Mark `SATISFIED` only when evidence links point to implemented/tested behavior.

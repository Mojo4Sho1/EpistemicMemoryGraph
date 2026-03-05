# v0 Overview Checklist

LAST_UPDATED: 2026-03-05
PROJECT_PHASE: implementation

## Status Legend
- `NOT_STARTED`: no implementation evidence yet
- `IN_PROGRESS`: partial implementation/evidence exists
- `BLOCKED`: cannot proceed due to explicit blocker
- `DONE`: exit criteria met with evidence links

## A. Build Milestones (MASTER_DOC 15.3)

### M1: Freeze schema and policy constants
- STATUS: DONE
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: constants/state-machine/data-model freeze reflected in code + docs with tests
- EVIDENCE: `MASTER_DOC.md`, `docs/specs/03_policy_and_state_machine.md`, `docs/specs/04_scoring_and_trust.md`, `src/core/policy_config.py`, `tests/test_policy_scoring.py`, `tests/test_state_machine.py`
- SOURCE: MASTER_DOC 15.3(1), 9, 10, 20

### M2: Implement observation log and persistence tables
- STATUS: DONE
- OWNER_TASK_ID: observation-sqlite-store-v0
- EXIT_CRITERIA: append-only observation persistence with deterministic duplicate handling and lookup
- EVIDENCE: `src/store/observation_store.py`, `tests/test_observation_store.py`
- SOURCE: MASTER_DOC 7.1, 15.3(2), 20

### M3: Implement in-memory workspace object
- STATUS: DONE
- OWNER_TASK_ID: workspace-update-boundary-v0q-v0
- EXIT_CRITERIA: workspace intake path records observations and returns deterministic result
- EVIDENCE: `src/workspace/intake.py`, `src/workspace/state.py`, `src/workspace/update.py`, `src/workspace/consolidation.py`, `tests/test_workspace_intake.py`, `tests/test_workspace_state.py`, `tests/test_workspace_update.py`, `tests/test_workspace_consolidation.py`
- SOURCE: MASTER_DOC 7.2, 13.1, 15.3(3)

### M4: Implement scoring and state transitions
- STATUS: DONE
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: deterministic scoring + transition logic with tests
- EVIDENCE: `src/core/scoring.py`, `src/core/state_machine.py`, `tests/test_policy_scoring.py`, `tests/test_state_machine.py`
- SOURCE: MASTER_DOC 9, 12, 15.3(4)

### M5: Implement conservative identity handling
- STATUS: DONE
- OWNER_TASK_ID: identity-alias-possible-same-as-v0
- EXIT_CRITERIA: alias + possible_same_as behavior with tests
- EVIDENCE: `src/core/constants.py`; `src/core/models.py`; `src/workspace/update.py`; `tests/test_core_models.py`; `tests/test_workspace_update.py`
- SOURCE: MASTER_DOC 8.1, 8.6, 15.3(5)

### M6: Implement tool boundary and validation layer
- STATUS: DONE
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: proposal-only tool surface with deterministic validation boundary
- EVIDENCE: `src/tools/schemas.py`, `tests/test_tool_schemas.py`, `docs/specs/06_tool_boundary_and_interfaces.md`
- SOURCE: MASTER_DOC 14, 15.3(6)

### M7: Implement consolidation and archival
- STATUS: DONE
- OWNER_TASK_ID: consolidation-archival-determinism-v0
- EXIT_CRITERIA: promote/archive/discard flow at task boundary with trace logging
- EVIDENCE: `src/workspace/consolidation.py`, `src/eval/schemas.py`, `tests/test_workspace_consolidation.py`, `tests/test_eval_artifacts.py`, `tests/smoke/test_workspace_update_smoke.py`, `scripts/probes/workspace_update_probe.py`
- SOURCE: MASTER_DOC 13.4, 15.3(7)

### M8: Build policy correctness suite
- STATUS: DONE
- OWNER_TASK_ID: policy-correctness-micro-suite-v0
- EXIT_CRITERIA: micro-scenario suite for state/policy correctness
- EVIDENCE: `tests/test_policy_scoring.py`, `tests/test_state_machine.py`, `tests/test_test_trigger.py`
- SOURCE: MASTER_DOC 16.1, 15.3(8), 20

### M9: Build baseline variants
- STATUS: DONE
- OWNER_TASK_ID: baseline-variants-core-v0
- EXIT_CRITERIA: baseline memory systems runnable for comparison
- EVIDENCE: `configs/baselines_v0q.yaml`; `src/eval/baselines.py`; `src/eval/fairness.py`; `tests/test_eval_fairness.py`
- SOURCE: MASTER_DOC 16.3, 18, 15.3(9)

### M10: Run first governance benchmark + end-to-end trials
- STATUS: DONE
- OWNER_TASK_ID: long-horizon-study-v0
- EXIT_CRITERIA: reproducible benchmark + long-horizon study artifacts
- EVIDENCE: `src/eval/stress.py`; `src/eval/baselines.py`; `src/eval/long_horizon.py`; `tests/test_eval_artifacts.py`; `tests/test_eval_fairness.py`; `tests/smoke/test_eval_artifact_smoke.py`; `scripts/probes/long_horizon_study_probe.py`; `artifacts/2026-03-05_abcdef12_full_governed_system_policy-debug_101/metrics_summary.json`; `artifacts/2026-03-05_abcdef12_raw_text_log_retrieval_policy-debug_101/metrics_summary.json`; `configs/eval_v0q.yaml`
- SOURCE: MASTER_DOC 16.2, 16.4, 15.3(10), 21

## B. Master Implementation Checklist (MASTER_DOC 20)

### Project framing
- CHECK_ID: C20-FRAME-01
- STATUS: DONE
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: v0 problem statement is frozen and referenced by implementation docs.
- EVIDENCE: `MASTER_DOC.md` sections 3, 20; `docs/specs/00_scope_and_claim.md`
- SOURCE: MASTER_DOC 20 (Freeze the v0 problem statement)

- CHECK_ID: C20-FRAME-02
- STATUS: DONE
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: first-study research claim is frozen and traceable.
- EVIDENCE: `MASTER_DOC.md` sections 3, 20; `docs/specs/00_scope_and_claim.md`
- SOURCE: MASTER_DOC 20 (Freeze the first study research claim)

- CHECK_ID: C20-FRAME-03
- STATUS: DONE
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: non-goals are frozen and enforced as exclusion criteria.
- EVIDENCE: `MASTER_DOC.md` sections 4.2, 20, 22; `docs/specs/09_risks_non_goals_deferred.md`
- SOURCE: MASTER_DOC 20 (Freeze non goals)

### Policy
- CHECK_ID: C20-POLICY-01
- STATUS: DONE
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: belief-state machine is deterministic and frozen in docs + code.
- EVIDENCE: `docs/specs/03_policy_and_state_machine.md`; `src/core/state_machine.py`; `tests/test_state_machine.py`
- SOURCE: MASTER_DOC 20 (Freeze the belief state machine)

- CHECK_ID: C20-POLICY-02
- STATUS: DONE
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: ten governance rules are represented in normative specs and enforced by boundary logic.
- EVIDENCE: `docs/specs/03_policy_and_state_machine.md`; `docs/specs/06_tool_boundary_and_interfaces.md`; `src/tools/schemas.py`
- SOURCE: MASTER_DOC 20 (Freeze the ten core rules)

- CHECK_ID: C20-POLICY-03
- STATUS: DONE
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: trust-model fields are frozen and represented in policy/data documentation.
- EVIDENCE: `docs/specs/04_scoring_and_trust.md`; `docs/specs/02_data_model.md`
- SOURCE: MASTER_DOC 20 (Freeze trust model fields)

- CHECK_ID: C20-POLICY-04
- STATUS: DONE
- OWNER_TASK_ID: consolidation-archival-determinism-v0
- EXIT_CRITERIA: promotion and decay criteria are fully covered by deterministic boundary tests.
- EVIDENCE: `configs/policy_v0q.yaml`; `src/workspace/consolidation.py`; `tests/test_workspace_consolidation.py`; `tests/test_state_machine.py`
- SOURCE: MASTER_DOC 20 (Freeze promotion and decay criteria)

- CHECK_ID: C20-POLICY-05
- STATUS: DONE
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: no-hard-auto-merge constraint is explicit in policy/data model documentation.
- EVIDENCE: `MASTER_DOC.md` sections 8.6, 20; `docs/specs/02_data_model.md`; `docs/specs/09_risks_non_goals_deferred.md`
- SOURCE: MASTER_DOC 20 (Freeze the no hard auto merge rule)

### Data model
- CHECK_ID: C20-DATA-01
- STATUS: DONE
- OWNER_TASK_ID: core-model-primitives-v0
- EXIT_CRITERIA: core object types are frozen in docs and model primitives.
- EVIDENCE: `docs/specs/02_data_model.md`; `src/core/models.py`; `tests/test_core_models.py`
- SOURCE: MASTER_DOC 20 (Freeze object types)

- CHECK_ID: C20-DATA-02
- STATUS: DONE
- OWNER_TASK_ID: core-model-primitives-v0
- EXIT_CRITERIA: relationship types are frozen and tested.
- EVIDENCE: `docs/specs/02_data_model.md`; `src/core/constants.py`; `tests/test_scaffold_imports.py`
- SOURCE: MASTER_DOC 20 (Freeze relationship types)

- CHECK_ID: C20-DATA-03
- STATUS: DONE
- OWNER_TASK_ID: identity-alias-possible-same-as-v0
- EXIT_CRITERIA: persistent table schema for canonical memory objects is frozen.
- EVIDENCE: `docs/specs/02_data_model.md`; `src/core/constants.py`; `src/core/models.py`; `src/workspace/update.py`; `src/store/observation_store.py`; `tests/test_core_models.py`; `tests/test_workspace_update.py`
- SOURCE: MASTER_DOC 20 (Freeze persistent table schema)

- CHECK_ID: C20-DATA-04
- STATUS: DONE
- OWNER_TASK_ID: identity-alias-possible-same-as-v0
- EXIT_CRITERIA: workspace schema is frozen and fully covered by deterministic tests.
- EVIDENCE: `docs/specs/02_data_model.md`; `src/workspace/state.py`; `src/workspace/update.py`; `tests/test_workspace_state.py`; `tests/test_workspace_update.py`
- SOURCE: MASTER_DOC 20 (Freeze workspace schema)

- CHECK_ID: C20-DATA-05
- STATUS: DONE
- OWNER_TASK_ID: consolidation-archival-determinism-v0
- EXIT_CRITERIA: episode archive format is frozen and emitted through consolidation/eval artifacts.
- EVIDENCE: `docs/specs/02_data_model.md`; `src/eval/schemas.py`; `src/workspace/consolidation.py`; `tests/test_workspace_consolidation.py`; `tests/test_eval_artifacts.py`
- SOURCE: MASTER_DOC 20 (Freeze episode archive format)

### Runtime architecture
- CHECK_ID: C20-RUNTIME-01
- STATUS: DONE
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: tool surface is frozen with deterministic schema validation.
- EVIDENCE: `docs/specs/06_tool_boundary_and_interfaces.md`; `src/tools/schemas.py`; `tests/test_tool_schemas.py`
- SOURCE: MASTER_DOC 20 (Freeze the tool surface)

- CHECK_ID: C20-RUNTIME-02
- STATUS: DONE
- OWNER_TASK_ID: workspace-update-boundary-v0q-v0
- EXIT_CRITERIA: deterministic policy boundary is implemented for intake/update gating.
- EVIDENCE: `src/workspace/update.py`; `src/workspace/intake.py`; `tests/test_workspace_update.py`; `tests/smoke/test_workspace_update_smoke.py`
- SOURCE: MASTER_DOC 20 (Freeze the deterministic policy boundary)

- CHECK_ID: C20-RUNTIME-03
- STATUS: DONE
- OWNER_TASK_ID: consolidation-archival-determinism-v0
- EXIT_CRITERIA: consolidation workflow boundary behavior is deterministic and fully evidenced.
- EVIDENCE: `docs/specs/05_operational_flows.md`; `src/workspace/consolidation.py`; `tests/test_workspace_consolidation.py`
- SOURCE: MASTER_DOC 20 (Freeze consolidation workflow)

- CHECK_ID: C20-RUNTIME-04
- STATUS: DONE
- OWNER_TASK_ID: retrieval-reactivation-boundary-v0
- EXIT_CRITERIA: retrieval/reactivation workflow is frozen with deterministic interfaces and tests.
- EVIDENCE: `src/store/canonical_memory.py`; `src/workspace/reactivation.py`; `src/workspace/update.py`; `tests/test_workspace_state.py`; `tests/test_workspace_update.py`; `tests/smoke/test_workspace_update_smoke.py`
- SOURCE: MASTER_DOC 20 (Freeze retrieval and reactivation workflow)

### Evaluation
- CHECK_ID: C20-EVAL-01
- STATUS: DONE
- OWNER_TASK_ID: policy-correctness-micro-suite-v0
- EXIT_CRITERIA: deterministic policy correctness tests exist and pass.
- EVIDENCE: `tests/test_policy_scoring.py`; `tests/test_state_machine.py`; `tests/test_test_trigger.py`
- SOURCE: MASTER_DOC 20 (Write policy correctness tests)

- CHECK_ID: C20-EVAL-02
- STATUS: DONE
- OWNER_TASK_ID: governance-stress-suite-v0
- EXIT_CRITERIA: governance stress scenario catalog is defined and executable.
- EVIDENCE: `src/eval/stress.py`; `src/eval/__init__.py`; `tests/test_eval_artifacts.py`; `tests/smoke/test_eval_artifact_smoke.py`
- SOURCE: MASTER_DOC 20 (Design governance stress scenarios)

- CHECK_ID: C20-EVAL-03
- STATUS: DONE
- OWNER_TASK_ID: baseline-variants-core-v0
- EXIT_CRITERIA: baseline systems are defined and runnable under shared fairness constraints.
- EVIDENCE: `configs/baselines_v0q.yaml`; `src/eval/baselines.py`; `src/eval/fairness.py`; `tests/test_eval_fairness.py`
- SOURCE: MASTER_DOC 20 (Define baseline systems)

- CHECK_ID: C20-EVAL-04
- STATUS: DONE
- OWNER_TASK_ID: governance-stress-suite-v0
- EXIT_CRITERIA: metrics/logging schema is frozen and used by benchmark artifacts.
- EVIDENCE: `docs/specs/08_evaluation_and_metrics.md`; `configs/eval_v0q.yaml`; `src/eval/schemas.py`; `src/eval/artifacts.py`; `src/eval/stress.py`; `tests/test_eval_artifacts.py`; `tests/smoke/test_eval_artifact_smoke.py`
- SOURCE: MASTER_DOC 20 (Define metrics and logging schema)

- CHECK_ID: C20-EVAL-05
- STATUS: DONE
- OWNER_TASK_ID: baseline-comparison-claims-v0
- EXIT_CRITERIA: ablation plan is defined and tied to runnable benchmark workflow.
- EVIDENCE: `MASTER_DOC.md` section 18; `docs/specs/08_evaluation_and_metrics.md`; `configs/baselines_v0q.yaml`; `src/eval/baselines.py`; `tests/test_eval_fairness.py`
- SOURCE: MASTER_DOC 20 (Define the ablation plan)

### Research hygiene
- CHECK_ID: C20-HYGIENE-01
- STATUS: DONE
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: experiment config spec exists and is frozen for v0.1q.
- EVIDENCE: `configs/policy_v0q.yaml`; `configs/eval_v0q.yaml`; `configs/baselines_v0q.yaml`; `configs/CONFIG_INDEX.md`
- SOURCE: MASTER_DOC 20 (Create experiment config spec)

- CHECK_ID: C20-HYGIENE-02
- STATUS: DONE
- OWNER_TASK_ID: governance-stress-suite-v0
- EXIT_CRITERIA: run logging spec is fully represented and exercised by benchmark runs.
- EVIDENCE: `docs/specs/08_evaluation_and_metrics.md`; `src/eval/schemas.py`; `src/eval/artifacts.py`; `src/eval/stress.py`; `tests/test_eval_artifacts.py`; `tests/smoke/test_eval_artifact_smoke.py`
- SOURCE: MASTER_DOC 20 (Create run logging spec)

- CHECK_ID: C20-HYGIENE-03
- STATUS: DONE
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: fixed seed and reproducibility policy is documented and coded.
- EVIDENCE: `configs/eval_v0q.yaml`; `src/eval/artifacts.py`; `tests/test_eval_artifacts.py`
- SOURCE: MASTER_DOC 20 (Create seed and reproducibility policy)

- CHECK_ID: C20-HYGIENE-04
- STATUS: DONE
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: artifact naming convention is deterministic and implemented.
- EVIDENCE: `configs/eval_v0q.yaml`; `src/eval/artifacts.py`; `tests/test_eval_artifacts.py`
- SOURCE: MASTER_DOC 20 (Create result artifact naming convention)

- CHECK_ID: C20-HYGIENE-05
- STATUS: IN_PROGRESS
- OWNER_TASK_ID: dod-evidence-closeout-v0
- EXIT_CRITERIA: failure-analysis template exists and is linked from evaluation workflow docs.
- EVIDENCE: `docs/specs/10_checklists_and_dod.md`; `docs/handoff/NEXT_TASK.md`
- SOURCE: MASTER_DOC 20 (Create failure analysis template)

## C. Definition of Done Readiness (MASTER_DOC 21)
- CHECK_ID: C21-01
- STATUS: DONE
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: policy is enforced by deterministic code paths.
- EVIDENCE: `src/core/scoring.py`; `src/core/state_machine.py`; `src/core/test_trigger.py`; `src/tools/schemas.py`
- SOURCE: MASTER_DOC 21 (deterministic policy enforcement)

- CHECK_ID: C21-02
- STATUS: DONE
- OWNER_TASK_ID: retrieval-reactivation-boundary-v0
- EXIT_CRITERIA: observation log, workspace, and canonical memory layers function end-to-end.
- EVIDENCE: `src/store/observation_store.py`; `src/store/canonical_memory.py`; `src/workspace/state.py`; `src/workspace/reactivation.py`; `src/workspace/update.py`; `tests/test_workspace_state.py`; `tests/test_workspace_update.py`; `tests/smoke/test_workspace_update_smoke.py`
- SOURCE: MASTER_DOC 21 (three layers end-to-end)

- CHECK_ID: C21-03
- STATUS: DONE
- OWNER_TASK_ID: policy-correctness-micro-suite-v0
- EXIT_CRITERIA: full policy micro-scenario suite passes deterministically.
- EVIDENCE: `tests/test_policy_scoring.py`; `tests/test_state_machine.py`; `tests/test_test_trigger.py`
- SOURCE: MASTER_DOC 21 (policy correctness suite)

- CHECK_ID: C21-04
- STATUS: DONE
- OWNER_TASK_ID: governance-stress-suite-v0
- EXIT_CRITERIA: governance stress benchmark executes reproducibly with required artifacts.
- EVIDENCE: `src/eval/stress.py`; `configs/eval_v0q.yaml`; `tests/test_eval_artifacts.py`; `tests/smoke/test_eval_artifact_smoke.py`
- SOURCE: MASTER_DOC 21 (stress benchmark reproducibility)

- CHECK_ID: C21-05
- STATUS: DONE
- OWNER_TASK_ID: baseline-comparison-claims-v0
- EXIT_CRITERIA: governed system improves >=10% relative on >=3 policy metrics vs raw-log baseline.
- EVIDENCE: `configs/eval_v0q.yaml`; `src/eval/baselines.py`; `tests/test_eval_fairness.py`
- SOURCE: MASTER_DOC 21 (baseline improvement threshold)

- CHECK_ID: C21-06
- STATUS: DONE
- OWNER_TASK_ID: baseline-comparison-claims-v0
- EXIT_CRITERIA: task success drop vs raw-log baseline is <=3 absolute percentage points.
- EVIDENCE: `configs/eval_v0q.yaml`; `src/eval/baselines.py`; `tests/test_eval_fairness.py`
- SOURCE: MASTER_DOC 21 (task success non-degradation threshold)

- CHECK_ID: C21-07
- STATUS: DONE
- OWNER_TASK_ID: long-horizon-study-v0
- EXIT_CRITERIA: one task family shows both governance and continuity metric improvement.
- EVIDENCE: `docs/specs/08_evaluation_and_metrics.md`; `configs/eval_v0q.yaml`; `src/eval/long_horizon.py`; `tests/test_eval_artifacts.py`; `scripts/probes/long_horizon_study_probe.py`; `artifacts/2026-03-05_abcdef12_full_governed_system_policy-debug_101/metrics_summary.json`; `artifacts/2026-03-05_abcdef12_raw_text_log_retrieval_policy-debug_101/metrics_summary.json`
- SOURCE: MASTER_DOC 21 (interpretable long-horizon benefit)

- CHECK_ID: C21-08
- STATUS: DONE
- OWNER_TASK_ID: governance-stress-suite-v0
- EXIT_CRITERIA: logging/artifact trail is complete for failure analysis reporting.
- EVIDENCE: `docs/specs/08_evaluation_and_metrics.md`; `configs/eval_v0q.yaml`; `src/eval/schemas.py`; `src/eval/artifacts.py`; `src/eval/stress.py`; `tests/test_eval_artifacts.py`; `tests/smoke/test_eval_artifact_smoke.py`
- SOURCE: MASTER_DOC 21 (artifact sufficiency for failure analysis)

## D. Immediate Next Actions Tracking (MASTER_DOC 23)
1. Treat master as design freeze: DONE
2. Split into derived docs: IN_PROGRESS
3. Implement schema + policy boundary before higher-level behavior: IN_PROGRESS
4. Create policy correctness micro-scenarios before full benchmark harness (OWNER_TASK_ID: policy-correctness-micro-suite-v0): DONE
5. Introduce minimal smoke suite + workspace probe scripts after composed boundary implementation (OWNER_TASK_ID: workspace-smoke-suite-v0q-v0): DONE
6. Harden SQLite observation-store persistence contract coverage (OWNER_TASK_ID: observation-sqlite-store-v0): DONE
7. Expand consolidation cadence/carryover/promotion boundary micro-scenarios (OWNER_TASK_ID: consolidation-archival-determinism-v0): DONE
8. Establish M5-M10 task queue + decision/spec-conformance trackers (OWNER_TASK_ID: docs-operations-hardening-v0): DONE
9. Implement conservative identity handling + retrieval/reactivation boundaries (OWNER_TASK_ID: retrieval-reactivation-boundary-v0): DONE

## Update Rules
- Update this file once per completed handoff loop.
- Only flip to `DONE` when exit criteria and evidence are both present.
- Every Section B/C row must include exactly one `CHECK_ID` and one `SOURCE`.
- `OWNER_TASK_ID` must reference active or staged task IDs from handoff queue docs.
- Keep content concise and operational; avoid narrative logs.

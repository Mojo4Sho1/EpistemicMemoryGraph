# v0 Overview Checklist

LAST_UPDATED: 2026-02-28
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
- STATUS: IN_PROGRESS
- OWNER_TASK_ID: observation-sqlite-store-v0
- EXIT_CRITERIA: append-only observation persistence with deterministic duplicate handling and lookup
- EVIDENCE: `src/store/observation_store.py`, `tests/test_observation_store.py`
- SOURCE: MASTER_DOC 7.1, 15.3(2), 20

### M3: Implement in-memory workspace object
- STATUS: IN_PROGRESS
- OWNER_TASK_ID: workspace-update-boundary-v0q-v0
- EXIT_CRITERIA: workspace intake path records observations and returns deterministic result
- EVIDENCE: `src/workspace/intake.py`, `src/workspace/state.py`, `src/workspace/consolidation.py`, `tests/test_workspace_intake.py`, `tests/test_workspace_state.py`, `tests/test_workspace_consolidation.py`, `docs/handoff/NEXT_TASK.md` (active task)
- SOURCE: MASTER_DOC 7.2, 13.1, 15.3(3)

### M4: Implement scoring and state transitions
- STATUS: DONE
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: deterministic scoring + transition logic with tests
- EVIDENCE: `src/core/scoring.py`, `src/core/state_machine.py`, `tests/test_policy_scoring.py`, `tests/test_state_machine.py`
- SOURCE: MASTER_DOC 9, 12, 15.3(4)

### M5: Implement conservative identity handling
- STATUS: NOT_STARTED
- OWNER_TASK_ID: UNASSIGNED
- EXIT_CRITERIA: alias + possible_same_as behavior with tests
- EVIDENCE: NONE
- SOURCE: MASTER_DOC 8.1, 8.6, 15.3(5)

### M6: Implement tool boundary and validation layer
- STATUS: DONE
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: proposal-only tool surface with deterministic validation boundary
- EVIDENCE: `src/tools/schemas.py`, `tests/test_tool_schemas.py`, `docs/specs/06_tool_boundary_and_interfaces.md`
- SOURCE: MASTER_DOC 14, 15.3(6)

### M7: Implement consolidation and archival
- STATUS: IN_PROGRESS
- OWNER_TASK_ID: workspace-update-boundary-v0q-v0
- EXIT_CRITERIA: promote/archive/discard flow at task boundary with trace logging
- EVIDENCE: `src/workspace/consolidation.py`, `src/eval/schemas.py`, `tests/test_workspace_consolidation.py`, `tests/test_eval_artifacts.py`
- SOURCE: MASTER_DOC 13.4, 15.3(7)

### M8: Build policy correctness suite
- STATUS: IN_PROGRESS
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: micro-scenario suite for state/policy correctness
- EVIDENCE: `tests/test_policy_scoring.py`, `tests/test_state_machine.py`, `tests/test_test_trigger.py`
- SOURCE: MASTER_DOC 16.1, 15.3(8), 20

### M9: Build baseline variants
- STATUS: NOT_STARTED
- OWNER_TASK_ID: UNASSIGNED
- EXIT_CRITERIA: baseline memory systems runnable for comparison
- EVIDENCE: NONE
- SOURCE: MASTER_DOC 16.3, 18, 15.3(9)

### M10: Run first governance benchmark + end-to-end trials
- STATUS: NOT_STARTED
- OWNER_TASK_ID: UNASSIGNED
- EXIT_CRITERIA: reproducible benchmark + long-horizon study artifacts
- EVIDENCE: NONE
- SOURCE: MASTER_DOC 16.2, 16.4, 15.3(10), 21

## B. Master Implementation Checklist (MASTER_DOC 20)

### Project framing
- STATUS: IN_PROGRESS
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: problem statement, research claim, and non-goals frozen in active docs
- EVIDENCE: `MASTER_DOC.md` sections 3, 4, 20
- SOURCE: MASTER_DOC 20

### Policy
- STATUS: DONE
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: belief states/rules/trust/promotion criteria represented in specs + code anchors
- EVIDENCE: `docs/specs/03_policy_and_state_machine.md`, `docs/specs/04_scoring_and_trust.md`, `src/core/policy_config.py`, `src/core/state_machine.py`
- SOURCE: MASTER_DOC 9, 10, 11, 20

### Data model
- STATUS: IN_PROGRESS
- OWNER_TASK_ID: core-model-primitives-v0
- EXIT_CRITERIA: object/relationship/schema/workspace/archive structures frozen and testable
- EVIDENCE: `docs/specs/02_data_model.md`, `src/core/models.py`
- SOURCE: MASTER_DOC 8, 20

### Runtime architecture
- STATUS: IN_PROGRESS
- OWNER_TASK_ID: workspace-update-boundary-v0q-v0
- EXIT_CRITERIA: tool surface, policy boundary, consolidation, retrieval/reactivation defined and partially implemented
- EVIDENCE: `docs/specs/01_architecture_overview.md`, `docs/specs/05_operational_flows.md`, `docs/specs/06_tool_boundary_and_interfaces.md`, `src/workspace/consolidation.py`, `src/tools/schemas.py`
- SOURCE: MASTER_DOC 6, 13, 14, 20

### Evaluation
- STATUS: IN_PROGRESS
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: correctness tests, stress scenarios, baselines, metrics/logging schema defined
- EVIDENCE: `docs/specs/08_evaluation_and_metrics.md`, `configs/eval_v0q.yaml`, `configs/baselines_v0q.yaml`, `src/eval/schemas.py`, `src/eval/fairness.py`, `tests/test_eval_fairness.py`
- SOURCE: MASTER_DOC 16, 17, 18, 20

### Research hygiene
- STATUS: IN_PROGRESS
- OWNER_TASK_ID: v0q-minimum-quantified-hardening-v0
- EXIT_CRITERIA: experiment config/logging/seed/artifact/failure-analysis policy artifacts present
- EVIDENCE: `configs/policy_v0q.yaml`, `configs/eval_v0q.yaml`, `configs/baselines_v0q.yaml`, `src/eval/artifacts.py`, `tests/test_eval_artifacts.py`
- SOURCE: MASTER_DOC 20

## C. Definition of Done Readiness (MASTER_DOC 21)
- Policy enforced by deterministic code: DONE
- Three layers function end-to-end: NOT_STARTED
- Policy correctness micro-suite passes: IN_PROGRESS
- Governance stress benchmark reproducible: NOT_STARTED
- Outperforms naive baseline on governance metrics: NOT_STARTED
- Interpretable long-horizon benefit: NOT_STARTED
- Logging/artifact trail sufficient: IN_PROGRESS

## D. Immediate Next Actions Tracking (MASTER_DOC 23)
1. Treat master as design freeze: DONE
2. Split into derived docs: IN_PROGRESS
3. Implement schema + policy boundary before higher-level behavior: IN_PROGRESS
4. Create policy correctness micro-scenarios before full benchmark harness: IN_PROGRESS

## Update Rules
- Update this file once per completed handoff loop.
- Only flip to `DONE` when exit criteria and evidence are both present.
- `OWNER_TASK_ID` must reference active or last-completing task IDs from handoff docs.
- Keep content concise and operational; avoid narrative logs.

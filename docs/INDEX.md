# Documentation Index (Agent-First)

Use this file as the first entrypoint for scoped work. Search by keyword and open only the referenced primary spec.

## How To Use

- Run `rg "KEYWORDS:" docs/INDEX.md` to list all topic blocks.
- Run `rg "<your term>" docs/INDEX.md` to route quickly.
- Open `PRIMARY_DOC` first, then `RELATED_DOCS` only as needed.

## Topic Map

KEYWORDS: project scope, research claim, non-goals, design principles, governance objective
CANONICAL_TOPIC: scope_and_claim
PRIMARY_DOC: docs/specs/00_scope_and_claim.md
RELATED_DOCS: docs/specs/09_risks_non_goals_deferred.md, docs/specs/10_checklists_and_dod.md
SOURCE_SECTIONS: 1, 2, 3, 4, 5, 22, 24
WHEN_TO_READ: use when deciding if a feature/task belongs in v0.

KEYWORDS: architecture layers, observation log, workspace, canonical memory, layer boundaries
CANONICAL_TOPIC: architecture_overview
PRIMARY_DOC: docs/specs/01_architecture_overview.md
RELATED_DOCS: docs/specs/05_operational_flows.md, docs/specs/06_tool_boundary_and_interfaces.md
SOURCE_SECTIONS: 6, 7, 13.4, 13.5, 15.1
WHEN_TO_READ: use when implementing system structure or memory layer responsibilities.

KEYWORDS: data model, entities, propositions, observations, episodes, edges, possible_same_as
CANONICAL_TOPIC: core_data_model
PRIMARY_DOC: docs/specs/02_data_model.md
RELATED_DOCS: docs/specs/03_policy_and_state_machine.md, docs/specs/04_scoring_and_trust.md
SOURCE_SECTIONS: 7.1, 7.3, 8, 15.1
WHEN_TO_READ: use when defining tables, object fields, and relationship semantics.

KEYWORDS: policy rules, belief state machine, tentative, contested state, accepted, rejected
CANONICAL_TOPIC: policy_and_state_machine
PRIMARY_DOC: docs/specs/03_policy_and_state_machine.md
RELATED_DOCS: docs/specs/04_scoring_and_trust.md, docs/specs/05_operational_flows.md
SOURCE_SECTIONS: 9, 10, 12, 13.3, 16.1
WHEN_TO_READ: use when implementing governance logic, transitions, or contradiction handling.

KEYWORDS: scoring model, trust model, source reliability, source independence, decay, volatility
CANONICAL_TOPIC: scoring_and_trust
PRIMARY_DOC: docs/specs/04_scoring_and_trust.md
RELATED_DOCS: docs/specs/03_policy_and_state_machine.md, docs/specs/08_evaluation_and_metrics.md
SOURCE_SECTIONS: 11, 12, 10.5, 10.7
WHEN_TO_READ: use when implementing confidence updates, trust weighting, and staleness handling.

KEYWORDS: intake flow, workspace update flow, hypothesis testing loop, consolidation, reactivation
CANONICAL_TOPIC: operational_flows
PRIMARY_DOC: docs/specs/05_operational_flows.md
RELATED_DOCS: docs/specs/03_policy_and_state_machine.md, docs/specs/01_architecture_overview.md
SOURCE_SECTIONS: 13.1, 13.2, 13.3, 13.4, 13.5, 6
WHEN_TO_READ: use when implementing runtime orchestration and task-boundary consolidation.

KEYWORDS: tool boundary, llm proposals, deterministic validator, interface surface, mutation authority
CANONICAL_TOPIC: tool_boundary_and_interfaces
PRIMARY_DOC: docs/specs/06_tool_boundary_and_interfaces.md
RELATED_DOCS: docs/specs/03_policy_and_state_machine.md, docs/specs/05_operational_flows.md
SOURCE_SECTIONS: 14, 10.4, 10.10, 15.2
WHEN_TO_READ: use when implementing tool adapters, validation, and durable write controls.

KEYWORDS: build plan, milestones, implementation sequence, sqlite, workspace in-memory
CANONICAL_TOPIC: build_plan_and_milestones
PRIMARY_DOC: docs/specs/07_build_plan_and_milestones.md
RELATED_DOCS: docs/specs/10_checklists_and_dod.md, docs/specs/08_evaluation_and_metrics.md
SOURCE_SECTIONS: 15.1, 15.2, 15.3, 23
WHEN_TO_READ: use when planning execution order and dependency-aware delivery.

KEYWORDS: evaluation, baseline comparison, ablation, false promotion rate, metrics, logging
CANONICAL_TOPIC: evaluation_and_metrics
PRIMARY_DOC: docs/specs/08_evaluation_and_metrics.md
RELATED_DOCS: docs/specs/10_checklists_and_dod.md, docs/specs/07_build_plan_and_milestones.md
SOURCE_SECTIONS: 16, 17, 18, 21
WHEN_TO_READ: use when creating tests, benchmark harnesses, and experiment artifacts.

KEYWORDS: policy config, eval config, baseline config, reproducibility hash, fairness preflight
CANONICAL_TOPIC: config_baselines
PRIMARY_DOC: configs/policy_v0q.yaml
RELATED_DOCS: configs/eval_v0q.yaml, configs/baselines_v0q.yaml, docs/specs/04_scoring_and_trust.md, docs/specs/08_evaluation_and_metrics.md, AGENTS.md
SOURCE_SECTIONS: 12, 13.3, 13.4, 16, 17
WHEN_TO_READ: use before implementing scoring/transition logic or evaluation harness behavior.


KEYWORDS: test index, smoke tests, unit tests, test map, pytest markers
CANONICAL_TOPIC: tests_index
PRIMARY_DOC: tests/TEST_INDEX.md
RELATED_DOCS: docs/handoff/NEXT_TASK.md, docs/specs/08_evaluation_and_metrics.md, AGENTS.md
SOURCE_SECTIONS: 16, 20, 23
WHEN_TO_READ: use when selecting test layers or deciding between unit and smoke coverage.

KEYWORDS: scripts index, probe scripts, diagnostics, manual checks, developer tooling
CANONICAL_TOPIC: scripts_index
PRIMARY_DOC: scripts/SCRIPTS_INDEX.md
RELATED_DOCS: docs/handoff/NEXT_TASK.md, AGENTS.md
SOURCE_SECTIONS: 15.2, 23
WHEN_TO_READ: use when adding or running manual probe scripts outside automated tests.

KEYWORDS: config index, config registry, policy yaml, eval yaml, baselines yaml
CANONICAL_TOPIC: config_index
PRIMARY_DOC: configs/CONFIG_INDEX.md
RELATED_DOCS: configs/policy_v0q.yaml, configs/eval_v0q.yaml, configs/baselines_v0q.yaml, docs/specs/04_scoring_and_trust.md, docs/specs/08_evaluation_and_metrics.md
SOURCE_SECTIONS: 12, 16, 17, 20
WHEN_TO_READ: use when locating and updating frozen config baselines.
KEYWORDS: risks, failure modes, deferred features, non-goals, schema sprawl
CANONICAL_TOPIC: risks_non_goals_deferred
PRIMARY_DOC: docs/specs/09_risks_non_goals_deferred.md
RELATED_DOCS: docs/specs/00_scope_and_claim.md, docs/specs/10_checklists_and_dod.md
SOURCE_SECTIONS: 4.2, 19, 22, 24
WHEN_TO_READ: use when evaluating scope decisions or protecting experiment validity.

KEYWORDS: implementation checklist, definition of done, acceptance criteria, release gate
CANONICAL_TOPIC: checklists_and_definition_of_done
PRIMARY_DOC: docs/specs/10_checklists_and_dod.md
RELATED_DOCS: docs/specs/07_build_plan_and_milestones.md, docs/specs/08_evaluation_and_metrics.md
SOURCE_SECTIONS: 20, 21, 23
WHEN_TO_READ: use when verifying completion and readiness to claim v0 results.

KEYWORDS: current state, blockers, locked decisions, ready flag, required references, next task id
CANONICAL_TOPIC: handoff_current_status
PRIMARY_DOC: docs/handoff/CURRENT_STATUS.md
RELATED_DOCS: docs/handoff/NEXT_TASK.md, docs/specs/07_build_plan_and_milestones.md
SOURCE_SECTIONS: N/A (operational handoff document)
WHEN_TO_READ: read first in every fresh session before opening task docs; then read `docs/handoff/NEXT_TASK.md`, then relevant spec `PRIMARY_DOC` entries.

KEYWORDS: next task, single primary task, subtasks, quality gates, acceptance criteria, validation commands
CANONICAL_TOPIC: handoff_next_task
PRIMARY_DOC: docs/handoff/NEXT_TASK.md
RELATED_DOCS: docs/handoff/CURRENT_STATUS.md, docs/specs/10_checklists_and_dod.md
SOURCE_SECTIONS: N/A (operational handoff document)
WHEN_TO_READ: read second in every fresh session to execute one scoped task loop with fixed quality gates, then update handoff docs.

KEYWORDS: overview checklist, macro progress, milestones dashboard, definition of done readiness, program tracker
CANONICAL_TOPIC: handoff_overview_checklist
PRIMARY_DOC: docs/handoff/OVERVIEW_CHECKLIST.md
RELATED_DOCS: docs/handoff/CURRENT_STATUS.md, docs/handoff/NEXT_TASK.md, docs/specs/07_build_plan_and_milestones.md, docs/specs/10_checklists_and_dod.md
SOURCE_SECTIONS: N/A (operational handoff document)
WHEN_TO_READ: use before or after executing loop tasks to assess v0 milestone/checklist progress beyond the single active task.

KEYWORDS: conda environment, environment setup, environment.yml, pytest, mypy, ruff
CANONICAL_TOPIC: python_environment_setup
PRIMARY_DOC: README.md
RELATED_DOCS: docs/DOCS_GUIDE.md, AGENTS.md
SOURCE_SECTIONS: N/A (operational developer setup)
WHEN_TO_READ: use for human-oriented project setup and environment creation before running repository tooling.

KEYWORDS: agent startup, handoff loop, task id continuity, quality gates, conda run
CANONICAL_TOPIC: agent_runtime_workflow
PRIMARY_DOC: AGENTS.md
RELATED_DOCS: docs/handoff/CURRENT_STATUS.md, docs/handoff/NEXT_TASK.md, docs/DOCS_GUIDE.md
SOURCE_SECTIONS: N/A (operational project policy)
WHEN_TO_READ: use for fresh-agent execution workflow, handoff continuity rules, and cycle closeout checks.

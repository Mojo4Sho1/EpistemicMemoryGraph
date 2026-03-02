# EpistemicMemoryGraph

A graph-based memory framework for LLM agents that separates observations, hypotheses, and beliefs to support provenance-aware reasoning, uncertainty handling, and long-horizon memory.

## Documentation

Start with these project documents:

- Canonical source spec: `MASTER_DOC.md`
- Decomposed v0 specs: `docs/specs/`
- Technical map: `docs/INDEX.md`
- Directory mini-indexes for deep navigation: `tests/TEST_INDEX.md`, `scripts/SCRIPTS_INDEX.md`, `configs/CONFIG_INDEX.md`
- Frozen v0.1q config baselines: `configs/`
  - `configs/policy_v0q.yaml`: policy/scoring thresholds and operational gate defaults
  - `configs/eval_v0q.yaml`: evaluation stage gates, fairness constraints, and claim thresholds
  - `configs/baselines_v0q.yaml`: baseline system set and shared comparison defaults
- Documentation maintenance guide: `docs/DOCS_GUIDE.md`

### Agent Handoff Docs

- `docs/handoff/CURRENT_STATUS.md`: active state, blockers, locked/pending decisions
- `docs/handoff/NEXT_TASK.md`: single-task execution contract for current loop
- `docs/handoff/TASK_QUEUE.md`: staged M5-M10 queue with one `READY: YES` task
- `docs/handoff/DECISION_LOG.md`: open-question closure tracking
- `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md`: `SPEC_MUST_ID` tracking for gate-4 conformance
- `docs/handoff/OVERVIEW_CHECKLIST.md`: milestone/checklist/DoD evidence dashboard

## Environment Setup

Create the project environment with:

`conda env create -f environment.yml`

Run tools in that environment with:

`conda run -n emg <command>`

## Agent Workflow

For agent operation and handoff-loop rules, see `AGENTS.md`.

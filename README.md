# EpistemicMemoryGraph

A graph-based memory framework for LLM agents that separates observations, hypotheses, and beliefs to support provenance-aware reasoning, uncertainty handling, and long-horizon memory.

## Documentation

Start with these project documents:

- Canonical source spec: `MASTER_DOC.md`
- Decomposed v0 specs: `docs/specs/`
- Technical map: `docs/INDEX.md`
- Documentation maintenance guide: `docs/DOCS_GUIDE.md`

## Environment Setup

Create the project environment with:

`conda env create -f environment.yml`

Run tools in that environment with:

`conda run -n emg <command>`

## Agent Workflow

For agent operation and handoff-loop rules, see `AGENTS.md`.

# Scope and Research Claim

## Purpose

Define the v0 problem framing, research claim, scope boundaries, and design principles that govern all implementation decisions.

## Normative Requirements

- `MUST` preserve the primary research claim: explicit observation-to-proposition-to-belief governance improves long-horizon memory behavior over naive baselines.
- `MUST` keep v0 scoped to a single-agent prototype with text/tool inputs.
- `MUST NOT` include deferred capabilities (multi-agent sync, learned trust calibration, production hardening) in v0 acceptance criteria.
- `SHOULD` treat this scope as a freeze for first implementation pass.
- `MAY` add future-scope notes only under explicit deferred sections.

## Data Objects / Interfaces

- Scope anchors:
  - in-scope capabilities list
  - non-goals list
  - design principles list
- Evaluation anchors:
  - study improvement targets (belief revision, contradiction handling, calibration, consistency, integrity)

## Policy Rules / Constraints

- Governance quality is the core objective, not feature breadth.
- Architecture choices must prioritize auditability, determinism, minimal ontology, and recompute-friendly behavior.
- Any expansion that weakens the core experiment signal should be deferred.

## Edge Cases and Failure Modes

- Scope creep can invalidate benchmark interpretation.
- Premature broadening can obscure whether governance policy itself drives gains.
- Over-indexing on retrieval quality can mask governance failures.

## Open Questions

- Should a formal v0.1 changelog file be added in `docs/` for scope updates?
- Should non-goals be tagged by "defer until" milestone for planning clarity?

## Traceability to `MASTER_DOC.md`

- Source sections: 1, 2, 3, 4, 5, 22, 24
- Notes: This file captures project framing and constraints, not implementation detail.

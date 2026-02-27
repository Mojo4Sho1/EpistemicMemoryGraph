# Scoring and Trust Model

## Purpose

Specify evidence aggregation, confidence scoring heuristics, and source trust factors used by deterministic policy.

## Normative Requirements

- `MUST` keep scoring deterministic and inspectable in v0.
- `MUST` track support, contradiction, source-group diversity, freshness, and volatility modifiers per proposition.
- `MUST` saturate repeated reinforcement from the same independence group.
- `MUST` apply stricter promotion thresholds for causal claims than descriptive claims.
- `SHOULD` penalize stale high-volatility claims more aggressively.
- `MAY` adjust trust expectations gradually using historical correction rate.

## Data Objects / Interfaces

- Proposition aggregates:
  - support weight
  - contradiction weight
  - distinct source group count
  - freshness modifier
  - volatility modifier
- Source fields:
  - `source_id`, `source_type`, `base_reliability`, `domain_tags`, `independence_group`, `historical_correction_rate`

## Policy Rules / Constraints

- Trust is structured by context; no single scalar trust score for all domains.
- Raw evidence count is insufficient without independence and reliability handling.
- Time alone never upgrades weak propositions.

## Edge Cases and Failure Modes

- Correlated sources can fake confidence if independence is mis-modeled.
- Overly harsh decay can cause excessive deprecation/rejection in stable domains.
- Overly permissive source priors can flood accepted state with low-quality claims.

## Open Questions

- What exact default weight constants should initialize v0 scoring?
- Should volatility class taxonomy be fixed at three tiers for initial benchmarking?

## Traceability to `MASTER_DOC.md`

- Source sections: 11, 12, 10.5, 10.7
- Notes: Designed for ablation-friendly implementation.

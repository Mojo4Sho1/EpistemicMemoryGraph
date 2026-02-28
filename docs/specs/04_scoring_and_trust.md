# Scoring and Trust Model

## Purpose

Specify evidence aggregation, confidence scoring heuristics, and source trust factors used by deterministic policy.

## Normative Requirements

- `MUST` keep scoring deterministic and inspectable in v0.
- `MUST` track support, contradiction, source-group diversity, freshness, and volatility modifiers per proposition.
- `MUST` saturate repeated reinforcement from the same independence group with fixed v0.1q increments: 0.70, +0.20, +0.10 capped at 1.00.
- `MUST` compute freshness as `exp(-ln(2) * age_hours / half_life_hours)`.
- `MUST` freeze volatility tiers and half-lives:
  - `low`: 168 hours
  - `medium`: 72 hours
  - `high`: 24 hours
- `MUST` freeze volatility factors for staleness penalty:
  - `low`: 0.5
  - `medium`: 1.0
  - `high`: 2.0
- `MUST` compute confidence as:
  - `confidence = clamp01(0.50 + 0.40*support_score - 0.50*contradiction_score + diversity_bonus - staleness_penalty)`
- `MUST` compute diversity bonus as `min(0.15, 0.05*(distinct_support_groups-1))`.
- `MUST` compute staleness penalty as `min(0.30, (1-freshness)*volatility_factor*0.30)`.
- `SHOULD` penalize stale high-volatility claims more aggressively.
- `MAY` adjust trust expectations gradually using historical correction rate.

## Data Objects / Interfaces

- Proposition aggregates:
  - support score
  - contradiction score
  - distinct support groups
  - distinct contradiction groups
  - freshness
  - volatility tier
  - confidence
- Source fields:
  - `source_id`, `source_type`, `base_reliability`, `domain_tags`, `independence_group`, `historical_correction_rate`

## Policy Rules / Constraints

- Trust is structured by context; no single scalar trust score for all domains.
- Raw evidence count is insufficient without independence and reliability handling.
- Time alone never upgrades weak propositions.
- Same-group reinforcement after the third observation should not materially increase confidence.

## Edge Cases and Failure Modes

- Correlated sources can fake confidence if independence is mis-modeled.
- Overly harsh decay can cause excessive deprecation/rejection in stable domains.
- Overly permissive source priors can flood accepted state with low-quality claims.

## Open Questions

- None for v0.1q core scoring constants.

## Traceability to `MASTER_DOC.md`

- Source sections: 11, 12, 10.5, 10.7
- Notes: Designed for ablation-friendly implementation with frozen default constants.

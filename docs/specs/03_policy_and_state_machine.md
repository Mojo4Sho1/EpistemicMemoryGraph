# Policy and Belief State Machine

## Purpose

Define deterministic governance policy and belief lifecycle transitions for propositions.

## Normative Requirements

- `MUST` enforce the ten governance rules in policy code.
- `MUST` place every proposition in exactly one primary state at all times.
- `MUST` derive belief state from evidence signals, not direct LLM assertion.
- `MUST` preserve contradictory history; contradictions cannot erase prior evidence.
- `MUST` use fixed transition precedence: `rejected` -> `contested` -> `accepted` -> `deprecated` -> `provisional` -> `tentative`.
- `MUST` apply the frozen thresholds below for v0.1q:
  - `accepted`: confidence >= 0.80, support groups >= 2, contradiction score < 0.30, freshness >= 0.40.
  - `provisional`: confidence >= 0.55 and not in higher-precedence states.
  - `contested`: support score >= 0.45 and contradiction score >= 0.45.
  - `rejected`: failed discriminating test OR (confidence < 0.15 AND contradiction score >= 0.80 AND contradiction groups >= 2).
  - `deprecated`: prior state in `{accepted, provisional}` AND freshness < 0.20 AND no new support for one half-life.
- `MAY` retain unresolved contested items across consolidation boundaries.

## Data Objects / Interfaces

- Belief states:
  - `tentative`, `provisional`, `accepted`, `contested`, `deprecated`, `rejected`
- Transition drivers:
  - support score, contradiction score, support-group diversity, freshness, test outcomes
- Transition result contract:
  - prior state
  - next state
  - deterministic rule id
  - deterministic reason

## Policy Rules / Constraints

- All inputs become observations first.
- Observation-to-accepted direct promotion is disallowed.
- Source weighting and independence controls dominate raw repetition count.
- Dynamic-domain claims decay when unrefreshed.
- Canonical promotion requires policy compliance at consolidation.

## Edge Cases and Failure Modes

- Premature acceptance under repeated correlated sources.
- Failure to enter `contested` state on material conflict.
- Time-driven confidence inflation without new evidence.
- Transition ambiguity if precedence is not explicitly enforced.

## Open Questions

- None for v0.1q transition thresholds and precedence.

## Traceability to `MASTER_DOC.md`

- Source sections: 9, 10, 12, 13.3, 16.1
- Notes: This is the normative policy center for implementation and tests.

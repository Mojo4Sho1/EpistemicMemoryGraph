# Policy and Belief State Machine

## Purpose

Define deterministic governance policy and belief lifecycle transitions for propositions.

## Normative Requirements

- `MUST` enforce the ten governance rules in policy code.
- `MUST` place every proposition in exactly one primary state at all times.
- `MUST` derive belief state from evidence signals, not direct LLM assertion.
- `MUST` preserve contradictory history; contradictions cannot erase prior evidence.
- `SHOULD` trigger hypothesis testing only when uncertainty affects integrity or task success.
- `MAY` retain unresolved contested items across consolidation boundaries.

## Data Objects / Interfaces

- Belief states:
  - `tentative`, `provisional`, `accepted`, `contested`, `deprecated`, `rejected`
- Transition drivers:
  - support weight, contradiction weight, source independence diversity, recency/volatility effects, test outcomes

## Policy Rules / Constraints

- All inputs become observations first.
- Observation-to-accepted direct promotion is disallowed.
- Source weighting and independence controls dominate raw repetition count.
- Dynamic-domain claims must decay when unrefreshed.
- Canonical promotion requires policy compliance at consolidation.

## Edge Cases and Failure Modes

- Premature acceptance under repeated correlated sources.
- Failure to enter `contested` state on material conflict.
- Time-driven confidence inflation without new evidence.

## Open Questions

- Should contested-state demotion thresholds differ by proposition class in v0?
- Should rejection require explicit failed test evidence or can contradiction saturation suffice?

## Traceability to `MASTER_DOC.md`

- Source sections: 9, 10, 12, 13.3, 16.1
- Notes: This is the normative policy center for implementation and tests.

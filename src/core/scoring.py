"""Deterministic proposition scoring primitives for v0.1q."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp
from typing import Mapping

from src.core.policy_config import (
    DEFAULT_POLICY_CONFIG,
    PolicyConfig,
    VolatilityTier,
    group_saturation_weight,
)


@dataclass(frozen=True, slots=True)
class PropositionSignals:
    """Evidence and temporal signals used for deterministic confidence scoring."""

    support_evidence_by_group: Mapping[str, int]
    contradiction_evidence_by_group: Mapping[str, int]
    age_hours: float
    volatility: VolatilityTier


@dataclass(frozen=True, slots=True)
class ScoreBreakdown:
    """Inspectable decomposition of derived confidence and components."""

    support_score: float
    contradiction_score: float
    distinct_support_groups: int
    distinct_contradict_groups: int
    freshness: float
    volatility: VolatilityTier
    volatility_factor: float
    diversity_bonus: float
    staleness_penalty: float
    confidence: float


def score_proposition(
    signals: PropositionSignals,
    config: PolicyConfig = DEFAULT_POLICY_CONFIG,
) -> ScoreBreakdown:
    """Compute confidence with deterministic, bounded v0.1q heuristics."""

    support_score, distinct_support_groups = _aggregate_group_score(
        signals.support_evidence_by_group
    )
    contradiction_score, distinct_contradict_groups = _aggregate_group_score(
        signals.contradiction_evidence_by_group
    )

    freshness = _compute_freshness(
        age_hours=signals.age_hours,
        volatility=signals.volatility,
        config=config,
    )
    volatility_factor = config.volatility_factor[signals.volatility]
    diversity_bonus = min(0.15, 0.05 * max(0, distinct_support_groups - 1))
    staleness_penalty = min(0.30, (1.0 - freshness) * volatility_factor * 0.30)

    confidence = _clamp01(
        0.50
        + 0.40 * support_score
        - 0.50 * contradiction_score
        + diversity_bonus
        - staleness_penalty
    )

    return ScoreBreakdown(
        support_score=support_score,
        contradiction_score=contradiction_score,
        distinct_support_groups=distinct_support_groups,
        distinct_contradict_groups=distinct_contradict_groups,
        freshness=freshness,
        volatility=signals.volatility,
        volatility_factor=volatility_factor,
        diversity_bonus=diversity_bonus,
        staleness_penalty=staleness_penalty,
        confidence=confidence,
    )


def _aggregate_group_score(evidence_by_group: Mapping[str, int]) -> tuple[float, int]:
    distinct_groups = 0
    total_weight = 0.0

    for evidence_count in evidence_by_group.values():
        if evidence_count <= 0:
            continue
        distinct_groups += 1
        total_weight += group_saturation_weight(evidence_count)

    if distinct_groups == 0:
        return 0.0, 0

    return min(1.0, total_weight / distinct_groups), distinct_groups


def _compute_freshness(age_hours: float, volatility: VolatilityTier, config: PolicyConfig) -> float:
    bounded_age_hours = max(0.0, age_hours)
    half_life_hours = config.volatility_half_life_hours[volatility]
    if half_life_hours <= 0:
        return 0.0
    return exp(-config_ln2(config) * bounded_age_hours / half_life_hours)


def _clamp01(value: float) -> float:
    return min(1.0, max(0.0, value))


def config_ln2(config: PolicyConfig) -> float:
    """Expose ln(2) for deterministic half-life tests without magic literals."""

    from src.core.policy_config import LN2

    _ = config
    return LN2

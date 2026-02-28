"""Deterministic policy constants and typed defaults for v0.1q."""

from __future__ import annotations

from dataclasses import dataclass
from math import log
from typing import Literal

VolatilityTier = Literal["low", "medium", "high"]
ActionImpact = Literal["low", "high", "irreversible"]

LN2 = log(2.0)


@dataclass(frozen=True, slots=True)
class SaturationConfig:
    """Per-group evidence contribution shape for repeated observations."""

    first_evidence: float = 0.70
    second_increment: float = 0.20
    third_or_more_increment: float = 0.10
    cap: float = 1.00
    post_third_epsilon: float = 1e-9


@dataclass(frozen=True, slots=True)
class ThresholdConfig:
    """State-transition thresholds for proposition governance."""

    accepted_confidence: float = 0.80
    accepted_min_support_groups: int = 2
    accepted_max_contradiction: float = 0.30
    accepted_min_freshness: float = 0.40

    provisional_confidence: float = 0.55

    contested_min_support: float = 0.45
    contested_min_contradiction: float = 0.45

    rejected_max_confidence: float = 0.15
    rejected_min_contradiction: float = 0.80
    rejected_min_contradict_groups: int = 2

    deprecated_max_freshness: float = 0.20
    promotion_min_freshness: float = 0.35


@dataclass(frozen=True, slots=True)
class OperationalConfig:
    """Operational constants for testing triggers and consolidation behavior."""

    trigger_confidence_gap: float = 0.15
    trigger_contested_updates: int = 2
    trigger_unresolved_contradictions: int = 2
    novelty_confidence_min: float = 0.45
    novelty_confidence_max: float = 0.70
    novelty_max_support_groups: int = 1

    consolidation_cadence_observations: int = 25
    unresolved_carryover_cap: int = 20


@dataclass(frozen=True, slots=True)
class PolicyConfig:
    """Top-level immutable policy config for deterministic v0.1q behavior."""

    volatility_half_life_hours: dict[VolatilityTier, float]
    volatility_factor: dict[VolatilityTier, float]
    saturation: SaturationConfig = SaturationConfig()
    thresholds: ThresholdConfig = ThresholdConfig()
    operational: OperationalConfig = OperationalConfig()


DEFAULT_POLICY_CONFIG = PolicyConfig(
    volatility_half_life_hours={"low": 168.0, "medium": 72.0, "high": 24.0},
    volatility_factor={"low": 0.5, "medium": 1.0, "high": 2.0},
)


def group_saturation_weight(
    evidence_count: int,
    saturation: SaturationConfig = DEFAULT_POLICY_CONFIG.saturation,
) -> float:
    """Return deterministic per-group contribution with capped repeated evidence."""

    if evidence_count <= 0:
        return 0.0
    if evidence_count == 1:
        return saturation.first_evidence
    if evidence_count == 2:
        return min(saturation.cap, saturation.first_evidence + saturation.second_increment)
    return min(
        saturation.cap,
        saturation.first_evidence
        + saturation.second_increment
        + saturation.third_or_more_increment,
    )

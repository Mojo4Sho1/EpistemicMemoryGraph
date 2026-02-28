"""Tests for deterministic v0.1q scoring behavior and constraints."""

from src.core.policy_config import DEFAULT_POLICY_CONFIG
from src.core.scoring import PropositionSignals, score_proposition


def test_independent_support_never_decreases_confidence() -> None:
    base = PropositionSignals(
        support_evidence_by_group={"group-a": 1},
        contradiction_evidence_by_group={},
        age_hours=0.0,
        volatility="medium",
    )
    stronger = PropositionSignals(
        support_evidence_by_group={"group-a": 1, "group-b": 1},
        contradiction_evidence_by_group={},
        age_hours=0.0,
        volatility="medium",
    )

    base_score = score_proposition(base)
    stronger_score = score_proposition(stronger)

    assert stronger_score.confidence >= base_score.confidence


def test_same_group_support_saturates_after_third_observation() -> None:
    third = PropositionSignals(
        support_evidence_by_group={"group-a": 3},
        contradiction_evidence_by_group={},
        age_hours=0.0,
        volatility="medium",
    )
    later = PropositionSignals(
        support_evidence_by_group={"group-a": 8},
        contradiction_evidence_by_group={},
        age_hours=0.0,
        volatility="medium",
    )

    third_score = score_proposition(third)
    later_score = score_proposition(later)

    delta = abs(later_score.confidence - third_score.confidence)
    assert delta <= DEFAULT_POLICY_CONFIG.saturation.post_third_epsilon


def test_time_decay_never_increases_confidence() -> None:
    newer = PropositionSignals(
        support_evidence_by_group={"group-a": 1, "group-b": 1},
        contradiction_evidence_by_group={},
        age_hours=1.0,
        volatility="high",
    )
    older = PropositionSignals(
        support_evidence_by_group={"group-a": 1, "group-b": 1},
        contradiction_evidence_by_group={},
        age_hours=200.0,
        volatility="high",
    )

    newer_score = score_proposition(newer)
    older_score = score_proposition(older)

    assert older_score.confidence <= newer_score.confidence


def test_half_life_freshness_is_point_five() -> None:
    half_life_age = PropositionSignals(
        support_evidence_by_group={"group-a": 1},
        contradiction_evidence_by_group={},
        age_hours=72.0,
        volatility="medium",
    )

    score = score_proposition(half_life_age)

    assert score.freshness == 0.5

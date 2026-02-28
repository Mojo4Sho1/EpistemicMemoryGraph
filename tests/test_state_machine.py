"""Tests for deterministic v0.1q belief-state transition behavior."""

from src.core.policy_config import VolatilityTier
from src.core.scoring import ScoreBreakdown
from src.core.state_machine import StateTransitionInput, evaluate_transition


def _score(
    *,
    support_score: float,
    contradiction_score: float,
    confidence: float,
    distinct_support_groups: int,
    distinct_contradict_groups: int,
    freshness: float,
    volatility: VolatilityTier = "medium",
) -> ScoreBreakdown:
    return ScoreBreakdown(
        support_score=support_score,
        contradiction_score=contradiction_score,
        distinct_support_groups=distinct_support_groups,
        distinct_contradict_groups=distinct_contradict_groups,
        freshness=freshness,
        volatility=volatility,
        volatility_factor=1.0,
        diversity_bonus=0.0,
        staleness_penalty=0.0,
        confidence=confidence,
    )


def test_failed_discriminating_test_forces_rejected() -> None:
    decision = evaluate_transition(
        StateTransitionInput(
            current_state="provisional",
            score=_score(
                support_score=0.9,
                contradiction_score=0.0,
                confidence=0.95,
                distinct_support_groups=3,
                distinct_contradict_groups=0,
                freshness=1.0,
            ),
            failed_discriminating_test=True,
        )
    )

    assert decision.next_state == "rejected"
    assert decision.rule_id == "transition.rejected.failed_test"


def test_rejected_precedence_over_contested() -> None:
    decision = evaluate_transition(
        StateTransitionInput(
            current_state="tentative",
            score=_score(
                support_score=0.7,
                contradiction_score=0.9,
                confidence=0.1,
                distinct_support_groups=2,
                distinct_contradict_groups=2,
                freshness=0.8,
            ),
        )
    )

    assert decision.next_state == "rejected"


def test_accepts_when_policy_thresholds_are_met() -> None:
    decision = evaluate_transition(
        StateTransitionInput(
            current_state="provisional",
            score=_score(
                support_score=0.8,
                contradiction_score=0.2,
                confidence=0.81,
                distinct_support_groups=2,
                distinct_contradict_groups=1,
                freshness=0.5,
            ),
        )
    )

    assert decision.next_state == "accepted"


def test_deprecated_when_stale_for_one_half_life_without_support() -> None:
    decision = evaluate_transition(
        StateTransitionInput(
            current_state="accepted",
            score=_score(
                support_score=0.3,
                contradiction_score=0.1,
                confidence=0.40,
                distinct_support_groups=1,
                distinct_contradict_groups=1,
                freshness=0.1,
                volatility="medium",
            ),
            hours_since_last_support=72.0,
        )
    )

    assert decision.next_state == "deprecated"


def test_provisional_when_confidence_crosses_threshold_only() -> None:
    decision = evaluate_transition(
        StateTransitionInput(
            current_state="tentative",
            score=_score(
                support_score=0.4,
                contradiction_score=0.1,
                confidence=0.60,
                distinct_support_groups=1,
                distinct_contradict_groups=1,
                freshness=0.8,
            ),
        )
    )

    assert decision.next_state == "provisional"


def test_tentative_when_no_higher_threshold_matches() -> None:
    decision = evaluate_transition(
        StateTransitionInput(
            current_state="tentative",
            score=_score(
                support_score=0.2,
                contradiction_score=0.1,
                confidence=0.30,
                distinct_support_groups=1,
                distinct_contradict_groups=1,
                freshness=0.9,
            ),
        )
    )

    assert decision.next_state == "tentative"

"""Tests for deterministic v0.1q hypothesis-test trigger logic."""

from src.core.test_trigger import TestTriggerInput as TriggerInput
from src.core.test_trigger import evaluate_test_trigger


def test_low_impact_high_cost_suppresses_trigger() -> None:
    decision = evaluate_test_trigger(
        TriggerInput(
            action_impact="low",
            top_two_confidence_gap=0.01,
            contested_consecutive_updates=3,
            unresolved_contradiction_count=3,
            is_high_impact_novelty=True,
            candidate_confidence=0.60,
            distinct_support_groups=1,
            estimated_test_cost=0.8,
            estimated_benefit=0.2,
        )
    )

    assert decision.should_trigger is False
    assert decision.suppressed is True


def test_high_impact_small_gap_triggers() -> None:
    decision = evaluate_test_trigger(
        TriggerInput(
            action_impact="high",
            top_two_confidence_gap=0.10,
            contested_consecutive_updates=0,
            unresolved_contradiction_count=0,
            is_high_impact_novelty=False,
            candidate_confidence=0.2,
            distinct_support_groups=3,
            estimated_test_cost=0.1,
            estimated_benefit=0.8,
        )
    )

    assert decision.should_trigger is True
    assert decision.rule_id == "trigger.high_impact_small_gap"


def test_rule_order_prefers_high_impact_gap_when_multiple_rules_match() -> None:
    decision = evaluate_test_trigger(
        TriggerInput(
            action_impact="irreversible",
            top_two_confidence_gap=0.10,
            contested_consecutive_updates=3,
            unresolved_contradiction_count=4,
            is_high_impact_novelty=True,
            candidate_confidence=0.60,
            distinct_support_groups=1,
            estimated_test_cost=0.1,
            estimated_benefit=0.8,
        )
    )

    assert decision.should_trigger is True
    assert decision.rule_id == "trigger.high_impact_small_gap"


def test_contested_persistence_triggers() -> None:
    decision = evaluate_test_trigger(
        TriggerInput(
            action_impact="high",
            top_two_confidence_gap=0.4,
            contested_consecutive_updates=2,
            unresolved_contradiction_count=0,
            is_high_impact_novelty=False,
            candidate_confidence=0.2,
            distinct_support_groups=2,
            estimated_test_cost=0.1,
            estimated_benefit=0.8,
        )
    )

    assert decision.should_trigger is True
    assert decision.rule_id == "trigger.contested_persistence"


def test_rule_order_prefers_contested_over_lower_priority_rules() -> None:
    decision = evaluate_test_trigger(
        TriggerInput(
            action_impact="high",
            top_two_confidence_gap=0.4,
            contested_consecutive_updates=2,
            unresolved_contradiction_count=3,
            is_high_impact_novelty=True,
            candidate_confidence=0.60,
            distinct_support_groups=1,
            estimated_test_cost=0.1,
            estimated_benefit=0.8,
        )
    )

    assert decision.should_trigger is True
    assert decision.rule_id == "trigger.contested_persistence"


def test_unresolved_contradictions_trigger() -> None:
    decision = evaluate_test_trigger(
        TriggerInput(
            action_impact="high",
            top_two_confidence_gap=0.4,
            contested_consecutive_updates=1,
            unresolved_contradiction_count=2,
            is_high_impact_novelty=False,
            candidate_confidence=0.3,
            distinct_support_groups=2,
            estimated_test_cost=0.1,
            estimated_benefit=0.8,
        )
    )

    assert decision.should_trigger is True
    assert decision.rule_id == "trigger.unresolved_contradictions"


def test_rule_order_prefers_unresolved_contradictions_over_novelty() -> None:
    decision = evaluate_test_trigger(
        TriggerInput(
            action_impact="high",
            top_two_confidence_gap=0.4,
            contested_consecutive_updates=1,
            unresolved_contradiction_count=2,
            is_high_impact_novelty=True,
            candidate_confidence=0.60,
            distinct_support_groups=1,
            estimated_test_cost=0.1,
            estimated_benefit=0.8,
        )
    )

    assert decision.should_trigger is True
    assert decision.rule_id == "trigger.unresolved_contradictions"


def test_high_impact_novelty_trigger() -> None:
    decision = evaluate_test_trigger(
        TriggerInput(
            action_impact="high",
            top_two_confidence_gap=0.4,
            contested_consecutive_updates=1,
            unresolved_contradiction_count=1,
            is_high_impact_novelty=True,
            candidate_confidence=0.60,
            distinct_support_groups=1,
            estimated_test_cost=0.1,
            estimated_benefit=0.8,
        )
    )

    assert decision.should_trigger is True
    assert decision.rule_id == "trigger.high_impact_novelty"


def test_low_impact_cost_equal_bounded_benefit_is_not_suppressed() -> None:
    decision = evaluate_test_trigger(
        TriggerInput(
            action_impact="low",
            top_two_confidence_gap=0.4,
            contested_consecutive_updates=2,
            unresolved_contradiction_count=0,
            is_high_impact_novelty=False,
            candidate_confidence=0.2,
            distinct_support_groups=2,
            estimated_test_cost=0.2,
            estimated_benefit=0.2,
        )
    )

    assert decision.suppressed is False
    assert decision.should_trigger is True
    assert decision.rule_id == "trigger.contested_persistence"


def test_low_impact_suppression_uses_bounded_benefit_floor() -> None:
    decision = evaluate_test_trigger(
        TriggerInput(
            action_impact="low",
            top_two_confidence_gap=0.4,
            contested_consecutive_updates=0,
            unresolved_contradiction_count=0,
            is_high_impact_novelty=False,
            candidate_confidence=0.2,
            distinct_support_groups=2,
            estimated_test_cost=0.01,
            estimated_benefit=-5.0,
        )
    )

    assert decision.should_trigger is False
    assert decision.suppressed is True
    assert decision.rule_id == "trigger.suppressed.low_impact_cost"


def test_low_impact_suppression_uses_bounded_benefit_cap() -> None:
    decision = evaluate_test_trigger(
        TriggerInput(
            action_impact="low",
            top_two_confidence_gap=0.4,
            contested_consecutive_updates=0,
            unresolved_contradiction_count=0,
            is_high_impact_novelty=False,
            candidate_confidence=0.2,
            distinct_support_groups=2,
            estimated_test_cost=1.1,
            estimated_benefit=5.0,
        )
    )

    assert decision.should_trigger is False
    assert decision.suppressed is True
    assert decision.rule_id == "trigger.suppressed.low_impact_cost"


def test_no_rule_match_returns_no_trigger() -> None:
    decision = evaluate_test_trigger(
        TriggerInput(
            action_impact="high",
            top_two_confidence_gap=0.5,
            contested_consecutive_updates=0,
            unresolved_contradiction_count=0,
            is_high_impact_novelty=False,
            candidate_confidence=0.2,
            distinct_support_groups=2,
            estimated_test_cost=0.1,
            estimated_benefit=0.8,
        )
    )

    assert decision.should_trigger is False
    assert decision.rule_id == "trigger.none"

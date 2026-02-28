"""Deterministic hypothesis-test trigger and suppression rules for v0.1q."""

from __future__ import annotations

from dataclasses import dataclass

from src.core.policy_config import (
    DEFAULT_POLICY_CONFIG,
    ActionImpact,
    PolicyConfig,
)


@dataclass(frozen=True, slots=True)
class TestTriggerInput:
    """Inputs used to evaluate hard-rule test triggering."""

    action_impact: ActionImpact
    top_two_confidence_gap: float
    contested_consecutive_updates: int
    unresolved_contradiction_count: int
    is_high_impact_novelty: bool
    candidate_confidence: float
    distinct_support_groups: int
    estimated_test_cost: float
    estimated_benefit: float


@dataclass(frozen=True, slots=True)
class TestTriggerDecision:
    """Output for deterministic trigger evaluation with rule traceability."""

    should_trigger: bool
    rule_id: str
    reason: str
    suppressed: bool


def evaluate_test_trigger(
    trigger_input: TestTriggerInput,
    config: PolicyConfig = DEFAULT_POLICY_CONFIG,
) -> TestTriggerDecision:
    """Evaluate ordered hard rules and low-impact suppression semantics."""

    if _is_suppressed(trigger_input):
        return TestTriggerDecision(
            should_trigger=False,
            rule_id="trigger.suppressed.low_impact_cost",
            reason="Low-impact action with test cost greater than bounded benefit.",
            suppressed=True,
        )

    rules = (
        _rule_high_impact_gap(trigger_input, config),
        _rule_contested_persistence(trigger_input, config),
        _rule_unresolved_contradictions(trigger_input, config),
        _rule_high_impact_novelty(trigger_input, config),
    )

    for should_trigger, rule_id, reason in rules:
        if should_trigger:
            return TestTriggerDecision(
                should_trigger=True,
                rule_id=rule_id,
                reason=reason,
                suppressed=False,
            )

    return TestTriggerDecision(
        should_trigger=False,
        rule_id="trigger.none",
        reason="No trigger rule satisfied.",
        suppressed=False,
    )


def _is_suppressed(trigger_input: TestTriggerInput) -> bool:
    bounded_benefit = max(0.0, min(1.0, trigger_input.estimated_benefit))
    return (
        trigger_input.action_impact == "low"
        and trigger_input.estimated_test_cost > bounded_benefit
    )


def _rule_high_impact_gap(
    trigger_input: TestTriggerInput,
    config: PolicyConfig,
) -> tuple[bool, str, str]:
    impact_is_high = trigger_input.action_impact in {"high", "irreversible"}
    confidence_gap_small = (
        trigger_input.top_two_confidence_gap < config.operational.trigger_confidence_gap
    )

    return (
        impact_is_high and confidence_gap_small,
        "trigger.high_impact_small_gap",
        "High/irreversible action with unresolved top proposition gap.",
    )


def _rule_contested_persistence(
    trigger_input: TestTriggerInput,
    config: PolicyConfig,
) -> tuple[bool, str, str]:
    return (
        trigger_input.contested_consecutive_updates
        >= config.operational.trigger_contested_updates,
        "trigger.contested_persistence",
        "Proposition stayed contested across required consecutive updates.",
    )


def _rule_unresolved_contradictions(
    trigger_input: TestTriggerInput,
    config: PolicyConfig,
) -> tuple[bool, str, str]:
    return (
        trigger_input.unresolved_contradiction_count
        >= config.operational.trigger_unresolved_contradictions,
        "trigger.unresolved_contradictions",
        "Unresolved contradiction count reached trigger threshold.",
    )


def _rule_high_impact_novelty(
    trigger_input: TestTriggerInput,
    config: PolicyConfig,
) -> tuple[bool, str, str]:
    confidence_in_band = (
        config.operational.novelty_confidence_min
        <= trigger_input.candidate_confidence
        <= config.operational.novelty_confidence_max
    )
    insufficient_independence = (
        trigger_input.distinct_support_groups
        <= config.operational.novelty_max_support_groups
    )

    return (
        trigger_input.is_high_impact_novelty and confidence_in_band and insufficient_independence,
        "trigger.high_impact_novelty",
        "High-impact novelty requires discriminating evidence before commitment.",
    )

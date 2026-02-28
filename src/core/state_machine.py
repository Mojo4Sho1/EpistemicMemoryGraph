"""Deterministic belief-state transition logic for v0.1q governance."""

from __future__ import annotations

from dataclasses import dataclass

from src.core.constants import BELIEF_STATES
from src.core.policy_config import DEFAULT_POLICY_CONFIG, PolicyConfig
from src.core.scoring import ScoreBreakdown


@dataclass(frozen=True, slots=True)
class StateTransitionInput:
    """Inputs required to evaluate deterministic belief-state transitions."""

    current_state: str
    score: ScoreBreakdown
    failed_discriminating_test: bool = False
    hours_since_last_support: float | None = None


@dataclass(frozen=True, slots=True)
class TransitionDecision:
    """Result of deterministic transition evaluation with traceable rule id."""

    prior_state: str
    next_state: str
    rule_id: str
    reason: str


def evaluate_transition(
    transition_input: StateTransitionInput,
    config: PolicyConfig = DEFAULT_POLICY_CONFIG,
) -> TransitionDecision:
    """Apply fixed precedence: rejected -> contested -> accepted -> deprecated -> provisional."""

    prior_state = transition_input.current_state
    if prior_state not in BELIEF_STATES:
        msg = f"Unsupported belief state: {prior_state}"
        raise ValueError(msg)

    score = transition_input.score
    thresholds = config.thresholds

    if transition_input.failed_discriminating_test:
        return TransitionDecision(
            prior_state=prior_state,
            next_state="rejected",
            rule_id="transition.rejected.failed_test",
            reason="Discriminating test failed.",
        )

    if (
        score.confidence < thresholds.rejected_max_confidence
        and score.contradiction_score >= thresholds.rejected_min_contradiction
        and score.distinct_contradict_groups >= thresholds.rejected_min_contradict_groups
    ):
        return TransitionDecision(
            prior_state=prior_state,
            next_state="rejected",
            rule_id="transition.rejected.contradiction_saturation",
            reason="Confidence is critically low under strong independent contradiction.",
        )

    if (
        score.support_score >= thresholds.contested_min_support
        and score.contradiction_score >= thresholds.contested_min_contradiction
    ):
        return TransitionDecision(
            prior_state=prior_state,
            next_state="contested",
            rule_id="transition.contested.material_conflict",
            reason="Material support and contradiction are simultaneously present.",
        )

    if (
        score.confidence >= thresholds.accepted_confidence
        and score.distinct_support_groups >= thresholds.accepted_min_support_groups
        and score.contradiction_score < thresholds.accepted_max_contradiction
        and score.freshness >= thresholds.accepted_min_freshness
    ):
        return TransitionDecision(
            prior_state=prior_state,
            next_state="accepted",
            rule_id="transition.accepted.policy_threshold",
            reason="Acceptance thresholds satisfied.",
        )

    if _should_deprecate(transition_input, config):
        return TransitionDecision(
            prior_state=prior_state,
            next_state="deprecated",
            rule_id="transition.deprecated.staleness",
            reason="Prior useful proposition became stale without refresh.",
        )

    if score.confidence >= thresholds.provisional_confidence:
        return TransitionDecision(
            prior_state=prior_state,
            next_state="provisional",
            rule_id="transition.provisional.supported",
            reason="Confidence reached provisional threshold.",
        )

    return TransitionDecision(
        prior_state=prior_state,
        next_state="tentative",
        rule_id="transition.tentative.default",
        reason="Insufficient evidence for higher states.",
    )


def _should_deprecate(
    transition_input: StateTransitionInput,
    config: PolicyConfig,
) -> bool:
    prior_state = transition_input.current_state
    if prior_state not in {"accepted", "provisional"}:
        return False

    if transition_input.score.freshness >= config.thresholds.deprecated_max_freshness:
        return False

    hours_since_last_support = transition_input.hours_since_last_support
    if hours_since_last_support is None:
        return False

    half_life_hours = config.volatility_half_life_hours[transition_input.score.volatility]
    return hours_since_last_support >= half_life_hours

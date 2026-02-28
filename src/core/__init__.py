"""Core package exports for v0 policy and model primitives."""

from src.core.constants import BELIEF_STATES, EDGE_TYPES
from src.core.models import Entity, Observation, Proposition
from src.core.policy_config import (
    DEFAULT_POLICY_CONFIG,
    ActionImpact,
    PolicyConfig,
    VolatilityTier,
)
from src.core.scoring import PropositionSignals, ScoreBreakdown, score_proposition
from src.core.state_machine import (
    StateTransitionInput,
    TransitionDecision,
    evaluate_transition,
)
from src.core.test_trigger import TestTriggerDecision, TestTriggerInput, evaluate_test_trigger

__all__ = [
    "ActionImpact",
    "BELIEF_STATES",
    "DEFAULT_POLICY_CONFIG",
    "EDGE_TYPES",
    "Entity",
    "Observation",
    "PolicyConfig",
    "Proposition",
    "PropositionSignals",
    "ScoreBreakdown",
    "StateTransitionInput",
    "TestTriggerDecision",
    "TestTriggerInput",
    "TransitionDecision",
    "VolatilityTier",
    "evaluate_test_trigger",
    "evaluate_transition",
    "score_proposition",
]

"""Tests for v0.1q consolidation cadence, carryover cap, and promotion gates."""

import pytest

from src.workspace import (
    apply_unresolved_carryover_cap,
    evaluate_promotion_eligibility,
    should_run_consolidation,
)


def test_task_boundary_forces_consolidation() -> None:
    decision = should_run_consolidation(
        new_observations_since_last=1,
        at_task_boundary=True,
    )

    assert decision.should_consolidate is True
    assert decision.rule_id == "consolidation.task_boundary"
    assert decision.reason == "Consolidation required at task boundary."


def test_task_boundary_takes_precedence_over_cadence() -> None:
    decision = should_run_consolidation(
        new_observations_since_last=25,
        at_task_boundary=True,
    )

    assert decision.should_consolidate is True
    assert decision.rule_id == "consolidation.task_boundary"


@pytest.mark.parametrize("new_observations", [25, 50, 75])
def test_observation_cadence_triggers_consolidation_at_multiples(
    new_observations: int,
) -> None:
    decision = should_run_consolidation(
        new_observations_since_last=new_observations,
        at_task_boundary=False,
    )

    assert decision.should_consolidate is True
    assert decision.rule_id == "consolidation.cadence.25"
    assert decision.reason == "Consolidation cadence threshold reached."


@pytest.mark.parametrize("new_observations", [0, 1, 24, 26, 49])
def test_consolidation_not_due_when_no_boundary_or_cadence_hit(
    new_observations: int,
) -> None:
    decision = should_run_consolidation(
        new_observations_since_last=new_observations,
        at_task_boundary=False,
    )

    assert decision.should_consolidate is False
    assert decision.rule_id == "consolidation.not_due"
    assert decision.reason == "Cadence threshold not reached and no task boundary."


def test_unresolved_carryover_cap_archives_overflow_in_input_order() -> None:
    unresolved = tuple(f"prop-{i}" for i in range(25))

    decision = apply_unresolved_carryover_cap(unresolved)

    assert decision.retained_ids == unresolved[:20]
    assert decision.archived_overflow_ids == unresolved[20:]
    assert decision.overflow_reason_code == "carryover_cap_exceeded"


@pytest.mark.parametrize("count", [0, 5, 20])
def test_unresolved_carryover_cap_no_overflow_when_at_or_below_cap(count: int) -> None:
    unresolved = tuple(f"prop-{i}" for i in range(count))

    decision = apply_unresolved_carryover_cap(unresolved)

    assert decision.retained_ids == unresolved
    assert decision.archived_overflow_ids == ()
    assert decision.overflow_reason_code is None


def test_unresolved_carryover_cap_zero_archives_everything() -> None:
    unresolved = ("prop-a", "prop-b", "prop-c")

    decision = apply_unresolved_carryover_cap(unresolved, cap=0)

    assert decision.retained_ids == ()
    assert decision.archived_overflow_ids == unresolved
    assert decision.overflow_reason_code == "carryover_cap_exceeded"


def test_promotion_accepted_state_is_eligible_at_freshness_threshold() -> None:
    decision = evaluate_promotion_eligibility(
        proposition_state="accepted",
        freshness=0.35,
    )

    assert decision.eligible is True
    assert decision.rule_id == "promotion.eligible"
    assert decision.reason == "State and freshness thresholds satisfied."


def test_promotion_rejects_accepted_state_below_freshness_threshold() -> None:
    decision = evaluate_promotion_eligibility(
        proposition_state="accepted",
        freshness=0.349999,
    )

    assert decision.eligible is False
    assert decision.rule_id == "promotion.ineligible.freshness"
    assert decision.reason == "Accepted proposition freshness below promotion threshold."


def test_promotion_requires_accepted_state_even_when_fresh() -> None:
    decision = evaluate_promotion_eligibility(
        proposition_state="provisional",
        freshness=0.9,
    )

    assert decision.eligible is False
    assert decision.rule_id == "promotion.ineligible.state"
    assert decision.reason == "Only accepted propositions are eligible for promotion."


def test_promotion_state_check_precedes_freshness_check() -> None:
    decision = evaluate_promotion_eligibility(
        proposition_state="tentative",
        freshness=0.0,
    )

    assert decision.eligible is False
    assert decision.rule_id == "promotion.ineligible.state"

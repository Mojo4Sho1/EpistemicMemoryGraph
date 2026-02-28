"""Tests for v0.1q consolidation cadence, carryover cap, and promotion gates."""

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


def test_observation_cadence_triggers_consolidation() -> None:
    decision = should_run_consolidation(
        new_observations_since_last=25,
        at_task_boundary=False,
    )

    assert decision.should_consolidate is True
    assert decision.rule_id == "consolidation.cadence.25"


def test_consolidation_not_due_when_no_boundary_or_cadence_hit() -> None:
    decision = should_run_consolidation(
        new_observations_since_last=24,
        at_task_boundary=False,
    )

    assert decision.should_consolidate is False


def test_unresolved_carryover_cap_archives_overflow() -> None:
    unresolved = [f"prop-{i}" for i in range(25)]

    decision = apply_unresolved_carryover_cap(unresolved)

    assert len(decision.retained_ids) == 20
    assert len(decision.archived_overflow_ids) == 5
    assert decision.overflow_reason_code == "carryover_cap_exceeded"


def test_promotion_requires_accepted_state_and_freshness() -> None:
    eligible = evaluate_promotion_eligibility(
        proposition_state="accepted",
        freshness=0.35,
    )
    stale = evaluate_promotion_eligibility(
        proposition_state="accepted",
        freshness=0.2,
    )
    wrong_state = evaluate_promotion_eligibility(
        proposition_state="provisional",
        freshness=0.9,
    )

    assert eligible.eligible is True
    assert stale.eligible is False
    assert wrong_state.eligible is False

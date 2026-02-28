"""Deterministic consolidation gates and carryover policy for v0.1q."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from src.core.policy_config import DEFAULT_POLICY_CONFIG


@dataclass(frozen=True, slots=True)
class ConsolidationDecision:
    """Whether consolidation should run for current workspace checkpoint."""

    should_consolidate: bool
    rule_id: str
    reason: str


@dataclass(frozen=True, slots=True)
class CarryoverDecision:
    """Deterministic carryover cap output with explicit archival overflow."""

    retained_ids: tuple[str, ...]
    archived_overflow_ids: tuple[str, ...]
    overflow_reason_code: str | None


@dataclass(frozen=True, slots=True)
class PromotionDecision:
    """Promotion gate decision for workspace propositions at consolidation."""

    eligible: bool
    rule_id: str
    reason: str


def should_run_consolidation(
    *,
    new_observations_since_last: int,
    at_task_boundary: bool,
    cadence: int = DEFAULT_POLICY_CONFIG.operational.consolidation_cadence_observations,
) -> ConsolidationDecision:
    """Apply fixed task-boundary + every-N-observations consolidation cadence."""

    if at_task_boundary:
        return ConsolidationDecision(
            should_consolidate=True,
            rule_id="consolidation.task_boundary",
            reason="Consolidation required at task boundary.",
        )

    if new_observations_since_last > 0 and new_observations_since_last % cadence == 0:
        return ConsolidationDecision(
            should_consolidate=True,
            rule_id="consolidation.cadence.25",
            reason="Consolidation cadence threshold reached.",
        )

    return ConsolidationDecision(
        should_consolidate=False,
        rule_id="consolidation.not_due",
        reason="Cadence threshold not reached and no task boundary.",
    )


def apply_unresolved_carryover_cap(
    unresolved_ids: Sequence[str],
    cap: int = DEFAULT_POLICY_CONFIG.operational.unresolved_carryover_cap,
) -> CarryoverDecision:
    """Retain up to cap unresolved ids and archive deterministic overflow."""

    retained = tuple(unresolved_ids[:cap])
    overflow = tuple(unresolved_ids[cap:])
    return CarryoverDecision(
        retained_ids=retained,
        archived_overflow_ids=overflow,
        overflow_reason_code="carryover_cap_exceeded" if overflow else None,
    )


def evaluate_promotion_eligibility(
    *,
    proposition_state: str,
    freshness: float,
    min_freshness: float = DEFAULT_POLICY_CONFIG.thresholds.promotion_min_freshness,
) -> PromotionDecision:
    """Require accepted state plus minimum freshness for canonical promotion."""

    if proposition_state != "accepted":
        return PromotionDecision(
            eligible=False,
            rule_id="promotion.ineligible.state",
            reason="Only accepted propositions are eligible for promotion.",
        )

    if freshness < min_freshness:
        return PromotionDecision(
            eligible=False,
            rule_id="promotion.ineligible.freshness",
            reason="Accepted proposition freshness below promotion threshold.",
        )

    return PromotionDecision(
        eligible=True,
        rule_id="promotion.eligible",
        reason="State and freshness thresholds satisfied.",
    )

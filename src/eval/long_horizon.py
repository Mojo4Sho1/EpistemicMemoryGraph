"""Deterministic Stage 4 long-horizon study workflow and interpretable-benefit checks."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

from src.eval.artifacts import write_run_artifacts
from src.eval.baselines import (
    GOVERNED_SYSTEM,
    RAW_LOG_BASELINE_SYSTEM,
    BaselineFairnessError,
)
from src.eval.fairness import BaselineRunSpec, check_baseline_fairness
from src.eval.schemas import AggregateMetrics, ConsolidationEvent, ScenarioResult, TransitionEvent

LONG_HORIZON_REQUIRED_SYSTEMS: tuple[str, ...] = (
    RAW_LOG_BASELINE_SYSTEM,
    GOVERNED_SYSTEM,
)
LONG_HORIZON_REQUIRED_ARTIFACT_FILES: tuple[str, ...] = (
    "manifest.json",
    "config_snapshot.yaml",
    "transitions.jsonl",
    "consolidation_events.jsonl",
    "scenario_results.jsonl",
    "metrics_summary.json",
)


@dataclass(frozen=True, slots=True)
class LongHorizonTaskFamily:
    """Deterministic Stage 4 task-family envelope."""

    family_id: str
    description: str
    governance_baseline: float
    governance_governed: float
    continuity_baseline: float
    continuity_governed: float


@dataclass(frozen=True, slots=True)
class LongHorizonRunRecord:
    """One emitted Stage 4 run artifact record."""

    family_id: str
    system: str
    seed: int
    run_dir: Path


@dataclass(frozen=True, slots=True)
class LongHorizonFamilyOutcome:
    """Interpretable-governance and continuity deltas for one task family."""

    family_id: str
    governance_metric_name: str
    continuity_metric_name: str
    governance_baseline: float
    governance_governed: float
    continuity_baseline: float
    continuity_governed: float
    governance_improvement: float
    continuity_improvement: float
    governance_improved: bool
    continuity_improved: bool
    paired_improvement: bool


@dataclass(frozen=True, slots=True)
class LongHorizonStudyResult:
    """Stage 4 interpretable-benefit summary across task families."""

    outcomes: tuple[LongHorizonFamilyOutcome, ...]
    task_families_with_paired_improvement: tuple[str, ...]
    interpretable_benefit_passed: bool


class LongHorizonContractError(ValueError):
    """Raised when Stage 4 inputs violate deterministic contract expectations."""


class LongHorizonStudyHarness:
    """Deterministic Stage 4 runner over long-horizon task families."""

    def __init__(
        self,
        *,
        required_systems: tuple[str, ...] = LONG_HORIZON_REQUIRED_SYSTEMS,
        required_artifact_files: tuple[str, ...] = LONG_HORIZON_REQUIRED_ARTIFACT_FILES,
    ) -> None:
        self._required_systems = required_systems
        self._required_artifact_files = required_artifact_files

    def run_stage4(
        self,
        *,
        artifacts_root: Path,
        run_date: datetime,
        git_sha: str,
        model_id: str,
        model_metadata: dict[str, str] | None = None,
        seeds: tuple[int, ...],
        run_specs: Mapping[str, BaselineRunSpec],
        config_snapshot: Mapping[str, Any],
        task_families: tuple[LongHorizonTaskFamily, ...],
    ) -> tuple[LongHorizonRunRecord, ...]:
        """Execute deterministic Stage 4 artifact runs for required systems and families."""

        if not task_families:
            raise LongHorizonContractError("Stage 4 requires at least one task family.")
        if not seeds:
            raise LongHorizonContractError("Stage 4 requires at least one seed.")

        self._ensure_required_system_coverage(tuple(run_specs), label="run_specs")
        fairness_result = check_baseline_fairness(run_specs)
        if not fairness_result.passed:
            raise BaselineFairnessError(fairness_result.violations)

        family_ids = [family.family_id for family in task_families]
        if len(set(family_ids)) != len(family_ids):
            raise LongHorizonContractError("Stage 4 task family ids must be unique.")

        records: list[LongHorizonRunRecord] = []
        config_payload = dict(config_snapshot)
        for family in task_families:
            for system in self._required_systems:
                for seed in seeds:
                    scenario_results = self._build_scenario_results(
                        family=family,
                        system=system,
                        seed=seed,
                    )
                    metrics_summary = _build_family_metrics(
                        family=family,
                        system=system,
                        seeds=seeds,
                    )
                    run_dir = write_run_artifacts(
                        artifacts_root=artifacts_root,
                        run_date=run_date,
                        git_sha=git_sha,
                        system=f"{system}_{family.family_id}",
                        seed=seed,
                        model_id=model_id,
                        config_snapshot=config_payload,
                        scenario_bundle={
                            "stage": "long_horizon",
                            "family_id": family.family_id,
                            "description": family.description,
                        },
                        transitions=[
                            self._build_transition_event(
                                family=family,
                                system=system,
                                seed=seed,
                            )
                        ],
                        consolidation_events=[
                            self._build_consolidation_event(
                                family=family, system=system, seed=seed
                            )
                        ],
                        scenario_results=scenario_results,
                        metrics_summary=metrics_summary,
                        model_metadata=model_metadata,
                    )
                    self._ensure_required_artifacts(run_dir)
                    records.append(
                        LongHorizonRunRecord(
                            family_id=family.family_id,
                            system=system,
                            seed=seed,
                            run_dir=run_dir,
                        )
                    )

        return tuple(records)

    def _ensure_required_system_coverage(
        self, actual_systems: tuple[str, ...], *, label: str
    ) -> None:
        required = set(self._required_systems)
        actual = set(actual_systems)
        if actual != required:
            missing = tuple(sorted(required - actual))
            extra = tuple(sorted(actual - required))
            raise LongHorizonContractError(
                f"{label} mismatch for Stage 4 required systems; missing={missing}, extra={extra}"
            )

    def _build_scenario_results(
        self, *, family: LongHorizonTaskFamily, system: str, seed: int
    ) -> tuple[ScenarioResult, ...]:
        if system == RAW_LOG_BASELINE_SYSTEM:
            governance_value = family.governance_baseline
            continuity_value = family.continuity_baseline
        else:
            governance_value = family.governance_governed
            continuity_value = family.continuity_governed

        return (
            ScenarioResult(
                stage="long_horizon",
                scenario_id=f"{family.family_id}-lh",
                system=system,
                seed=seed,
                task_success=continuity_value >= 0.5,
                policy_metrics={"false_promotion_rate": governance_value},
                identity_metrics={},
                memory_health_metrics={},
                task_metrics={"context_retention_success_rate": continuity_value},
            ),
        )

    def _build_transition_event(
        self,
        *,
        family: LongHorizonTaskFamily,
        system: str,
        seed: int,
    ) -> TransitionEvent:
        run_tag = f"{family.family_id}-{system}-{seed}"
        return TransitionEvent(
            proposition_id=f"{run_tag}-proposition",
            prior_state="provisional",
            new_state="accepted",
            confidence=0.73,
            support_score=0.81,
            contradiction_score=0.08,
            freshness=0.91,
            evidence_ids=(f"{run_tag}-obs-1",),
            rule_id="transition.accepted.sustained_support",
            timestamp_utc="2026-03-05T00:00:00Z",
        )

    def _build_consolidation_event(
        self,
        *,
        family: LongHorizonTaskFamily,
        system: str,
        seed: int,
    ) -> ConsolidationEvent:
        run_tag = f"{family.family_id}-{system}-{seed}"
        return ConsolidationEvent(
            session_id=f"{run_tag}-session",
            task_id=f"{run_tag}-task",
            promoted_proposition_ids=(f"{run_tag}-proposition",),
            archived_proposition_ids=(),
            discarded_proposition_ids=(),
            carryover_retained_ids=(),
            overflow_reason_code=None,
            rule_id="consolidation.task_boundary",
            timestamp_utc="2026-03-05T00:01:00Z",
        )

    def _ensure_required_artifacts(self, run_dir: Path) -> None:
        actual_files = {path.name for path in run_dir.iterdir()}
        missing = tuple(name for name in self._required_artifact_files if name not in actual_files)
        if missing:
            raise LongHorizonContractError(
                f"Artifact directory {run_dir} is missing required files: {missing}."
            )


def evaluate_stage4_interpretable_benefit(
    *,
    task_families: tuple[LongHorizonTaskFamily, ...],
    governance_metric_name: str = "false_promotion_rate",
    continuity_metric_name: str = "context_retention_success_rate",
) -> LongHorizonStudyResult:
    """Compute Stage 4 paired governance and continuity improvement by task family."""

    if not task_families:
        raise LongHorizonContractError("Stage 4 requires at least one task family.")

    outcomes: list[LongHorizonFamilyOutcome] = []
    for family in task_families:
        governance_improvement = round(
            family.governance_baseline - family.governance_governed, 6
        )
        continuity_improvement = round(
            family.continuity_governed - family.continuity_baseline, 6
        )
        governance_improved = governance_improvement > 0
        continuity_improved = continuity_improvement > 0
        paired_improvement = governance_improved and continuity_improved

        outcomes.append(
            LongHorizonFamilyOutcome(
                family_id=family.family_id,
                governance_metric_name=governance_metric_name,
                continuity_metric_name=continuity_metric_name,
                governance_baseline=family.governance_baseline,
                governance_governed=family.governance_governed,
                continuity_baseline=family.continuity_baseline,
                continuity_governed=family.continuity_governed,
                governance_improvement=governance_improvement,
                continuity_improvement=continuity_improvement,
                governance_improved=governance_improved,
                continuity_improved=continuity_improved,
                paired_improvement=paired_improvement,
            )
        )

    paired_families = tuple(
        outcome.family_id for outcome in outcomes if outcome.paired_improvement
    )
    return LongHorizonStudyResult(
        outcomes=tuple(outcomes),
        task_families_with_paired_improvement=paired_families,
        interpretable_benefit_passed=bool(paired_families),
    )


def _build_family_metrics(
    *,
    family: LongHorizonTaskFamily,
    system: str,
    seeds: tuple[int, ...],
) -> AggregateMetrics:
    if system == RAW_LOG_BASELINE_SYSTEM:
        governance_value = family.governance_baseline
        continuity_value = family.continuity_baseline
    else:
        governance_value = family.governance_governed
        continuity_value = family.continuity_governed

    return AggregateMetrics(
        system=system,
        seed_set=seeds,
        policy_metrics={"false_promotion_rate": governance_value},
        identity_metrics={},
        memory_health_metrics={},
        task_metrics={"context_retention_success_rate": continuity_value},
    )

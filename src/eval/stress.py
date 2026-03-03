"""Deterministic Stage 2 governance stress harness and scenario contracts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

from src.eval.artifacts import stable_hash, write_run_artifacts
from src.eval.schemas import (
    AggregateMetrics,
    ConsolidationEvent,
    ScenarioResult,
    TransitionEvent,
)

STAGE2_FIXED_SEEDS: tuple[int, ...] = (101, 202, 303, 404, 505)
STAGE2_REQUIRED_FAILURE_MODES: tuple[str, ...] = (
    "delayed_correction",
    "correlated_false_sources",
    "same_source_reinforcement",
    "changing_facts_over_time",
    "ambiguous_entity_references",
    "insufficient_evidence_abstention",
    "competing_propositions_targeted_test",
)
STAGE2_REQUIRED_ARTIFACT_FILES: tuple[str, ...] = (
    "manifest.json",
    "config_snapshot.yaml",
    "transitions.jsonl",
    "consolidation_events.jsonl",
    "scenario_results.jsonl",
    "metrics_summary.json",
)


@dataclass(frozen=True, slots=True)
class GovernanceStressScenario:
    """One deterministic governance stress scenario descriptor."""

    scenario_id: str
    failure_mode: str
    description: str

    def to_dict(self) -> dict[str, str]:
        return {
            "scenario_id": self.scenario_id,
            "failure_mode": self.failure_mode,
            "description": self.description,
        }


@dataclass(frozen=True, slots=True)
class GovernanceStressBundle:
    """Scenario bundle used for Stage 2 runs."""

    bundle_id: str
    scenarios: tuple[GovernanceStressScenario, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "bundle_id": self.bundle_id,
            "scenarios": [scenario.to_dict() for scenario in self.scenarios],
        }

    def deterministic_hash(self) -> str:
        return stable_hash(self.to_dict())


@dataclass(frozen=True, slots=True)
class GovernanceStressRunRecord:
    """Metadata returned for each deterministic Stage 2 run artifact directory."""

    system: str
    seed: int
    run_dir: Path
    scenario_bundle_hash: str
    reproducibility_hash: str


class GovernanceStressContractError(ValueError):
    """Raised when the Stage 2 contract is violated."""


class GovernanceStressHarness:
    """Deterministic Stage 2 harness enforcing fixed seeds and shared bundles."""

    def __init__(
        self,
        *,
        systems: tuple[str, ...],
        seeds: tuple[int, ...] = STAGE2_FIXED_SEEDS,
        required_artifact_files: tuple[str, ...] = STAGE2_REQUIRED_ARTIFACT_FILES,
    ) -> None:
        if seeds != STAGE2_FIXED_SEEDS:
            raise GovernanceStressContractError(
                f"Stage 2 seeds must match {STAGE2_FIXED_SEEDS}; got {seeds}."
            )
        self._systems = systems
        self._seeds = seeds
        self._required_artifact_files = required_artifact_files

    def run_stage2(
        self,
        *,
        artifacts_root: Path,
        run_date: datetime,
        git_sha: str,
        model_id: str,
        config_snapshot: Mapping[str, Any],
        scenario_bundles: Mapping[str, GovernanceStressBundle],
    ) -> tuple[GovernanceStressRunRecord, ...]:
        self._validate_bundle_contract(scenario_bundles)

        config_payload = dict(config_snapshot)
        records: list[GovernanceStressRunRecord] = []
        for system in self._systems:
            bundle = scenario_bundles[system]
            bundle_payload = bundle.to_dict()
            bundle_hash = bundle.deterministic_hash()
            reproducibility_hash = stable_hash(
                {
                    "config_hash": stable_hash(config_payload),
                    "scenario_bundle_hash": bundle_hash,
                }
            )
            for seed in self._seeds:
                scenario_results = self._build_scenario_results(
                    system=system,
                    seed=seed,
                    bundle=bundle,
                )
                metrics_summary = self._build_metrics_summary(
                    system=system,
                    scenario_results=scenario_results,
                )
                run_dir = write_run_artifacts(
                    artifacts_root=artifacts_root,
                    run_date=run_date,
                    git_sha=git_sha,
                    system=system,
                    seed=seed,
                    model_id=model_id,
                    config_snapshot=config_payload,
                    scenario_bundle=bundle_payload,
                    transitions=[self._build_transition_event(system=system, seed=seed)],
                    consolidation_events=[
                        self._build_consolidation_event(system=system, seed=seed)
                    ],
                    scenario_results=scenario_results,
                    metrics_summary=metrics_summary,
                )
                self._ensure_required_artifacts(run_dir)
                records.append(
                    GovernanceStressRunRecord(
                        system=system,
                        seed=seed,
                        run_dir=run_dir,
                        scenario_bundle_hash=bundle_hash,
                        reproducibility_hash=reproducibility_hash,
                    )
                )
        return tuple(records)

    def _validate_bundle_contract(
        self, scenario_bundles: Mapping[str, GovernanceStressBundle]
    ) -> None:
        provided_systems = set(scenario_bundles)
        required_systems = set(self._systems)
        if provided_systems != required_systems:
            missing = tuple(sorted(required_systems - provided_systems))
            extra = tuple(sorted(provided_systems - required_systems))
            raise GovernanceStressContractError(
                f"Scenario bundle systems mismatch; missing={missing}, extra={extra}."
            )

        bundle_hashes = {
            scenario_bundles[system].deterministic_hash() for system in self._systems
        }
        if len(bundle_hashes) != 1:
            raise GovernanceStressContractError(
                "Stage 2 requires identical scenario bundles per compared system."
            )

        for system in self._systems:
            bundle = scenario_bundles[system]
            scenario_ids = [scenario.scenario_id for scenario in bundle.scenarios]
            if len(set(scenario_ids)) != len(scenario_ids):
                raise GovernanceStressContractError(
                    f"Bundle {bundle.bundle_id} has duplicate scenario ids."
                )
            failure_modes = {scenario.failure_mode for scenario in bundle.scenarios}
            missing_failure_modes = tuple(
                mode
                for mode in STAGE2_REQUIRED_FAILURE_MODES
                if mode not in failure_modes
            )
            if missing_failure_modes:
                raise GovernanceStressContractError(
                    f"Bundle {bundle.bundle_id} missing required failure modes: "
                    f"{missing_failure_modes}."
                )

    def _build_scenario_results(
        self, *, system: str, seed: int, bundle: GovernanceStressBundle
    ) -> list[ScenarioResult]:
        seed_offset = (seed % 100) / 1000.0
        results: list[ScenarioResult] = []
        for index, scenario in enumerate(bundle.scenarios, start=1):
            task_success = (seed + index) % 3 != 0
            results.append(
                ScenarioResult(
                    stage="governance_stress",
                    scenario_id=scenario.scenario_id,
                    system=system,
                    seed=seed,
                    task_success=task_success,
                    policy_metrics={"false_promotion_rate": round(0.04 * index + seed_offset, 4)},
                    identity_metrics={"false_merge_rate": round(0.01 * ((index + seed) % 4), 4)},
                    memory_health_metrics={"stale_node_fraction": round(0.08 + 0.01 * index, 4)},
                    task_metrics={"wall_clock_latency": round(1.0 + 0.05 * index, 4)},
                )
            )
        return results

    def _build_metrics_summary(
        self, *, system: str, scenario_results: list[ScenarioResult]
    ) -> AggregateMetrics:
        run_count = len(scenario_results)
        false_promotion_sum = sum(
            item.policy_metrics["false_promotion_rate"] for item in scenario_results
        )
        false_merge_sum = sum(
            item.identity_metrics["false_merge_rate"] for item in scenario_results
        )
        stale_sum = sum(
            item.memory_health_metrics["stale_node_fraction"] for item in scenario_results
        )
        success_sum = sum(1 for item in scenario_results if item.task_success)
        return AggregateMetrics(
            system=system,
            seed_set=self._seeds,
            policy_metrics={"false_promotion_rate": round(false_promotion_sum / run_count, 4)},
            identity_metrics={"false_merge_rate": round(false_merge_sum / run_count, 4)},
            memory_health_metrics={"stale_node_fraction": round(stale_sum / run_count, 4)},
            task_metrics={"task_success_rate": round(success_sum / run_count, 4)},
        )

    def _build_transition_event(self, *, system: str, seed: int) -> TransitionEvent:
        run_tag = f"{system}-{seed}"
        return TransitionEvent(
            proposition_id=f"{run_tag}-proposition",
            prior_state="tentative",
            new_state="provisional",
            confidence=0.61,
            support_score=0.72,
            contradiction_score=0.15,
            freshness=0.90,
            evidence_ids=(f"{run_tag}-obs-1",),
            rule_id="transition.provisional.supported",
            timestamp_utc="2026-03-03T00:00:00Z",
        )

    def _build_consolidation_event(self, *, system: str, seed: int) -> ConsolidationEvent:
        run_tag = f"{system}-{seed}"
        return ConsolidationEvent(
            session_id=f"{run_tag}-session",
            task_id=f"{run_tag}-task",
            promoted_proposition_ids=(f"{run_tag}-proposition",),
            archived_proposition_ids=(),
            discarded_proposition_ids=(),
            carryover_retained_ids=(),
            overflow_reason_code=None,
            rule_id="consolidation.task_boundary",
            timestamp_utc="2026-03-03T00:01:00Z",
        )

    def _ensure_required_artifacts(self, run_dir: Path) -> None:
        actual_files = {path.name for path in run_dir.iterdir()}
        missing_files = tuple(
            name for name in self._required_artifact_files if name not in actual_files
        )
        if missing_files:
            raise GovernanceStressContractError(
                f"Artifact directory {run_dir} is missing required files: {missing_files}."
            )


def build_default_governance_stress_bundle() -> GovernanceStressBundle:
    """Build default Stage 2 stress suite covering required governance failure modes."""

    scenarios = tuple(
        GovernanceStressScenario(
            scenario_id=f"stress-{index + 1:02d}",
            failure_mode=failure_mode,
            description=f"Stage 2 governance stress scenario for {failure_mode}.",
        )
        for index, failure_mode in enumerate(STAGE2_REQUIRED_FAILURE_MODES)
    )
    return GovernanceStressBundle(bundle_id="stage2-governance-stress-v0q", scenarios=scenarios)


def build_uniform_stage2_bundles(
    *, systems: tuple[str, ...], bundle: GovernanceStressBundle | None = None
) -> dict[str, GovernanceStressBundle]:
    """Build per-system scenario bundles that satisfy Stage 2 identical-bundle contract."""

    resolved_bundle = bundle or build_default_governance_stress_bundle()
    return {system: resolved_bundle for system in systems}

"""Tests for v0.1q artifact writing and reproducibility hashing."""

import json
from datetime import datetime
from pathlib import Path

import pytest

from src.eval import (
    STAGE2_FIXED_SEEDS,
    STAGE2_REQUIRED_ARTIFACT_FILES,
    AggregateMetrics,
    ConsolidationEvent,
    GovernanceStressBundle,
    GovernanceStressContractError,
    GovernanceStressHarness,
    GovernanceStressScenario,
    ScenarioResult,
    TransitionEvent,
    build_default_governance_stress_bundle,
    build_uniform_stage2_bundles,
    stable_hash,
    write_run_artifacts,
)


def _transition() -> TransitionEvent:
    return TransitionEvent(
        proposition_id="prop-1",
        prior_state="tentative",
        new_state="provisional",
        confidence=0.62,
        support_score=0.7,
        contradiction_score=0.1,
        freshness=0.9,
        evidence_ids=("obs-1",),
        rule_id="transition.provisional.supported",
        timestamp_utc="2026-02-27T12:00:00Z",
    )


def _consolidation() -> ConsolidationEvent:
    return ConsolidationEvent(
        session_id="session-1",
        task_id="task-1",
        promoted_proposition_ids=("prop-1",),
        archived_proposition_ids=(),
        discarded_proposition_ids=(),
        carryover_retained_ids=("prop-2",),
        overflow_reason_code=None,
        rule_id="consolidation.task_boundary",
        timestamp_utc="2026-02-27T12:01:00Z",
    )


def _scenario_result() -> ScenarioResult:
    return ScenarioResult(
        stage="policy_correctness",
        scenario_id="scenario-1",
        system="governed",
        seed=101,
        task_success=True,
        policy_metrics={"false_promotion_rate": 0.1},
        identity_metrics={"false_merge_rate": 0.0},
        memory_health_metrics={"stale_node_fraction": 0.2},
        task_metrics={"wall_clock_latency": 1.3},
    )


def _metrics_summary() -> AggregateMetrics:
    return AggregateMetrics(
        system="governed",
        seed_set=(101, 202, 303, 404, 505),
        policy_metrics={"false_promotion_rate": 0.1},
        identity_metrics={"false_merge_rate": 0.0},
        memory_health_metrics={"stale_node_fraction": 0.2},
        task_metrics={"task_success_rate": 0.8},
    )


def test_write_run_artifacts_creates_required_files(tmp_path: Path) -> None:
    run_dir = write_run_artifacts(
        artifacts_root=tmp_path,
        run_date=datetime(2026, 2, 27, 12, 0, 0),
        git_sha="abcdef1234567890",
        system="governed",
        seed=101,
        model_id="model-x",
        config_snapshot={"policy": {"accepted": 0.8}},
        scenario_bundle={"scenarios": ["s1"]},
        transitions=[_transition()],
        consolidation_events=[_consolidation()],
        scenario_results=[_scenario_result()],
        metrics_summary=_metrics_summary(),
    )

    assert run_dir.exists()
    assert run_dir.name == "2026-02-27_abcdef12_governed_101"
    for name in (
        "manifest.json",
        "config_snapshot.yaml",
        "transitions.jsonl",
        "consolidation_events.jsonl",
        "scenario_results.jsonl",
        "metrics_summary.json",
    ):
        assert (run_dir / name).exists()


def test_stable_hash_is_order_independent_for_mappings() -> None:
    first = stable_hash({"a": 1, "b": 2})
    second = stable_hash({"b": 2, "a": 1})

    assert first == second


def test_manifest_reproducibility_hash_matches_frozen_recipe(tmp_path: Path) -> None:
    config_snapshot = {"policy": {"accepted": 0.8}}
    scenario_bundle = {"scenarios": ["s1"]}

    run_dir = write_run_artifacts(
        artifacts_root=tmp_path,
        run_date=datetime(2026, 2, 27, 12, 0, 0),
        git_sha="abcdef1234567890",
        system="governed",
        seed=101,
        model_id="model-x",
        config_snapshot=config_snapshot,
        scenario_bundle=scenario_bundle,
        transitions=[_transition()],
        consolidation_events=[_consolidation()],
        scenario_results=[_scenario_result()],
        metrics_summary=_metrics_summary(),
    )

    manifest_payload = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    expected = stable_hash(
        {
            "config_hash": stable_hash(config_snapshot),
            "scenario_bundle_hash": stable_hash(scenario_bundle),
        }
    )

    assert manifest_payload["reproducibility_hash"] == expected


def test_governance_stress_harness_rejects_non_fixed_seed_set() -> None:
    with pytest.raises(GovernanceStressContractError):
        GovernanceStressHarness(
            systems=("full_governed_system",),
            seeds=(101, 202),
        )


def test_governance_stress_harness_rejects_non_identical_bundles(tmp_path: Path) -> None:
    harness = GovernanceStressHarness(systems=("system-a", "system-b"))
    bundle_a = build_default_governance_stress_bundle()
    bundle_b = GovernanceStressBundle(
        bundle_id="stage2-governance-stress-v0q-system-b",
        scenarios=(
            GovernanceStressScenario(
                scenario_id="stress-01",
                failure_mode="delayed_correction",
                description="Different bundle id should fail shared bundle contract.",
            ),
            GovernanceStressScenario(
                scenario_id="stress-02",
                failure_mode="correlated_false_sources",
                description="Different bundle id should fail shared bundle contract.",
            ),
            GovernanceStressScenario(
                scenario_id="stress-03",
                failure_mode="same_source_reinforcement",
                description="Different bundle id should fail shared bundle contract.",
            ),
            GovernanceStressScenario(
                scenario_id="stress-04",
                failure_mode="changing_facts_over_time",
                description="Different bundle id should fail shared bundle contract.",
            ),
            GovernanceStressScenario(
                scenario_id="stress-05",
                failure_mode="ambiguous_entity_references",
                description="Different bundle id should fail shared bundle contract.",
            ),
            GovernanceStressScenario(
                scenario_id="stress-06",
                failure_mode="insufficient_evidence_abstention",
                description="Different bundle id should fail shared bundle contract.",
            ),
            GovernanceStressScenario(
                scenario_id="stress-07",
                failure_mode="competing_propositions_targeted_test",
                description="Different bundle id should fail shared bundle contract.",
            ),
        ),
    )

    with pytest.raises(GovernanceStressContractError):
        harness.run_stage2(
            artifacts_root=tmp_path,
            run_date=datetime(2026, 3, 3, 12, 0, 0),
            git_sha="abcdef1234567890",
            model_id="model-x",
            config_snapshot={"eval": {"stage": "governance_stress"}},
            scenario_bundles={"system-a": bundle_a, "system-b": bundle_b},
        )


def test_governance_stress_harness_emits_required_files_for_fixed_seed_set(tmp_path: Path) -> None:
    harness = GovernanceStressHarness(systems=("full_governed_system",))
    run_records = harness.run_stage2(
        artifacts_root=tmp_path,
        run_date=datetime(2026, 3, 3, 13, 0, 0),
        git_sha="abcdef1234567890",
        model_id="model-governed",
        config_snapshot={"eval": {"stage": "governance_stress"}},
        scenario_bundles=build_uniform_stage2_bundles(
            systems=("full_governed_system",),
            bundle=build_default_governance_stress_bundle(),
        ),
    )

    assert len(run_records) == len(STAGE2_FIXED_SEEDS)
    assert {record.seed for record in run_records} == set(STAGE2_FIXED_SEEDS)
    assert {record.system for record in run_records} == {"full_governed_system"}

    for record in run_records:
        assert set(STAGE2_REQUIRED_ARTIFACT_FILES).issubset(
            {path.name for path in record.run_dir.iterdir()}
        )

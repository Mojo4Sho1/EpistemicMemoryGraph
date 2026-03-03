"""Smoke test for minimal evaluation artifact contract behavior."""

import json
from datetime import datetime
from pathlib import Path

import pytest

from src.eval import (
    STAGE2_FIXED_SEEDS,
    STAGE2_REQUIRED_ARTIFACT_FILES,
    AggregateMetrics,
    ConsolidationEvent,
    GovernanceStressHarness,
    ScenarioResult,
    TransitionEvent,
    build_default_governance_stress_bundle,
    build_uniform_stage2_bundles,
    stable_hash,
    write_run_artifacts,
)

pytestmark = pytest.mark.smoke


def _transition_event() -> TransitionEvent:
    return TransitionEvent(
        proposition_id="prop-smoke-1",
        prior_state="tentative",
        new_state="provisional",
        confidence=0.60,
        support_score=0.70,
        contradiction_score=0.10,
        freshness=0.95,
        evidence_ids=("obs-smoke-1",),
        rule_id="transition.provisional.supported",
        timestamp_utc="2026-02-28T11:00:00Z",
    )


def _consolidation_event() -> ConsolidationEvent:
    return ConsolidationEvent(
        session_id="smoke-session",
        task_id="smoke-task",
        promoted_proposition_ids=("prop-smoke-1",),
        archived_proposition_ids=(),
        discarded_proposition_ids=(),
        carryover_retained_ids=(),
        overflow_reason_code=None,
        rule_id="consolidation.task_boundary",
        timestamp_utc="2026-02-28T11:01:00Z",
    )


def _scenario_result() -> ScenarioResult:
    return ScenarioResult(
        stage="policy_correctness",
        scenario_id="smoke-scenario-1",
        system="governed",
        seed=101,
        task_success=True,
        policy_metrics={"false_promotion_rate": 0.10},
        identity_metrics={"false_merge_rate": 0.00},
        memory_health_metrics={"stale_node_fraction": 0.20},
        task_metrics={"wall_clock_latency": 1.2},
    )


def _aggregate_metrics() -> AggregateMetrics:
    return AggregateMetrics(
        system="governed",
        seed_set=(101, 202, 303, 404, 505),
        policy_metrics={"false_promotion_rate": 0.10},
        identity_metrics={"false_merge_rate": 0.00},
        memory_health_metrics={"stale_node_fraction": 0.20},
        task_metrics={"task_success_rate": 0.88},
    )


def test_eval_artifact_smoke_contract(tmp_path: Path) -> None:
    config_snapshot = {"policy": {"accepted": 0.80}}
    scenario_bundle = {"bundle_id": "smoke-bundle", "scenarios": ["smoke-scenario-1"]}

    run_dir = write_run_artifacts(
        artifacts_root=tmp_path,
        run_date=datetime(2026, 2, 28, 11, 0, 0),
        git_sha="12345678abcdef90",
        system="governed",
        seed=101,
        model_id="model-smoke",
        config_snapshot=config_snapshot,
        scenario_bundle=scenario_bundle,
        transitions=[_transition_event()],
        consolidation_events=[_consolidation_event()],
        scenario_results=[_scenario_result()],
        metrics_summary=_aggregate_metrics(),
    )

    assert run_dir.name == "2026-02-28_12345678_governed_101"
    expected_files = {
        "manifest.json",
        "config_snapshot.yaml",
        "transitions.jsonl",
        "consolidation_events.jsonl",
        "scenario_results.jsonl",
        "metrics_summary.json",
    }
    assert {path.name for path in run_dir.iterdir()} == expected_files

    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["timestamp_utc"] == "2026-02-28T11:00:00Z"
    assert manifest["config_hash"] == stable_hash(config_snapshot)
    assert manifest["scenario_bundle_hash"] == stable_hash(scenario_bundle)
    assert manifest["reproducibility_hash"] == stable_hash(
        {
            "config_hash": stable_hash(config_snapshot),
            "scenario_bundle_hash": stable_hash(scenario_bundle),
        }
    )

    transitions_rows = (run_dir / "transitions.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(transitions_rows) == 1


def test_stage2_governance_stress_smoke_contract(tmp_path: Path) -> None:
    harness = GovernanceStressHarness(systems=("full_governed_system",))
    run_records = harness.run_stage2(
        artifacts_root=tmp_path,
        run_date=datetime(2026, 3, 3, 14, 0, 0),
        git_sha="abcdef1234567890",
        model_id="model-smoke",
        config_snapshot={"eval": {"stage": "governance_stress"}},
        scenario_bundles=build_uniform_stage2_bundles(
            systems=("full_governed_system",),
            bundle=build_default_governance_stress_bundle(),
        ),
    )

    assert len(run_records) == len(STAGE2_FIXED_SEEDS)
    assert {record.seed for record in run_records} == set(STAGE2_FIXED_SEEDS)
    for record in run_records:
        assert set(STAGE2_REQUIRED_ARTIFACT_FILES).issubset(
            {path.name for path in record.run_dir.iterdir()}
        )

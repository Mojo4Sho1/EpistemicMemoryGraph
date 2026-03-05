"""Tests for v0.1q artifact writing and reproducibility hashing."""

import json
from datetime import datetime
from pathlib import Path

import pytest

from src.eval import (
    LONG_HORIZON_REQUIRED_ARTIFACT_FILES,
    STAGE2_FIXED_SEEDS,
    STAGE2_REQUIRED_ARTIFACT_FILES,
    AggregateMetrics,
    BaselineFairnessError,
    BaselineRunSpec,
    ConsolidationEvent,
    GovernanceStressBundle,
    GovernanceStressContractError,
    GovernanceStressHarness,
    GovernanceStressScenario,
    LongHorizonContractError,
    LongHorizonStudyHarness,
    LongHorizonTaskFamily,
    ScenarioResult,
    TransitionEvent,
    build_default_governance_stress_bundle,
    build_uniform_stage2_bundles,
    evaluate_stage4_interpretable_benefit,
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


def _stage4_spec(*, token_budget: int = 4096) -> BaselineRunSpec:
    return BaselineRunSpec(
        model_snapshot="model-locked",
        prompt_template_family="default-v1",
        tool_availability=("record_observation", "request_consolidation"),
        token_budget=token_budget,
        wall_clock_timeout_seconds=120,
        seed_set=(101, 202, 303, 404, 505),
    )


def test_long_horizon_harness_emits_deterministic_artifacts_for_required_systems(
    tmp_path: Path,
) -> None:
    harness = LongHorizonStudyHarness()
    run_specs = {
        "raw_text_log_retrieval": _stage4_spec(),
        "full_governed_system": _stage4_spec(),
    }
    task_families = (
        LongHorizonTaskFamily(
            family_id="policy-debug",
            description="Repeated policy-sensitive debugging steps.",
            governance_baseline=0.34,
            governance_governed=0.24,
            continuity_baseline=0.62,
            continuity_governed=0.76,
        ),
    )
    seeds = (101, 202)

    first = harness.run_stage4(
        artifacts_root=tmp_path / "first",
        run_date=datetime(2026, 3, 5, 9, 0, 0),
        git_sha="abcdef1234567890",
        model_id="model-governed",
        seeds=seeds,
        run_specs=run_specs,
        config_snapshot={"eval": {"stage": "long_horizon"}},
        task_families=task_families,
    )
    second = harness.run_stage4(
        artifacts_root=tmp_path / "second",
        run_date=datetime(2026, 3, 5, 9, 0, 0),
        git_sha="abcdef1234567890",
        model_id="model-governed",
        seeds=seeds,
        run_specs=run_specs,
        config_snapshot={"eval": {"stage": "long_horizon"}},
        task_families=task_families,
    )

    assert len(first) == 4
    assert [(item.family_id, item.system, item.seed) for item in first] == [
        ("policy-debug", "raw_text_log_retrieval", 101),
        ("policy-debug", "raw_text_log_retrieval", 202),
        ("policy-debug", "full_governed_system", 101),
        ("policy-debug", "full_governed_system", 202),
    ]
    assert [(item.family_id, item.system, item.seed) for item in first] == [
        (item.family_id, item.system, item.seed) for item in second
    ]

    for record in first:
        assert set(LONG_HORIZON_REQUIRED_ARTIFACT_FILES).issubset(
            {path.name for path in record.run_dir.iterdir()}
        )


def test_long_horizon_harness_requires_stage4_fairness_lock(tmp_path: Path) -> None:
    harness = LongHorizonStudyHarness()
    run_specs = {
        "raw_text_log_retrieval": _stage4_spec(token_budget=2048),
        "full_governed_system": _stage4_spec(token_budget=4096),
    }
    task_families = (
        LongHorizonTaskFamily(
            family_id="policy-debug",
            description="Repeated policy-sensitive debugging steps.",
            governance_baseline=0.34,
            governance_governed=0.24,
            continuity_baseline=0.62,
            continuity_governed=0.76,
        ),
    )

    with pytest.raises(LongHorizonContractError):
        harness.run_stage4(
            artifacts_root=tmp_path,
            run_date=datetime(2026, 3, 5, 9, 0, 0),
            git_sha="abcdef1234567890",
            model_id="model-governed",
            seeds=(101,),
            run_specs={"raw_text_log_retrieval": _stage4_spec()},
            config_snapshot={"eval": {"stage": "long_horizon"}},
            task_families=task_families,
        )

    with pytest.raises(BaselineFairnessError) as exc_info:
        harness.run_stage4(
            artifacts_root=tmp_path,
            run_date=datetime(2026, 3, 5, 9, 0, 0),
            git_sha="abcdef1234567890",
            model_id="model-governed",
            seeds=(101,),
            run_specs=run_specs,
            config_snapshot={"eval": {"stage": "long_horizon"}},
            task_families=task_families,
        )
    assert "Fairness preflight failed" in str(exc_info.value)


def test_stage4_interpretable_benefit_passes_when_one_family_has_paired_improvement() -> None:
    result = evaluate_stage4_interpretable_benefit(
        task_families=(
            LongHorizonTaskFamily(
                family_id="policy-debug",
                description="Repeated policy-sensitive debugging steps.",
                governance_baseline=0.34,
                governance_governed=0.24,
                continuity_baseline=0.62,
                continuity_governed=0.76,
            ),
            LongHorizonTaskFamily(
                family_id="identity-reconciliation",
                description="Entity resolution over long dialogue turns.",
                governance_baseline=0.18,
                governance_governed=0.17,
                continuity_baseline=0.70,
                continuity_governed=0.69,
            ),
        )
    )

    assert result.interpretable_benefit_passed is True
    assert result.task_families_with_paired_improvement == ("policy-debug",)


def test_stage4_interpretable_benefit_fails_when_no_family_has_paired_improvement() -> None:
    result = evaluate_stage4_interpretable_benefit(
        task_families=(
            LongHorizonTaskFamily(
                family_id="policy-debug",
                description="Repeated policy-sensitive debugging steps.",
                governance_baseline=0.20,
                governance_governed=0.21,
                continuity_baseline=0.62,
                continuity_governed=0.76,
            ),
            LongHorizonTaskFamily(
                family_id="identity-reconciliation",
                description="Entity resolution over long dialogue turns.",
                governance_baseline=0.18,
                governance_governed=0.17,
                continuity_baseline=0.70,
                continuity_governed=0.69,
            ),
        )
    )

    assert result.interpretable_benefit_passed is False
    assert result.task_families_with_paired_improvement == ()

"""Tests for Phase 2 small/edge uplift runner, stats, and reporting artifacts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest

from src.eval import (
    PHASE2_DECISION_GATE_OPEN,
    PHASE2_ID,
    PHASE2_STAGE_LOCAL_SCREENING,
    FindingsSummary,
    LongHorizonTaskFamily,
    Phase2ContractError,
    Phase2ModelOutcome,
    Phase2PolicyAblationSpec,
    Phase2SmallEdgeRunner,
    Phase2SmallModelSpec,
    Phase2StatisticalGate,
    StatisticalResult,
    bootstrap_ci,
    build_phase2_local_small_model_panel,
    evaluate_paired_metric,
    paired_permutation_pvalue,
)


def test_bootstrap_ci_is_deterministic_for_fixed_seed() -> None:
    values = (0.10, 0.15, 0.08, 0.12)

    first = bootstrap_ci(values, seed=11)
    second = bootstrap_ci(values, seed=11)

    assert first == second


def test_paired_permutation_detects_large_difference() -> None:
    baseline = (0.40, 0.42, 0.41, 0.39, 0.43, 0.44, 0.38, 0.41)
    governed = (0.20, 0.18, 0.19, 0.21, 0.22, 0.23, 0.17, 0.20)

    p_value = paired_permutation_pvalue(
        baseline_values=baseline,
        governed_values=governed,
        lower_is_better=True,
        seed=7,
    )

    assert p_value < 0.1


def test_evaluate_paired_metric_requires_all_statistical_gates() -> None:
    result = evaluate_paired_metric(
        metric_name="false_promotion_rate",
        baseline_values=(0.40, 0.41, 0.39, 0.42, 0.43, 0.44, 0.38, 0.41),
        governed_values=(0.22, 0.24, 0.21, 0.23, 0.25, 0.24, 0.20, 0.22),
        lower_is_better=True,
        alpha=0.05,
        min_effect_size=0.2,
        seed=3,
    )

    assert result.metric_name == "false_promotion_rate"
    assert result.delta > 0
    assert result.ci_low > 0
    assert result.passed is True


def test_findings_summary_to_dict_serializes_nested_results() -> None:
    summary = FindingsSummary(
        phase_id=PHASE2_ID,
        stage_id="P2-S3",
        model_id="tiny-1b",
        task_families=("policy-debug",),
        key_results=(
            StatisticalResult(
                metric_name="false_promotion_rate",
                delta=0.10,
                ci_low=0.08,
                ci_high=0.12,
                p_value=0.01,
                effect_size=1.2,
                passed=True,
            ),
        ),
        caveats=("deterministic harness",),
        interpretation="signal present",
        decision_gate_status=PHASE2_DECISION_GATE_OPEN,
    )

    payload = summary.to_dict()

    assert payload["phase_id"] == PHASE2_ID
    assert payload["key_results"][0]["metric_name"] == "false_promotion_rate"


def _task_families() -> tuple[LongHorizonTaskFamily, ...]:
    return (
        LongHorizonTaskFamily(
            family_id="policy-debug",
            description="Repeated policy-sensitive debugging steps.",
            governance_baseline=0.34,
            governance_governed=0.24,
            continuity_baseline=0.62,
            continuity_governed=0.76,
        ),
        LongHorizonTaskFamily(
            family_id="edge-planning",
            description="Small-model multi-turn planning revisions.",
            governance_baseline=0.30,
            governance_governed=0.22,
            continuity_baseline=0.58,
            continuity_governed=0.71,
        ),
    )


def _model_panel() -> tuple[Phase2SmallModelSpec, ...]:
    return (
        Phase2SmallModelSpec(
            model_id="tiny-1b",
            parameter_scale="~1B",
            prompt_template_family="phase2-default-v1",
            tool_availability=("record_observation", "request_consolidation"),
            token_budget=2048,
            wall_clock_timeout_seconds=120,
            seed_set=(101,),
            provider_org="Tiny Labs",
            origin_country="United States",
            compliance_class="allowed_university",
        ),
    )


def test_phase2_runner_emits_findings_summary_artifacts(tmp_path: Path) -> None:
    runner = Phase2SmallEdgeRunner(stage_id="P2-S3")

    outcomes = runner.run_phase2(
        artifacts_root=tmp_path,
        run_date=datetime(2026, 3, 6, 10, 0, 0),
        git_sha="abcdef1234567890",
        model_panel=_model_panel(),
        task_families=_task_families(),
        statistical_gate=Phase2StatisticalGate(
            alpha=0.05,
            confidence_level=0.95,
            min_effect_size=0.1,
            bootstrap_resamples=500,
            permutation_resamples=2000,
        ),
        decision_gate_status=PHASE2_DECISION_GATE_OPEN,
    )

    assert len(outcomes) == 1
    outcome = outcomes[0]
    assert outcome.bundle_dir.exists()
    assert outcome.findings_md_path.exists()
    assert outcome.findings_json_path.exists()

    md_text = outcome.findings_md_path.read_text(encoding="utf-8")
    assert "# Findings Summary (P2)" in md_text
    assert "Decision Gate Status" in md_text

    payload = json.loads(outcome.findings_json_path.read_text(encoding="utf-8"))
    assert payload["phase_id"] == "P2"
    assert payload["decision_gate_status"] == "OPEN"


def test_phase2_runner_rejects_invalid_decision_gate_status(tmp_path: Path) -> None:
    runner = Phase2SmallEdgeRunner(stage_id="P2-S3")

    with pytest.raises(Phase2ContractError):
        runner.run_phase2(
            artifacts_root=tmp_path,
            run_date=datetime(2026, 3, 6, 10, 0, 0),
            git_sha="abcdef1234567890",
            model_panel=_model_panel(),
            task_families=_task_families(),
            decision_gate_status="INVALID",
        )


def test_phase2_runner_rejects_disallowed_origin_country(tmp_path: Path) -> None:
    runner = Phase2SmallEdgeRunner(stage_id="P2-S3")
    disallowed_panel = (
        Phase2SmallModelSpec(
            model_id="blocked-model",
            parameter_scale="~1B",
            prompt_template_family="phase2-default-v1",
            tool_availability=("record_observation", "request_consolidation"),
            token_budget=2048,
            wall_clock_timeout_seconds=120,
            seed_set=(101,),
            provider_org="Blocked Lab",
            origin_country="China",
            compliance_class="allowed_university",
        ),
    )

    with pytest.raises(Phase2ContractError):
        runner.run_phase2(
            artifacts_root=tmp_path,
            run_date=datetime(2026, 3, 6, 10, 0, 0),
            git_sha="abcdef1234567890",
            model_panel=disallowed_panel,
            task_families=_task_families(),
        )


def test_phase2_local_panel_completeness_is_exactly_three_models() -> None:
    panel = build_phase2_local_small_model_panel()
    assert len(panel) == 3
    assert {item.model_id for item in panel} == {
        "meta_llama3.2_1b_instruct",
        "google_gemma3_1b",
        "microsoft_phi4_mini",
    }


def test_phase2_local_screening_stage_rejects_incomplete_panel(tmp_path: Path) -> None:
    runner = Phase2SmallEdgeRunner(stage_id=PHASE2_STAGE_LOCAL_SCREENING)

    with pytest.raises(Phase2ContractError):
        runner.run_phase2(
            artifacts_root=tmp_path,
            run_date=datetime(2026, 3, 6, 10, 0, 0),
            git_sha="abcdef1234567890",
            model_panel=_model_panel(),
            task_families=_task_families(),
        )


def test_phase2_runner_writes_compliance_metadata_to_manifest_and_config(tmp_path: Path) -> None:
    runner = Phase2SmallEdgeRunner(stage_id="P2-S3")
    outcomes = runner.run_phase2(
        artifacts_root=tmp_path,
        run_date=datetime(2026, 3, 6, 10, 0, 0),
        git_sha="abcdef1234567890",
        model_panel=_model_panel(),
        task_families=_task_families(),
        decision_gate_status=PHASE2_DECISION_GATE_OPEN,
    )
    manifest_path = next((outcomes[0].bundle_dir).glob("*/manifest.json"))
    config_path = next((outcomes[0].bundle_dir).glob("*/config_snapshot.yaml"))

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["model_metadata"] == {
        "provider_org": "Tiny Labs",
        "origin_country": "United States",
        "compliance_class": "allowed_university",
    }

    config_text = config_path.read_text(encoding="utf-8")
    assert 'provider_org: "Tiny Labs"' in config_text
    assert 'origin_country: "United States"' in config_text
    assert 'compliance_class: "allowed_university"' in config_text


def test_phase2_policy_ablations_indicate_causal_dependence() -> None:
    runner = Phase2SmallEdgeRunner()
    ablations = runner.run_policy_ablations(
        model_outcomes=(
            Phase2ModelOutcome(
                model_id="m1",
                bundle_dir=Path("unused"),
                findings_md_path=Path("unused.md"),
                findings_json_path=Path("unused.json"),
                key_results=(),
                phase2_passed=True,
            ),
        ),
        ablation_spec=Phase2PolicyAblationSpec(),
    )
    assert len(ablations) == 1
    assert ablations[0].baseline_passed is True
    assert ablations[0].ablation_passed is False
    assert ablations[0].causal_gain_retained is True

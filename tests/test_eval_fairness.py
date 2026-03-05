"""Tests for baseline fairness preflight checks."""

import pytest

from src.eval import (
    BASELINE_SYSTEMS,
    GOVERNED_SYSTEM,
    RAW_LOG_BASELINE_SYSTEM,
    AggregateMetrics,
    BaselineAdapterInput,
    BaselineCoverageError,
    BaselineFairnessError,
    BaselineRunResult,
    BaselineRunSpec,
    BaselineRuntime,
    OpenAICompatChatResponse,
    OpenAICompatClientConfig,
    OpenAICompatibleBaselineAdapter,
    Stage3ThresholdConfig,
    build_default_baseline_adapters,
    build_default_baseline_runtime,
    check_baseline_fairness,
    evaluate_stage3_claim_thresholds,
)


def _spec(*, token_budget: int = 4096) -> BaselineRunSpec:
    return BaselineRunSpec(
        model_snapshot="model-locked",
        prompt_template_family="default-v1",
        tool_availability=("record_observation", "request_consolidation"),
        token_budget=token_budget,
        wall_clock_timeout_seconds=120,
        seed_set=(101, 202, 303, 404, 505),
    )


def _metrics(
    *,
    system: str,
    false_promotion_rate: float,
    stale_node_fraction: float,
    false_merge_rate: float,
    task_success_rate: float,
) -> AggregateMetrics:
    return AggregateMetrics(
        system=system,
        seed_set=(101, 202, 303, 404, 505),
        policy_metrics={
            "false_promotion_rate": false_promotion_rate,
            "stale_node_fraction": stale_node_fraction,
            "false_merge_rate": false_merge_rate,
        },
        identity_metrics={"false_merge_rate": false_merge_rate},
        memory_health_metrics={"stale_node_fraction": stale_node_fraction},
        task_metrics={"task_success_rate": task_success_rate},
    )


def test_fairness_passes_when_specs_match() -> None:
    result = check_baseline_fairness(
        {
            "raw_log": _spec(),
            "governed": _spec(),
        }
    )

    assert result.passed is True
    assert result.violations == ()


def test_fairness_fails_when_token_budget_differs() -> None:
    result = check_baseline_fairness(
        {
            "raw_log": _spec(token_budget=2048),
            "governed": _spec(token_budget=4096),
        }
    )

    assert result.passed is False
    assert any("token_budget" in violation for violation in result.violations)


def test_baseline_runtime_runs_all_frozen_systems_deterministically() -> None:
    runtime = build_default_baseline_runtime()
    run_specs = {system: _spec() for system in BASELINE_SYSTEMS}

    first = runtime.run_all(prompt="Summarize the task", seed=101, run_specs=run_specs)
    second = runtime.run_all(prompt="Summarize the task", seed=101, run_specs=run_specs)

    assert tuple(first) == BASELINE_SYSTEMS
    assert first == second
    assert set(first) == set(BASELINE_SYSTEMS)


def test_baseline_runtime_blocks_execution_on_fairness_violation() -> None:
    calls: list[str] = []

    class CountingAdapter:
        def __init__(self, *, system: str) -> None:
            self._system = system

        def execute(self, request: BaselineAdapterInput) -> BaselineRunResult:
            calls.append(self._system)
            return BaselineRunResult(
                system=request.system,
                adapter_label="counting_adapter",
                output_text="ok",
            )

    adapters = {system: CountingAdapter(system=system) for system in BASELINE_SYSTEMS}
    runtime = BaselineRuntime(adapters)

    run_specs = {system: _spec() for system in BASELINE_SYSTEMS}
    run_specs["raw_text_log_retrieval"] = _spec(token_budget=2048)

    with pytest.raises(BaselineFairnessError):
        runtime.run_all(prompt="check parity", seed=101, run_specs=run_specs)

    assert calls == []


def test_baseline_runtime_requires_full_matrix_coverage() -> None:
    adapters = build_default_baseline_adapters()
    adapters.pop("context_window_only")
    runtime = BaselineRuntime(adapters)
    run_specs = {system: _spec() for system in BASELINE_SYSTEMS}

    with pytest.raises(BaselineCoverageError):
        runtime.run_all(prompt="coverage", seed=101, run_specs=run_specs)


def test_stage3_claim_thresholds_pass_with_fairness_and_required_improvements() -> None:
    run_specs = {system: _spec() for system in BASELINE_SYSTEMS}
    aggregate_metrics = {
        system: _metrics(
            system=system,
            false_promotion_rate=0.3,
            stale_node_fraction=0.4,
            false_merge_rate=0.2,
            task_success_rate=0.80,
        )
        for system in BASELINE_SYSTEMS
    }
    aggregate_metrics[RAW_LOG_BASELINE_SYSTEM] = _metrics(
        system=RAW_LOG_BASELINE_SYSTEM,
        false_promotion_rate=0.40,
        stale_node_fraction=0.50,
        false_merge_rate=0.30,
        task_success_rate=0.84,
    )
    aggregate_metrics[GOVERNED_SYSTEM] = _metrics(
        system=GOVERNED_SYSTEM,
        false_promotion_rate=0.34,  # 15% relative improvement
        stale_node_fraction=0.42,  # 16% relative improvement
        false_merge_rate=0.25,  # 16.67% relative improvement
        task_success_rate=0.82,  # 2pp absolute drop
    )

    result = evaluate_stage3_claim_thresholds(
        aggregate_metrics=aggregate_metrics,
        run_specs=run_specs,
        threshold_config=Stage3ThresholdConfig(
            minimum_relative_policy_improvement_percent=10.0,
            minimum_policy_metrics_improved_count=3,
            max_task_success_absolute_drop_percent=3.0,
        ),
    )

    assert result.required_ablations_present is True
    assert result.missing_ablations == ()
    assert result.policy_threshold_passed is True
    assert result.task_success_non_degradation_passed is True
    assert result.claim_thresholds_passed is True
    assert result.policy_metrics_meeting_threshold == (
        "false_promotion_rate",
        "stale_node_fraction",
        "false_merge_rate",
    )
    assert result.task_success_absolute_drop_percent == 2.0


def test_stage3_claim_thresholds_fail_when_only_two_policy_metrics_improve() -> None:
    run_specs = {system: _spec() for system in BASELINE_SYSTEMS}
    aggregate_metrics = {
        system: _metrics(
            system=system,
            false_promotion_rate=0.3,
            stale_node_fraction=0.4,
            false_merge_rate=0.2,
            task_success_rate=0.80,
        )
        for system in BASELINE_SYSTEMS
    }
    aggregate_metrics[RAW_LOG_BASELINE_SYSTEM] = _metrics(
        system=RAW_LOG_BASELINE_SYSTEM,
        false_promotion_rate=0.40,
        stale_node_fraction=0.50,
        false_merge_rate=0.30,
        task_success_rate=0.84,
    )
    aggregate_metrics[GOVERNED_SYSTEM] = _metrics(
        system=GOVERNED_SYSTEM,
        false_promotion_rate=0.34,  # 15% relative improvement
        stale_node_fraction=0.45,  # 10% relative improvement
        false_merge_rate=0.29,  # 3.33% relative improvement (below threshold)
        task_success_rate=0.82,
    )

    result = evaluate_stage3_claim_thresholds(
        aggregate_metrics=aggregate_metrics,
        run_specs=run_specs,
    )

    assert result.policy_threshold_passed is False
    assert result.task_success_non_degradation_passed is True
    assert result.claim_thresholds_passed is False
    assert result.policy_metrics_meeting_threshold == (
        "false_promotion_rate",
        "stale_node_fraction",
    )


def test_stage3_claim_thresholds_fail_when_task_success_drop_exceeds_limit() -> None:
    run_specs = {system: _spec() for system in BASELINE_SYSTEMS}
    aggregate_metrics = {
        system: _metrics(
            system=system,
            false_promotion_rate=0.3,
            stale_node_fraction=0.4,
            false_merge_rate=0.2,
            task_success_rate=0.80,
        )
        for system in BASELINE_SYSTEMS
    }
    aggregate_metrics[RAW_LOG_BASELINE_SYSTEM] = _metrics(
        system=RAW_LOG_BASELINE_SYSTEM,
        false_promotion_rate=0.40,
        stale_node_fraction=0.50,
        false_merge_rate=0.30,
        task_success_rate=0.90,
    )
    aggregate_metrics[GOVERNED_SYSTEM] = _metrics(
        system=GOVERNED_SYSTEM,
        false_promotion_rate=0.34,
        stale_node_fraction=0.42,
        false_merge_rate=0.25,
        task_success_rate=0.86,  # 4pp absolute drop
    )

    result = evaluate_stage3_claim_thresholds(
        aggregate_metrics=aggregate_metrics,
        run_specs=run_specs,
    )

    assert result.policy_threshold_passed is True
    assert result.task_success_absolute_drop_percent == 4.0
    assert result.task_success_non_degradation_passed is False
    assert result.claim_thresholds_passed is False


def test_stage3_claim_thresholds_enforce_fairness_before_comparison() -> None:
    run_specs = {system: _spec() for system in BASELINE_SYSTEMS}
    run_specs["context_window_only"] = _spec(token_budget=2048)
    aggregate_metrics = {
        system: _metrics(
            system=system,
            false_promotion_rate=0.3,
            stale_node_fraction=0.4,
            false_merge_rate=0.2,
            task_success_rate=0.80,
        )
        for system in BASELINE_SYSTEMS
    }

    with pytest.raises(BaselineFairnessError):
        evaluate_stage3_claim_thresholds(
            aggregate_metrics=aggregate_metrics,
            run_specs=run_specs,
        )


def test_openai_compatible_baseline_adapter_uses_client_response() -> None:
    class FakeOpenAICompatClient:
        def chat(self, request: object) -> OpenAICompatChatResponse:
            req = request  # keep test client minimal while checking request payloads
            assert hasattr(req, "user_prompt")
            assert hasattr(req, "seed")
            assert hasattr(req, "config")
            # Narrowed checks
            user_prompt = getattr(req, "user_prompt")
            seed = getattr(req, "seed")
            config = getattr(req, "config")
            assert user_prompt == "screen this"
            assert seed == 202
            assert getattr(config, "model") == "meta_llama3.2_1b_instruct"
            return OpenAICompatChatResponse(output_text="ok-from-openai-compat")

    adapter = OpenAICompatibleBaselineAdapter(
        client=FakeOpenAICompatClient(),
        client_config=OpenAICompatClientConfig(
            base_url="http://localhost:11434/v1",
            api_key="local",
            model="meta_llama3.2_1b_instruct",
            timeout_seconds=120,
            max_tokens=256,
            temperature=0.0,
            seed=202,
        ),
    )
    result = adapter.execute(
        BaselineAdapterInput(
            system="raw_text_log_retrieval",
            prompt="screen this",
            seed=202,
            run_spec=_spec(),
        )
    )

    assert result.output_text == "ok-from-openai-compat"

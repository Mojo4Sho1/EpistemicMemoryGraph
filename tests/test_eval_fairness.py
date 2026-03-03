"""Tests for baseline fairness preflight checks."""

import pytest

from src.eval import (
    BASELINE_SYSTEMS,
    BaselineAdapterInput,
    BaselineCoverageError,
    BaselineFairnessError,
    BaselineRunResult,
    BaselineRunSpec,
    BaselineRuntime,
    build_default_baseline_adapters,
    build_default_baseline_runtime,
    check_baseline_fairness,
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

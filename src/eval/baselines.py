"""Deterministic baseline runtime adapters and Stage 3 comparison helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol

from src.eval.fairness import BaselineRunSpec, check_baseline_fairness
from src.eval.openai_compat import (
    OpenAICompatChatRequest,
    OpenAICompatClient,
    OpenAICompatClientConfig,
)
from src.eval.schemas import AggregateMetrics

BASELINE_SYSTEMS: tuple[str, ...] = (
    "context_window_only",
    "raw_text_log_retrieval",
    "summary_only_memory",
    "simple_key_value_memory",
    "graph_without_governance",
    "full_governed_system",
)
RAW_LOG_BASELINE_SYSTEM = "raw_text_log_retrieval"
GOVERNED_SYSTEM = "full_governed_system"
REQUIRED_ABLATION_SYSTEMS: tuple[str, ...] = (
    "context_window_only",
    "summary_only_memory",
    "simple_key_value_memory",
    "graph_without_governance",
)


@dataclass(frozen=True, slots=True)
class BaselineAdapterInput:
    """Deterministic adapter input envelope for one system execution."""

    system: str
    prompt: str
    seed: int
    run_spec: BaselineRunSpec


@dataclass(frozen=True, slots=True)
class BaselineRunResult:
    """Deterministic baseline adapter output for one system."""

    system: str
    adapter_label: str
    output_text: str


class BaselineAdapter(Protocol):
    """Interface for runnable baseline systems under shared controls."""

    def execute(self, request: BaselineAdapterInput) -> BaselineRunResult:
        """Run one deterministic baseline execution for the given input."""


class BaselineCoverageError(ValueError):
    """Raised when runtime adapters/specs do not cover the full baseline matrix."""


class BaselineFairnessError(ValueError):
    """Raised when fairness preflight fails before baseline execution."""

    def __init__(self, violations: tuple[str, ...]) -> None:
        super().__init__("Fairness preflight failed.")
        self.violations = violations


@dataclass(frozen=True, slots=True)
class Stage3ThresholdConfig:
    """Frozen Stage 3 claim thresholds from configs/eval_v0q.yaml."""

    minimum_relative_policy_improvement_percent: float = 10.0
    minimum_policy_metrics_improved_count: int = 3
    max_task_success_absolute_drop_percent: float = 3.0


@dataclass(frozen=True, slots=True)
class Stage3ClaimResult:
    """Deterministic Stage 3 claim-threshold outcome report."""

    raw_log_baseline_system: str
    governed_system: str
    required_ablations_present: bool
    missing_ablations: tuple[str, ...]
    relative_policy_improvements_percent: dict[str, float]
    policy_metrics_meeting_threshold: tuple[str, ...]
    policy_threshold_passed: bool
    task_success_absolute_drop_percent: float
    task_success_non_degradation_passed: bool
    claim_thresholds_passed: bool


class DeterministicBaselineAdapter:
    """Simple deterministic adapter used for runnable baseline scaffolding."""

    def __init__(self, *, adapter_label: str) -> None:
        self._adapter_label = adapter_label

    def execute(self, request: BaselineAdapterInput) -> BaselineRunResult:
        summary = (
            f"{self._adapter_label}|{request.system}|seed={request.seed}|"
            f"token_budget={request.run_spec.token_budget}|prompt={request.prompt}"
        )
        return BaselineRunResult(
            system=request.system,
            adapter_label=self._adapter_label,
            output_text=summary,
        )


class OpenAICompatibleBaselineAdapter:
    """Baseline adapter that calls an OpenAI-compatible chat endpoint."""

    def __init__(
        self,
        *,
        client: OpenAICompatClient,
        client_config: OpenAICompatClientConfig,
        adapter_label: str = "openai_compat_adapter",
        system_prompt: str = "You are a deterministic evaluation assistant.",
    ) -> None:
        self._client = client
        self._client_config = client_config
        self._adapter_label = adapter_label
        self._system_prompt = system_prompt

    def execute(self, request: BaselineAdapterInput) -> BaselineRunResult:
        response = self._client.chat(
            OpenAICompatChatRequest(
                system_prompt=self._system_prompt,
                user_prompt=request.prompt,
                seed=request.seed,
                config=self._client_config,
            )
        )
        return BaselineRunResult(
            system=request.system,
            adapter_label=self._adapter_label,
            output_text=response.output_text,
        )


class BaselineRuntime:
    """Deterministic baseline runner with fairness preflight enforcement."""

    def __init__(
        self,
        adapters: Mapping[str, BaselineAdapter],
        *,
        required_systems: tuple[str, ...] = BASELINE_SYSTEMS,
    ) -> None:
        self._adapters = dict(adapters)
        self._required_systems = required_systems

    def run_all(
        self,
        *,
        prompt: str,
        seed: int,
        run_specs: Mapping[str, BaselineRunSpec],
    ) -> dict[str, BaselineRunResult]:
        self._ensure_matrix_coverage(adapter_names=tuple(self._adapters), label="adapters")
        self._ensure_matrix_coverage(adapter_names=tuple(run_specs), label="run_specs")

        fairness_result = check_baseline_fairness(run_specs)
        if not fairness_result.passed:
            raise BaselineFairnessError(fairness_result.violations)

        results: dict[str, BaselineRunResult] = {}
        for system in self._required_systems:
            request = BaselineAdapterInput(
                system=system,
                prompt=prompt,
                seed=seed,
                run_spec=run_specs[system],
            )
            results[system] = self._adapters[system].execute(request)
        return results

    def _ensure_matrix_coverage(self, *, adapter_names: tuple[str, ...], label: str) -> None:
        actual = set(adapter_names)
        required = set(self._required_systems)
        if actual != required:
            missing = tuple(sorted(required - actual))
            extra = tuple(sorted(actual - required))
            raise BaselineCoverageError(
                f"{label} mismatch for baseline matrix; missing={missing}, extra={extra}"
            )


def build_default_baseline_adapters() -> dict[str, BaselineAdapter]:
    """Build deterministic adapters for all frozen Stage 3 baseline systems."""

    return {
        system: DeterministicBaselineAdapter(adapter_label=f"{system}_adapter")
        for system in BASELINE_SYSTEMS
    }


def build_default_baseline_runtime() -> BaselineRuntime:
    """Build runtime with deterministic coverage for all frozen baseline systems."""

    return BaselineRuntime(build_default_baseline_adapters())


def evaluate_stage3_claim_thresholds(
    *,
    aggregate_metrics: Mapping[str, AggregateMetrics],
    run_specs: Mapping[str, BaselineRunSpec],
    threshold_config: Stage3ThresholdConfig = Stage3ThresholdConfig(),
    raw_log_baseline_system: str = RAW_LOG_BASELINE_SYSTEM,
    governed_system: str = GOVERNED_SYSTEM,
    required_systems: tuple[str, ...] = BASELINE_SYSTEMS,
    required_ablations: tuple[str, ...] = REQUIRED_ABLATION_SYSTEMS,
    higher_is_better_policy_metrics: tuple[str, ...] = (),
) -> Stage3ClaimResult:
    """Evaluate Stage 3 thresholds against the raw-log baseline with fairness lock."""

    _ensure_matrix_coverage(
        label="aggregate_metrics",
        required_systems=required_systems,
        actual_systems=tuple(aggregate_metrics),
    )
    _ensure_matrix_coverage(
        label="run_specs",
        required_systems=required_systems,
        actual_systems=tuple(run_specs),
    )

    fairness_result = check_baseline_fairness(run_specs)
    if not fairness_result.passed:
        raise BaselineFairnessError(fairness_result.violations)

    missing_ablations = tuple(
        system for system in required_ablations if system not in aggregate_metrics
    )
    required_ablations_present = not missing_ablations

    baseline_metrics = aggregate_metrics[raw_log_baseline_system]
    governed_metrics = aggregate_metrics[governed_system]
    relative_improvements = _compute_relative_policy_improvements(
        baseline_policy_metrics=baseline_metrics.policy_metrics,
        governed_policy_metrics=governed_metrics.policy_metrics,
        higher_is_better_policy_metrics=higher_is_better_policy_metrics,
    )

    passing_policy_metrics = tuple(
        metric_name
        for metric_name, value in relative_improvements.items()
        if value >= threshold_config.minimum_relative_policy_improvement_percent
    )
    policy_threshold_passed = (
        len(passing_policy_metrics) >= threshold_config.minimum_policy_metrics_improved_count
    )

    task_success_drop = _compute_task_success_absolute_drop_percent(
        raw_log_task_metrics=baseline_metrics.task_metrics,
        governed_task_metrics=governed_metrics.task_metrics,
    )
    task_success_non_degradation_passed = (
        task_success_drop <= threshold_config.max_task_success_absolute_drop_percent
    )

    claim_thresholds_passed = (
        required_ablations_present
        and policy_threshold_passed
        and task_success_non_degradation_passed
    )
    return Stage3ClaimResult(
        raw_log_baseline_system=raw_log_baseline_system,
        governed_system=governed_system,
        required_ablations_present=required_ablations_present,
        missing_ablations=missing_ablations,
        relative_policy_improvements_percent=relative_improvements,
        policy_metrics_meeting_threshold=passing_policy_metrics,
        policy_threshold_passed=policy_threshold_passed,
        task_success_absolute_drop_percent=task_success_drop,
        task_success_non_degradation_passed=task_success_non_degradation_passed,
        claim_thresholds_passed=claim_thresholds_passed,
    )


def _ensure_matrix_coverage(
    *,
    label: str,
    required_systems: tuple[str, ...],
    actual_systems: tuple[str, ...],
) -> None:
    actual = set(actual_systems)
    required = set(required_systems)
    if actual != required:
        missing = tuple(sorted(required - actual))
        extra = tuple(sorted(actual - required))
        raise BaselineCoverageError(
            f"{label} mismatch for baseline matrix; missing={missing}, extra={extra}"
        )


def _compute_relative_policy_improvements(
    *,
    baseline_policy_metrics: Mapping[str, float],
    governed_policy_metrics: Mapping[str, float],
    higher_is_better_policy_metrics: tuple[str, ...],
) -> dict[str, float]:
    if set(baseline_policy_metrics) != set(governed_policy_metrics):
        missing = tuple(sorted(set(baseline_policy_metrics) - set(governed_policy_metrics)))
        extra = tuple(sorted(set(governed_policy_metrics) - set(baseline_policy_metrics)))
        raise BaselineCoverageError(
            f"policy metric mismatch; missing={missing}, extra={extra}"
        )

    improvements: dict[str, float] = {}
    higher_is_better = set(higher_is_better_policy_metrics)
    for metric_name in baseline_policy_metrics:
        baseline_value = baseline_policy_metrics[metric_name]
        governed_value = governed_policy_metrics[metric_name]
        denominator = abs(baseline_value) if baseline_value != 0 else 1.0
        if metric_name in higher_is_better:
            delta = governed_value - baseline_value
        else:
            delta = baseline_value - governed_value
        improvements[metric_name] = round((delta / denominator) * 100.0, 6)
    return improvements


def _compute_task_success_absolute_drop_percent(
    *,
    raw_log_task_metrics: Mapping[str, float],
    governed_task_metrics: Mapping[str, float],
) -> float:
    if "task_success_rate" not in raw_log_task_metrics:
        raise BaselineCoverageError(
            "raw-log task metrics missing required 'task_success_rate'."
        )
    if "task_success_rate" not in governed_task_metrics:
        raise BaselineCoverageError(
            "governed task metrics missing required 'task_success_rate'."
        )

    raw_log_success = raw_log_task_metrics["task_success_rate"]
    governed_success = governed_task_metrics["task_success_rate"]
    return round((raw_log_success - governed_success) * 100.0, 6)

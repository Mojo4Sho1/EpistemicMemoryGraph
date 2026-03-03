"""Deterministic baseline runtime adapters for v0.1q Stage 3 comparisons."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol

from src.eval.fairness import BaselineRunSpec, check_baseline_fairness

BASELINE_SYSTEMS: tuple[str, ...] = (
    "context_window_only",
    "raw_text_log_retrieval",
    "summary_only_memory",
    "simple_key_value_memory",
    "graph_without_governance",
    "full_governed_system",
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

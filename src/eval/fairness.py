"""Baseline fairness preflight checks for v0.1q evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class BaselineRunSpec:
    """Execution controls that must match across systems for fair comparison."""

    model_snapshot: str
    prompt_template_family: str
    tool_availability: tuple[str, ...]
    token_budget: int
    wall_clock_timeout_seconds: int
    seed_set: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class FairnessCheckResult:
    """Result of baseline parity validation before benchmark execution."""

    passed: bool
    violations: tuple[str, ...]


def check_baseline_fairness(specs: Mapping[str, BaselineRunSpec]) -> FairnessCheckResult:
    """Ensure all systems use equivalent non-policy execution constraints."""

    if not specs:
        return FairnessCheckResult(
            passed=False,
            violations=("No baseline specs provided.",),
        )

    items = list(specs.items())
    reference_name, reference_spec = items[0]
    violations: list[str] = []

    for system_name, system_spec in items[1:]:
        if system_spec.model_snapshot != reference_spec.model_snapshot:
            violations.append(
                f"{system_name}: model_snapshot differs from {reference_name}."
            )
        if system_spec.prompt_template_family != reference_spec.prompt_template_family:
            violations.append(
                f"{system_name}: prompt_template_family differs from {reference_name}."
            )
        if tuple(system_spec.tool_availability) != tuple(reference_spec.tool_availability):
            violations.append(
                f"{system_name}: tool_availability differs from {reference_name}."
            )
        if system_spec.token_budget != reference_spec.token_budget:
            violations.append(f"{system_name}: token_budget differs from {reference_name}.")
        if (
            system_spec.wall_clock_timeout_seconds
            != reference_spec.wall_clock_timeout_seconds
        ):
            violations.append(
                f"{system_name}: wall_clock_timeout_seconds differs from {reference_name}."
            )
        if tuple(system_spec.seed_set) != tuple(reference_spec.seed_set):
            violations.append(f"{system_name}: seed_set differs from {reference_name}.")

    return FairnessCheckResult(
        passed=not violations,
        violations=tuple(violations),
    )

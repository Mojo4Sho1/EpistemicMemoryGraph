"""Evaluation package exports for v0.1q fairness and artifact schemas."""

from src.eval.artifacts import (
    build_run_directory_name,
    stable_hash,
    write_run_artifacts,
)
from src.eval.baselines import (
    BASELINE_SYSTEMS,
    BaselineAdapter,
    BaselineAdapterInput,
    BaselineCoverageError,
    BaselineFairnessError,
    BaselineRunResult,
    BaselineRuntime,
    DeterministicBaselineAdapter,
    build_default_baseline_adapters,
    build_default_baseline_runtime,
)
from src.eval.fairness import BaselineRunSpec, FairnessCheckResult, check_baseline_fairness
from src.eval.schemas import (
    AggregateMetrics,
    ConsolidationEvent,
    RunManifest,
    ScenarioResult,
    TransitionEvent,
    utc_now_iso,
)

__all__ = [
    "AggregateMetrics",
    "BASELINE_SYSTEMS",
    "BaselineAdapter",
    "BaselineAdapterInput",
    "BaselineCoverageError",
    "BaselineFairnessError",
    "BaselineRunSpec",
    "BaselineRunResult",
    "BaselineRuntime",
    "ConsolidationEvent",
    "DeterministicBaselineAdapter",
    "FairnessCheckResult",
    "RunManifest",
    "ScenarioResult",
    "TransitionEvent",
    "build_run_directory_name",
    "build_default_baseline_adapters",
    "build_default_baseline_runtime",
    "check_baseline_fairness",
    "stable_hash",
    "utc_now_iso",
    "write_run_artifacts",
]

"""Machine-readable run artifact schema definitions for v0.1q evaluation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class RunManifest:
    """Top-level run metadata and reproducibility hashes."""

    model_id: str
    git_sha: str
    system: str
    seed: int
    timestamp_utc: str
    config_hash: str
    scenario_bundle_hash: str
    reproducibility_hash: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TransitionEvent:
    """State transition event with evidence references and rule id."""

    proposition_id: str
    prior_state: str
    new_state: str
    confidence: float
    support_score: float
    contradiction_score: float
    freshness: float
    evidence_ids: tuple[str, ...]
    rule_id: str
    timestamp_utc: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ConsolidationEvent:
    """Consolidation checkpoint event with promotion/archival outcomes."""

    session_id: str
    task_id: str
    promoted_proposition_ids: tuple[str, ...]
    archived_proposition_ids: tuple[str, ...]
    discarded_proposition_ids: tuple[str, ...]
    carryover_retained_ids: tuple[str, ...]
    overflow_reason_code: str | None
    rule_id: str
    timestamp_utc: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ScenarioResult:
    """Per-scenario outcome record for deterministic benchmark reporting."""

    stage: str
    scenario_id: str
    system: str
    seed: int
    task_success: bool
    policy_metrics: dict[str, float]
    identity_metrics: dict[str, float]
    memory_health_metrics: dict[str, float]
    task_metrics: dict[str, float]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class AggregateMetrics:
    """Aggregated metrics summary for baseline and governed-system comparison."""

    system: str
    seed_set: tuple[int, ...]
    policy_metrics: dict[str, float]
    identity_metrics: dict[str, float]
    memory_health_metrics: dict[str, float]
    task_metrics: dict[str, float]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def utc_now_iso() -> str:
    """Return UTC timestamp in a stable ISO-8601 representation."""

    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

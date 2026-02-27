"""Minimal typed v0 model primitives for core memory objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from src.core.constants import BELIEF_STATES


@dataclass(frozen=True, slots=True)
class Observation:
    """Immutable evidence object captured from an input source."""

    observation_id: str
    timestamp: datetime
    source_id: str
    source_type: str
    source_independence_group: str
    session_id: str
    task_id: str
    raw_payload: str
    parsed_payload: dict[str, Any]
    ingest_status: str


@dataclass(slots=True)
class Entity:
    """Canonical or candidate identity node."""

    entity_id: str
    canonical_name: str
    entity_type: str
    aliases: tuple[str, ...] = ()
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    is_canonical: bool = False


@dataclass(slots=True)
class Proposition:
    """Claim object carrying status and scoring signals."""

    proposition_id: str
    text: str
    structured_form: dict[str, Any] | None
    status: str
    confidence: float
    support_weight: float
    contradiction_weight: float
    source_group_count: int
    recency: float
    volatility: float
    provenance_summary: str

    def __post_init__(self) -> None:
        if self.status not in BELIEF_STATES:
            msg = f"Unsupported belief state: {self.status}"
            raise ValueError(msg)

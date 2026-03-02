"""Minimal typed v0 model primitives for core memory objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from src.core.constants import BELIEF_STATES


def _identity_key(value: str) -> str:
    return value.strip().casefold()


def _dedupe_identity_terms(
    terms: tuple[str, ...], *, exclude_keys: frozenset[str] = frozenset()
) -> tuple[str, ...]:
    deduped: list[str] = []
    seen_keys = set(exclude_keys)
    for term in terms:
        stripped = term.strip()
        if not stripped:
            continue
        key = _identity_key(stripped)
        if key in seen_keys:
            continue
        seen_keys.add(key)
        deduped.append(stripped)
    return tuple(deduped)


def _dedupe_entity_ids(
    entity_ids: tuple[str, ...], *, exclude_ids: frozenset[str] = frozenset()
) -> tuple[str, ...]:
    deduped: list[str] = []
    seen_ids = set(exclude_ids)
    for entity_id in entity_ids:
        stripped = entity_id.strip()
        if not stripped or stripped in seen_ids:
            continue
        seen_ids.add(stripped)
        deduped.append(stripped)
    return tuple(deduped)


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
    possible_same_as: tuple[str, ...] = ()
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    is_canonical: bool = False

    def __post_init__(self) -> None:
        self.entity_id = self.entity_id.strip()
        if not self.entity_id:
            msg = "entity_id must be non-empty"
            raise ValueError(msg)

        self.canonical_name = self.canonical_name.strip()
        if not self.canonical_name:
            msg = "canonical_name must be non-empty"
            raise ValueError(msg)

        self.entity_type = self.entity_type.strip()
        if not self.entity_type:
            msg = "entity_type must be non-empty"
            raise ValueError(msg)

        canonical_key = _identity_key(self.canonical_name)
        self.aliases = _dedupe_identity_terms(
            self.aliases, exclude_keys=frozenset({canonical_key})
        )
        self.possible_same_as = _dedupe_entity_ids(
            self.possible_same_as, exclude_ids=frozenset({self.entity_id})
        )

    def identity_terms(self) -> tuple[str, ...]:
        """Return canonical name and aliases for deterministic matching."""

        return (self.canonical_name, *self.aliases)


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

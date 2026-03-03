"""Deterministic read/query interfaces for canonical-memory reactivation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


def _normalize_key(value: str) -> str:
    return value.strip().casefold()


def _dedupe_keys(keys: tuple[str, ...]) -> tuple[str, ...]:
    normalized: list[str] = []
    seen: set[str] = set()
    for key in keys:
        normalized_key = _normalize_key(key)
        if not normalized_key or normalized_key in seen:
            continue
        seen.add(normalized_key)
        normalized.append(normalized_key)
    return tuple(normalized)


def _dedupe_ids(values: tuple[str, ...]) -> tuple[str, ...]:
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        stripped = value.strip()
        if not stripped or stripped in seen:
            continue
        seen.add(stripped)
        deduped.append(stripped)
    return tuple(deduped)


@dataclass(slots=True)
class CanonicalMemoryNode:
    """Canonical graph node projection used for bounded reactivation loads."""

    node_id: str
    session_id: str
    task_id: str
    entity_ids: tuple[str, ...] = ()
    proposition_ids: tuple[str, ...] = ()
    relevance_keys: tuple[str, ...] = ()
    payload_summary: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        self.node_id = self.node_id.strip()
        self.session_id = self.session_id.strip()
        self.task_id = self.task_id.strip()

        if not self.node_id:
            msg = "node_id must be non-empty"
            raise ValueError(msg)
        if not self.session_id:
            msg = "session_id must be non-empty"
            raise ValueError(msg)
        if not self.task_id:
            msg = "task_id must be non-empty"
            raise ValueError(msg)

        self.entity_ids = _dedupe_ids(self.entity_ids)
        self.proposition_ids = _dedupe_ids(self.proposition_ids)
        self.relevance_keys = _dedupe_keys(self.relevance_keys)


@dataclass(slots=True)
class CanonicalSubgraphQuery:
    """Typed request for deterministic canonical-context lookup."""

    session_id: str
    task_id: str
    relevance_keys: tuple[str, ...]
    limit: int = 8

    def __post_init__(self) -> None:
        self.session_id = self.session_id.strip()
        self.task_id = self.task_id.strip()
        if not self.session_id:
            msg = "session_id must be non-empty"
            raise ValueError(msg)
        if not self.task_id:
            msg = "task_id must be non-empty"
            raise ValueError(msg)
        if self.limit < 0:
            msg = "limit must be >= 0"
            raise ValueError(msg)
        self.relevance_keys = _dedupe_keys(self.relevance_keys)


class CanonicalMemoryStore(ABC):
    """Read/query boundary for canonical graph context reactivation."""

    @abstractmethod
    def query_relevant_subgraph(
        self, query: CanonicalSubgraphQuery
    ) -> tuple[CanonicalMemoryNode, ...]:
        """Return only session/task relevant canonical nodes for reactivation."""


class InMemoryCanonicalMemoryStore(CanonicalMemoryStore):
    """In-memory canonical graph projection for deterministic runtime tests."""

    def __init__(self) -> None:
        self._nodes: list[CanonicalMemoryNode] = []

    def append_node(self, node: CanonicalMemoryNode) -> None:
        """Append one canonical node in deterministic insertion order."""

        self._nodes.append(node)

    def query_relevant_subgraph(
        self, query: CanonicalSubgraphQuery
    ) -> tuple[CanonicalMemoryNode, ...]:
        if query.limit == 0 or not query.relevance_keys:
            return ()

        ranked_matches: list[tuple[int, int, CanonicalMemoryNode]] = []
        query_keys = set(query.relevance_keys)

        for index, node in enumerate(self._nodes):
            if node.session_id != query.session_id or node.task_id != query.task_id:
                continue
            overlap = query_keys.intersection(node.relevance_keys)
            if not overlap:
                continue
            ranked_matches.append((-len(overlap), index, node))

        ranked_matches.sort()
        return tuple(node for _, _, node in ranked_matches[: query.limit])

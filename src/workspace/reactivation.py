"""Deterministic canonical-context retrieval/reactivation boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from src.store import CanonicalMemoryNode, CanonicalMemoryStore, CanonicalSubgraphQuery

ReactivationStatus = Literal["not_requested", "no_matches", "loaded"]


def _dedupe_ids(values: list[str]) -> tuple[str, ...]:
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return tuple(ordered)


@dataclass(frozen=True, slots=True)
class ReactivationRequest:
    """Typed request for session/task-scoped canonical-context reactivation."""

    session_id: str
    task_id: str
    relevance_keys: tuple[str, ...]
    limit: int = 8


@dataclass(frozen=True, slots=True)
class ReactivationResult:
    """Deterministic reactivation output without full-graph hydration."""

    status: ReactivationStatus
    canonical_nodes: tuple[CanonicalMemoryNode, ...]
    hydrated_entity_ids: tuple[str, ...]
    hydrated_proposition_ids: tuple[str, ...]
    rule_id: str


class WorkspaceReactivationBoundary:
    """Load only relevant canonical context for one workspace update."""

    def __init__(self, store: CanonicalMemoryStore) -> None:
        self._store = store

    def reactivate(self, request: ReactivationRequest) -> ReactivationResult:
        query = CanonicalSubgraphQuery(
            session_id=request.session_id,
            task_id=request.task_id,
            relevance_keys=request.relevance_keys,
            limit=request.limit,
        )
        if not query.relevance_keys:
            return ReactivationResult(
                status="not_requested",
                canonical_nodes=(),
                hydrated_entity_ids=(),
                hydrated_proposition_ids=(),
                rule_id="reactivation.not_requested",
            )

        nodes = self._store.query_relevant_subgraph(query)
        if not nodes:
            return ReactivationResult(
                status="no_matches",
                canonical_nodes=(),
                hydrated_entity_ids=(),
                hydrated_proposition_ids=(),
                rule_id="reactivation.no_matches",
            )

        entity_ids: list[str] = []
        proposition_ids: list[str] = []
        for node in nodes:
            entity_ids.extend(node.entity_ids)
            proposition_ids.extend(node.proposition_ids)

        return ReactivationResult(
            status="loaded",
            canonical_nodes=nodes,
            hydrated_entity_ids=_dedupe_ids(entity_ids),
            hydrated_proposition_ids=_dedupe_ids(proposition_ids),
            rule_id="reactivation.loaded_relevant_subgraph",
        )

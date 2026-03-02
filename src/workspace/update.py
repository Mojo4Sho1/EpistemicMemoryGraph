"""Composed deterministic workspace update boundary for v0.1q."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from src.core.models import Entity, Observation
from src.workspace.consolidation import (
    ConsolidationDecision,
    PromotionDecision,
    evaluate_promotion_eligibility,
    should_run_consolidation,
)
from src.workspace.intake import (
    IntakeStatus,
    ObservationIntakeRequest,
    WorkspaceObservationIntake,
)
from src.workspace.state import (
    InMemoryWorkspaceObservationIndex,
    ObservationIndexRegisterRequest,
)

IndexUpdateStatus = Literal["indexed", "already_indexed"]
IdentityUpdateStatus = Literal[
    "not_requested",
    "created",
    "updated",
    "no_change",
    "linked_possible_same_as",
]


def _identity_key(value: str) -> str:
    return value.strip().casefold()


def _dedupe_entity_ids(entity_ids: tuple[str, ...]) -> tuple[str, ...]:
    ordered: list[str] = []
    seen: set[str] = set()
    for entity_id in entity_ids:
        stripped = entity_id.strip()
        if not stripped or stripped in seen:
            continue
        seen.add(stripped)
        ordered.append(stripped)
    return tuple(ordered)


@dataclass(frozen=True, slots=True)
class IdentityUpdateDecision:
    """Deterministic identity-handling outcome for one workspace update."""

    status: IdentityUpdateStatus
    entity_id: str | None
    alias_links_added: tuple[str, ...]
    possible_same_as_links_added: tuple[str, ...]
    merge_blocked: bool
    hard_merge_performed: bool
    rule_id: str


@dataclass(frozen=True, slots=True)
class WorkspaceUpdateRequest:
    """Typed request for one composed workspace update call."""

    observation: Observation
    new_observations_since_last: int
    at_task_boundary: bool
    proposition_state: str
    proposition_freshness: float
    identity_entity: Entity | None = None


@dataclass(frozen=True, slots=True)
class WorkspaceUpdateResult:
    """Deterministic composed update result across intake/index/gating."""

    observation_id: str
    session_id: str
    task_id: str
    intake_status: IntakeStatus
    stored: bool
    index_status: IndexUpdateStatus
    observation_ids: tuple[str, ...]
    consolidation: ConsolidationDecision
    promotion: PromotionDecision
    identity: IdentityUpdateDecision


class WorkspaceUpdateBoundary:
    """Compose intake + session/task indexing + policy gate metadata."""

    def __init__(
        self,
        *,
        intake: WorkspaceObservationIntake,
        index: InMemoryWorkspaceObservationIndex,
    ) -> None:
        self._intake = intake
        self._index = index
        self._entities: dict[str, Entity] = {}
        self._alias_index: dict[str, list[str]] = {}

    def get_entity_ids(self) -> tuple[str, ...]:
        """Return deterministic identity insertion order for test visibility."""

        return tuple(self._entities.keys())

    def get_entity(self, entity_id: str) -> Entity | None:
        """Return a safe entity snapshot by id when present."""

        entity = self._entities.get(entity_id)
        if entity is None:
            return None
        return self._clone_entity(entity)

    def update(self, request: WorkspaceUpdateRequest) -> WorkspaceUpdateResult:
        """Apply one deterministic workspace update for a single observation."""

        if request.new_observations_since_last < 0:
            msg = "new_observations_since_last must be >= 0"
            raise ValueError(msg)

        observation = request.observation
        intake_result = self._intake.ingest(ObservationIntakeRequest(observation=observation))
        current_observation_ids = self._index.get_observation_ids(
            observation.session_id, observation.task_id
        )

        if observation.observation_id in current_observation_ids:
            index_status: IndexUpdateStatus = "already_indexed"
            observation_ids = current_observation_ids
        else:
            register_result = self._index.register(
                ObservationIndexRegisterRequest(
                    session_id=observation.session_id,
                    task_id=observation.task_id,
                    observation_id=observation.observation_id,
                )
            )
            index_status = "indexed"
            observation_ids = register_result.observation_ids

        consolidation = should_run_consolidation(
            new_observations_since_last=request.new_observations_since_last,
            at_task_boundary=request.at_task_boundary,
        )
        promotion = evaluate_promotion_eligibility(
            proposition_state=request.proposition_state,
            freshness=request.proposition_freshness,
        )
        identity = self._update_identity(request.identity_entity)

        return WorkspaceUpdateResult(
            observation_id=observation.observation_id,
            session_id=observation.session_id,
            task_id=observation.task_id,
            intake_status=intake_result.status,
            stored=intake_result.stored,
            index_status=index_status,
            observation_ids=observation_ids,
            consolidation=consolidation,
            promotion=promotion,
            identity=identity,
        )

    def _update_identity(self, candidate: Entity | None) -> IdentityUpdateDecision:
        if candidate is None:
            return IdentityUpdateDecision(
                status="not_requested",
                entity_id=None,
                alias_links_added=(),
                possible_same_as_links_added=(),
                merge_blocked=False,
                hard_merge_performed=False,
                rule_id="identity.not_requested",
            )

        existing = self._entities.get(candidate.entity_id)
        if existing is not None:
            alias_links_added = self._add_alias_links(existing, candidate.aliases)
            possible_same_as_links_added = self._add_possible_same_as_links(
                existing, candidate.possible_same_as
            )
            if alias_links_added or possible_same_as_links_added:
                status: IdentityUpdateStatus = "updated"
                rule_id = "identity.updated"
            else:
                status = "no_change"
                rule_id = "identity.no_change"
            return IdentityUpdateDecision(
                status=status,
                entity_id=existing.entity_id,
                alias_links_added=alias_links_added,
                possible_same_as_links_added=possible_same_as_links_added,
                merge_blocked=False,
                hard_merge_performed=False,
                rule_id=rule_id,
            )

        self._create_entity(candidate)
        created = self._entities[candidate.entity_id]
        explicit_links = tuple(
            entity_id
            for entity_id in candidate.possible_same_as
            if entity_id in self._entities and entity_id != created.entity_id
        )
        alias_ambiguity_links = self._find_identity_matches(created)
        desired_links = _dedupe_entity_ids((*explicit_links, *alias_ambiguity_links))
        possible_same_as_links_added = self._add_possible_same_as_links(created, desired_links)
        for linked_id in possible_same_as_links_added:
            linked_entity = self._entities[linked_id]
            self._add_possible_same_as_links(linked_entity, (created.entity_id,))

        if possible_same_as_links_added:
            return IdentityUpdateDecision(
                status="linked_possible_same_as",
                entity_id=created.entity_id,
                alias_links_added=(),
                possible_same_as_links_added=possible_same_as_links_added,
                merge_blocked=True,
                hard_merge_performed=False,
                rule_id="identity.ambiguity.link_only",
            )

        return IdentityUpdateDecision(
            status="created",
            entity_id=created.entity_id,
            alias_links_added=(),
            possible_same_as_links_added=(),
            merge_blocked=False,
            hard_merge_performed=False,
            rule_id="identity.created",
        )

    def _create_entity(self, candidate: Entity) -> None:
        entity = self._clone_entity(candidate)
        self._entities[entity.entity_id] = entity
        self._register_alias_terms(entity, entity.identity_terms())

    def _find_identity_matches(self, candidate: Entity) -> tuple[str, ...]:
        matches: list[str] = []
        for term in candidate.identity_terms():
            key = _identity_key(term)
            for entity_id in self._alias_index.get(key, []):
                if entity_id == candidate.entity_id or entity_id in matches:
                    continue
                matches.append(entity_id)
        return tuple(matches)

    def _register_alias_terms(self, entity: Entity, terms: tuple[str, ...]) -> None:
        for term in terms:
            key = _identity_key(term)
            if not key:
                continue
            entity_ids = self._alias_index.setdefault(key, [])
            if entity.entity_id not in entity_ids:
                entity_ids.append(entity.entity_id)

    def _add_alias_links(self, entity: Entity, aliases: tuple[str, ...]) -> tuple[str, ...]:
        added: list[str] = []
        existing_aliases = list(entity.aliases)
        seen_keys = {_identity_key(term) for term in entity.identity_terms()}
        canonical_key = _identity_key(entity.canonical_name)

        for alias in aliases:
            stripped = alias.strip()
            if not stripped:
                continue
            key = _identity_key(stripped)
            if key == canonical_key or key in seen_keys:
                continue
            seen_keys.add(key)
            existing_aliases.append(stripped)
            added.append(stripped)

        if added:
            entity.aliases = tuple(existing_aliases)
            entity.updated_at = datetime.utcnow()
            self._register_alias_terms(entity, tuple(added))
        return tuple(added)

    def _add_possible_same_as_links(
        self, entity: Entity, candidate_links: tuple[str, ...]
    ) -> tuple[str, ...]:
        added: list[str] = []
        existing = set(entity.possible_same_as)
        possible_same_as = list(entity.possible_same_as)

        for linked_id in candidate_links:
            stripped = linked_id.strip()
            if (
                not stripped
                or stripped == entity.entity_id
                or stripped in existing
                or stripped not in self._entities
            ):
                continue
            existing.add(stripped)
            possible_same_as.append(stripped)
            added.append(stripped)

        if added:
            entity.possible_same_as = tuple(possible_same_as)
            entity.updated_at = datetime.utcnow()
        return tuple(added)

    @staticmethod
    def _clone_entity(entity: Entity) -> Entity:
        return Entity(
            entity_id=entity.entity_id,
            canonical_name=entity.canonical_name,
            entity_type=entity.entity_type,
            aliases=entity.aliases,
            possible_same_as=entity.possible_same_as,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_canonical=entity.is_canonical,
        )

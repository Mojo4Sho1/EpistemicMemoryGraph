"""Tests for composed workspace update boundary behavior."""

from datetime import datetime

from src.core.models import Entity, Observation
from src.store import InMemoryObservationStore
from src.workspace import (
    InMemoryWorkspaceObservationIndex,
    WorkspaceObservationIntake,
    WorkspaceUpdateBoundary,
    WorkspaceUpdateRequest,
)


def _build_observation(observation_id: str) -> Observation:
    return Observation(
        observation_id=observation_id,
        timestamp=datetime(2026, 2, 28, 9, 0, 0),
        source_id="source-1",
        source_type="api",
        source_independence_group="group-a",
        session_id="session-1",
        task_id="task-1",
        raw_payload="raw",
        parsed_payload={"value": observation_id},
        ingest_status="ingested",
    )


def _build_boundary() -> WorkspaceUpdateBoundary:
    store = InMemoryObservationStore()
    intake = WorkspaceObservationIntake(store)
    index = InMemoryWorkspaceObservationIndex()
    return WorkspaceUpdateBoundary(intake=intake, index=index)


def _build_entity(
    entity_id: str,
    canonical_name: str,
    *,
    aliases: tuple[str, ...] = (),
    possible_same_as: tuple[str, ...] = (),
) -> Entity:
    return Entity(
        entity_id=entity_id,
        canonical_name=canonical_name,
        entity_type="person",
        aliases=aliases,
        possible_same_as=possible_same_as,
        is_canonical=False,
    )


def test_update_ingests_indexes_and_returns_gate_metadata() -> None:
    boundary = _build_boundary()
    request = WorkspaceUpdateRequest(
        observation=_build_observation("obs-update-1"),
        new_observations_since_last=1,
        at_task_boundary=False,
        proposition_state="accepted",
        proposition_freshness=0.5,
    )

    result = boundary.update(request)

    assert result.observation_id == "obs-update-1"
    assert result.intake_status == "ingested"
    assert result.stored is True
    assert result.index_status == "indexed"
    assert result.observation_ids == ("obs-update-1",)
    assert result.consolidation.should_consolidate is False
    assert result.consolidation.rule_id == "consolidation.not_due"
    assert result.promotion.eligible is True
    assert result.promotion.rule_id == "promotion.eligible"
    assert result.identity.status == "not_requested"
    assert result.identity.rule_id == "identity.not_requested"
    assert result.identity.hard_merge_performed is False


def test_update_duplicate_observation_is_index_idempotent() -> None:
    boundary = _build_boundary()
    request = WorkspaceUpdateRequest(
        observation=_build_observation("obs-update-dup"),
        new_observations_since_last=2,
        at_task_boundary=False,
        proposition_state="accepted",
        proposition_freshness=0.5,
    )

    first = boundary.update(request)
    second = boundary.update(request)

    assert first.intake_status == "ingested"
    assert first.index_status == "indexed"
    assert first.observation_ids == ("obs-update-dup",)
    assert second.intake_status == "duplicate"
    assert second.stored is False
    assert second.index_status == "already_indexed"
    assert second.observation_ids == ("obs-update-dup",)


def test_update_indexes_duplicate_when_missing_from_session_task_index() -> None:
    store = InMemoryObservationStore()
    observation = _build_observation("obs-update-dup-not-indexed")
    store.append(observation)

    intake = WorkspaceObservationIntake(store)
    index = InMemoryWorkspaceObservationIndex()
    boundary = WorkspaceUpdateBoundary(intake=intake, index=index)
    request = WorkspaceUpdateRequest(
        observation=observation,
        new_observations_since_last=25,
        at_task_boundary=False,
        proposition_state="accepted",
        proposition_freshness=0.2,
    )

    result = boundary.update(request)

    assert result.intake_status == "duplicate"
    assert result.stored is False
    assert result.index_status == "indexed"
    assert result.observation_ids == ("obs-update-dup-not-indexed",)
    assert result.consolidation.should_consolidate is True
    assert result.consolidation.rule_id == "consolidation.cadence.25"
    assert result.promotion.eligible is False
    assert result.promotion.rule_id == "promotion.ineligible.freshness"


def test_update_rejects_negative_new_observation_count() -> None:
    boundary = _build_boundary()
    request = WorkspaceUpdateRequest(
        observation=_build_observation("obs-update-negative"),
        new_observations_since_last=-1,
        at_task_boundary=False,
        proposition_state="accepted",
        proposition_freshness=0.5,
    )

    try:
        boundary.update(request)
    except ValueError as exc:
        assert str(exc) == "new_observations_since_last must be >= 0"
    else:
        raise AssertionError("Expected ValueError for negative new observation count.")


def test_update_identity_links_ambiguity_without_hard_merge() -> None:
    boundary = _build_boundary()
    first = WorkspaceUpdateRequest(
        observation=_build_observation("obs-identity-1"),
        new_observations_since_last=1,
        at_task_boundary=False,
        proposition_state="accepted",
        proposition_freshness=0.9,
        identity_entity=_build_entity(
            "ent-ada-primary",
            "Ada Lovelace",
            aliases=("A. Lovelace",),
        ),
    )
    second = WorkspaceUpdateRequest(
        observation=_build_observation("obs-identity-2"),
        new_observations_since_last=2,
        at_task_boundary=False,
        proposition_state="accepted",
        proposition_freshness=0.9,
        identity_entity=_build_entity(
            "ent-ada-candidate",
            "ada lovelace",
            aliases=("Ada L.",),
        ),
    )

    first_result = boundary.update(first)
    second_result = boundary.update(second)

    assert first_result.identity.status == "created"
    assert second_result.identity.status == "linked_possible_same_as"
    assert second_result.identity.entity_id == "ent-ada-candidate"
    assert second_result.identity.possible_same_as_links_added == ("ent-ada-primary",)
    assert second_result.identity.merge_blocked is True
    assert second_result.identity.hard_merge_performed is False
    assert boundary.get_entity_ids() == ("ent-ada-primary", "ent-ada-candidate")

    primary = boundary.get_entity("ent-ada-primary")
    candidate = boundary.get_entity("ent-ada-candidate")
    assert primary is not None
    assert candidate is not None
    assert primary.possible_same_as == ("ent-ada-candidate",)
    assert candidate.possible_same_as == ("ent-ada-primary",)


def test_update_identity_updates_existing_entity_aliases_only() -> None:
    boundary = _build_boundary()
    first = WorkspaceUpdateRequest(
        observation=_build_observation("obs-identity-update-1"),
        new_observations_since_last=1,
        at_task_boundary=False,
        proposition_state="accepted",
        proposition_freshness=0.9,
        identity_entity=_build_entity(
            "ent-grace",
            "Grace Hopper",
            aliases=("Rear Admiral Hopper",),
        ),
    )
    second = WorkspaceUpdateRequest(
        observation=_build_observation("obs-identity-update-2"),
        new_observations_since_last=2,
        at_task_boundary=False,
        proposition_state="accepted",
        proposition_freshness=0.9,
        identity_entity=_build_entity(
            "ent-grace",
            "Grace Hopper",
            aliases=("Grace Brewster Murray Hopper", "rear admiral hopper"),
        ),
    )

    boundary.update(first)
    second_result = boundary.update(second)

    assert second_result.identity.status == "updated"
    assert second_result.identity.alias_links_added == (
        "Grace Brewster Murray Hopper",
    )
    assert second_result.identity.merge_blocked is False
    assert second_result.identity.hard_merge_performed is False
    assert boundary.get_entity_ids() == ("ent-grace",)

    updated_entity = boundary.get_entity("ent-grace")
    assert updated_entity is not None
    assert updated_entity.aliases == (
        "Rear Admiral Hopper",
        "Grace Brewster Murray Hopper",
    )

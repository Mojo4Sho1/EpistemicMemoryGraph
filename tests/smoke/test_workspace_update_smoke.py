"""Smoke tests for deterministic composed workspace update behavior."""

from datetime import datetime

import pytest

from src.core.models import Observation
from src.store import (
    CanonicalMemoryNode,
    InMemoryCanonicalMemoryStore,
    InMemoryObservationStore,
)
from src.workspace import (
    InMemoryWorkspaceObservationIndex,
    WorkspaceObservationIntake,
    WorkspaceReactivationBoundary,
    WorkspaceUpdateBoundary,
    WorkspaceUpdateRequest,
)

pytestmark = pytest.mark.smoke


def _build_observation(observation_id: str) -> Observation:
    return Observation(
        observation_id=observation_id,
        timestamp=datetime(2026, 2, 28, 10, 0, 0),
        source_id="smoke-source",
        source_type="api",
        source_independence_group="smoke-group",
        session_id="smoke-session",
        task_id="smoke-task",
        raw_payload='{"event":"smoke"}',
        parsed_payload={"observation_id": observation_id},
        ingest_status="ingested",
    )


def _build_boundary() -> WorkspaceUpdateBoundary:
    intake = WorkspaceObservationIntake(InMemoryObservationStore())
    index = InMemoryWorkspaceObservationIndex()
    canonical_store = InMemoryCanonicalMemoryStore()
    canonical_store.append_node(
        CanonicalMemoryNode(
            node_id="node-smoke",
            session_id="smoke-session",
            task_id="smoke-task",
            entity_ids=("ent-smoke",),
            proposition_ids=("prop-smoke",),
            relevance_keys=("smoke", "event"),
        )
    )
    reactivation = WorkspaceReactivationBoundary(canonical_store)
    return WorkspaceUpdateBoundary(intake=intake, index=index, reactivation=reactivation)


def test_workspace_update_smoke_end_to_end_is_deterministic() -> None:
    boundary = _build_boundary()

    first = boundary.update(
        WorkspaceUpdateRequest(
            observation=_build_observation("obs-smoke-1"),
            new_observations_since_last=24,
            at_task_boundary=False,
            proposition_state="accepted",
            proposition_freshness=0.80,
            reactivation_relevance_keys=("smoke",),
        )
    )
    second = boundary.update(
        WorkspaceUpdateRequest(
            observation=_build_observation("obs-smoke-2"),
            new_observations_since_last=25,
            at_task_boundary=False,
            proposition_state="accepted",
            proposition_freshness=0.20,
            reactivation_relevance_keys=("unknown-key",),
        )
    )
    duplicate = boundary.update(
        WorkspaceUpdateRequest(
            observation=_build_observation("obs-smoke-2"),
            new_observations_since_last=1,
            at_task_boundary=True,
            proposition_state="tentative",
            proposition_freshness=0.90,
            reactivation_relevance_keys=(),
        )
    )

    assert first.intake_status == "ingested"
    assert first.index_status == "indexed"
    assert first.observation_ids == ("obs-smoke-1",)
    assert first.consolidation.should_consolidate is False
    assert first.consolidation.rule_id == "consolidation.not_due"
    assert first.promotion.eligible is True
    assert first.promotion.rule_id == "promotion.eligible"
    assert first.reactivation.status == "loaded"
    assert first.reactivation.hydrated_entity_ids == ("ent-smoke",)
    assert first.reactivation.hydrated_proposition_ids == ("prop-smoke",)

    assert second.intake_status == "ingested"
    assert second.index_status == "indexed"
    assert second.observation_ids == ("obs-smoke-1", "obs-smoke-2")
    assert second.consolidation.should_consolidate is True
    assert second.consolidation.rule_id == "consolidation.cadence.25"
    assert second.promotion.eligible is False
    assert second.promotion.rule_id == "promotion.ineligible.freshness"
    assert second.reactivation.status == "no_matches"
    assert second.reactivation.rule_id == "reactivation.no_matches"

    assert duplicate.intake_status == "duplicate"
    assert duplicate.stored is False
    assert duplicate.index_status == "already_indexed"
    assert duplicate.observation_ids == ("obs-smoke-1", "obs-smoke-2")
    assert duplicate.consolidation.should_consolidate is True
    assert duplicate.consolidation.rule_id == "consolidation.task_boundary"
    assert duplicate.promotion.eligible is False
    assert duplicate.promotion.rule_id == "promotion.ineligible.state"
    assert duplicate.reactivation.status == "not_requested"
    assert duplicate.reactivation.rule_id == "reactivation.not_requested"

"""Smoke tests for deterministic composed workspace update behavior."""

from datetime import datetime

import pytest

from src.core.models import Observation
from src.store import InMemoryObservationStore
from src.workspace import (
    InMemoryWorkspaceObservationIndex,
    WorkspaceObservationIntake,
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
    return WorkspaceUpdateBoundary(intake=intake, index=index)


def test_workspace_update_smoke_end_to_end_is_deterministic() -> None:
    boundary = _build_boundary()

    first = boundary.update(
        WorkspaceUpdateRequest(
            observation=_build_observation("obs-smoke-1"),
            new_observations_since_last=24,
            at_task_boundary=False,
            proposition_state="accepted",
            proposition_freshness=0.80,
        )
    )
    second = boundary.update(
        WorkspaceUpdateRequest(
            observation=_build_observation("obs-smoke-2"),
            new_observations_since_last=25,
            at_task_boundary=False,
            proposition_state="accepted",
            proposition_freshness=0.20,
        )
    )
    duplicate = boundary.update(
        WorkspaceUpdateRequest(
            observation=_build_observation("obs-smoke-2"),
            new_observations_since_last=1,
            at_task_boundary=True,
            proposition_state="tentative",
            proposition_freshness=0.90,
        )
    )

    assert first.intake_status == "ingested"
    assert first.index_status == "indexed"
    assert first.observation_ids == ("obs-smoke-1",)
    assert first.consolidation.should_consolidate is False
    assert first.consolidation.rule_id == "consolidation.not_due"
    assert first.promotion.eligible is True
    assert first.promotion.rule_id == "promotion.eligible"

    assert second.intake_status == "ingested"
    assert second.index_status == "indexed"
    assert second.observation_ids == ("obs-smoke-1", "obs-smoke-2")
    assert second.consolidation.should_consolidate is True
    assert second.consolidation.rule_id == "consolidation.cadence.25"
    assert second.promotion.eligible is False
    assert second.promotion.rule_id == "promotion.ineligible.freshness"

    assert duplicate.intake_status == "duplicate"
    assert duplicate.stored is False
    assert duplicate.index_status == "already_indexed"
    assert duplicate.observation_ids == ("obs-smoke-1", "obs-smoke-2")
    assert duplicate.consolidation.should_consolidate is True
    assert duplicate.consolidation.rule_id == "consolidation.task_boundary"
    assert duplicate.promotion.eligible is False
    assert duplicate.promotion.rule_id == "promotion.ineligible.state"

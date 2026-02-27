"""Tests for workspace observation intake boundary."""

from datetime import datetime

from src.core.models import Observation
from src.store import InMemoryObservationStore
from src.workspace import ObservationIntakeRequest, WorkspaceObservationIntake


def _build_observation(observation_id: str) -> Observation:
    return Observation(
        observation_id=observation_id,
        timestamp=datetime(2026, 2, 27, 13, 0, 0),
        source_id="source-1",
        source_type="api",
        source_independence_group="group-a",
        session_id="session-1",
        task_id="task-1",
        raw_payload="raw",
        parsed_payload={"value": observation_id},
        ingest_status="ingested",
    )


def test_intake_ingests_observation_successfully() -> None:
    store = InMemoryObservationStore()
    intake = WorkspaceObservationIntake(store)
    observation = _build_observation("obs-intake-1")

    result = intake.ingest(ObservationIntakeRequest(observation=observation))

    assert result.observation_id == "obs-intake-1"
    assert result.status == "ingested"
    assert result.stored is True
    assert store.get_by_id("obs-intake-1") is not None


def test_intake_reports_duplicate_observation_deterministically() -> None:
    store = InMemoryObservationStore()
    intake = WorkspaceObservationIntake(store)
    observation = _build_observation("obs-intake-dup")
    store.append(observation)

    result = intake.ingest(ObservationIntakeRequest(observation=observation))

    assert result.observation_id == "obs-intake-dup"
    assert result.status == "duplicate"
    assert result.stored is False

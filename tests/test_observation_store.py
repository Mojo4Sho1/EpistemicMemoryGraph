"""Tests for observation-store interface and in-memory append-only stub."""

from datetime import datetime

import pytest

from src.core.models import Observation
from src.store import InMemoryObservationStore


def _build_observation(observation_id: str) -> Observation:
    return Observation(
        observation_id=observation_id,
        timestamp=datetime(2026, 2, 27, 12, 0, 0),
        source_id="source-1",
        source_type="api",
        source_independence_group="group-a",
        session_id="session-1",
        task_id="task-1",
        raw_payload="raw",
        parsed_payload={"value": observation_id},
        ingest_status="ingested",
    )


def test_append_and_lookup_by_id() -> None:
    store = InMemoryObservationStore()
    observation = _build_observation("obs-1")

    store.append(observation)

    loaded = store.get_by_id("obs-1")
    assert loaded is not None
    assert loaded.observation_id == "obs-1"


def test_append_rejects_duplicate_observation_id() -> None:
    store = InMemoryObservationStore()
    observation = _build_observation("obs-1")
    store.append(observation)

    with pytest.raises(ValueError):
        store.append(observation)


def test_lookup_unknown_id_returns_none() -> None:
    store = InMemoryObservationStore()
    assert store.get_by_id("missing") is None

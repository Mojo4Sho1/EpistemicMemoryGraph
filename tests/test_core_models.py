"""Tests for minimal typed v0 core model primitives."""

from datetime import datetime

import pytest

from src.core.constants import BELIEF_STATES
from src.core.models import Entity, Observation, Proposition


def test_observation_has_required_fields() -> None:
    obs = Observation(
        observation_id="obs-1",
        timestamp=datetime(2026, 2, 27, 10, 0, 0),
        source_id="source-1",
        source_type="api",
        source_independence_group="group-a",
        session_id="session-1",
        task_id="task-1",
        raw_payload="raw",
        parsed_payload={"value": "x"},
        ingest_status="ingested",
    )

    assert obs.observation_id == "obs-1"
    assert obs.source_independence_group == "group-a"
    assert obs.parsed_payload["value"] == "x"


def test_entity_supports_minimal_identity_fields() -> None:
    entity = Entity(
        entity_id="ent-1",
        canonical_name="Ada Lovelace",
        entity_type="person",
        aliases=("A. Lovelace",),
        is_canonical=True,
    )

    assert entity.canonical_name == "Ada Lovelace"
    assert entity.entity_type == "person"
    assert entity.aliases == ("A. Lovelace",)
    assert entity.is_canonical is True


def test_proposition_accepts_spec_belief_state() -> None:
    prop = Proposition(
        proposition_id="prop-1",
        text="The system uses SQLite in v0.",
        structured_form=None,
        status="tentative",
        confidence=0.4,
        support_weight=0.6,
        contradiction_weight=0.0,
        source_group_count=1,
        recency=1.0,
        volatility=0.1,
        provenance_summary="single docs source",
    )

    assert prop.status in BELIEF_STATES


def test_proposition_rejects_unknown_belief_state() -> None:
    with pytest.raises(ValueError):
        Proposition(
            proposition_id="prop-2",
            text="Invalid state example",
            structured_form=None,
            status="unknown",
            confidence=0.1,
            support_weight=0.1,
            contradiction_weight=0.0,
            source_group_count=1,
            recency=1.0,
            volatility=0.1,
            provenance_summary="test",
        )

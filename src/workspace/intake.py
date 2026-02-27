"""Minimal workspace observation-intake boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from src.core.models import Observation
from src.store import ObservationStore

IntakeStatus = Literal["ingested", "duplicate"]


@dataclass(frozen=True, slots=True)
class ObservationIntakeRequest:
    """Typed intake input for a single observation."""

    observation: Observation


@dataclass(frozen=True, slots=True)
class ObservationIntakeResult:
    """Deterministic outcome for single-observation intake."""

    observation_id: str
    status: IntakeStatus
    stored: bool


class WorkspaceObservationIntake:
    """Minimal boundary that records observations through the store interface."""

    def __init__(self, store: ObservationStore) -> None:
        self._store = store

    def ingest(self, request: ObservationIntakeRequest) -> ObservationIntakeResult:
        observation = request.observation
        try:
            self._store.append(observation)
            return ObservationIntakeResult(
                observation_id=observation.observation_id,
                status="ingested",
                stored=True,
            )
        except ValueError:
            if self._store.get_by_id(observation.observation_id) is None:
                msg = f"Duplicate intake reported but not found: {observation.observation_id}"
                raise RuntimeError(msg) from None
            return ObservationIntakeResult(
                observation_id=observation.observation_id,
                status="duplicate",
                stored=False,
            )

"""Observation store interfaces and an in-memory append-only stub."""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.core.models import Observation


class ObservationStore(ABC):
    """Minimal persistence boundary for append and lookup by id."""

    @abstractmethod
    def append(self, observation: Observation) -> None:
        """Append an observation to the store."""

    @abstractmethod
    def get_by_id(self, observation_id: str) -> Observation | None:
        """Return an observation by id if present."""


class InMemoryObservationStore(ObservationStore):
    """Test-oriented in-memory append-only observation store."""

    def __init__(self) -> None:
        self._items: dict[str, Observation] = {}

    def append(self, observation: Observation) -> None:
        if observation.observation_id in self._items:
            msg = f"Observation already exists: {observation.observation_id}"
            raise ValueError(msg)
        self._items[observation.observation_id] = observation

    def get_by_id(self, observation_id: str) -> Observation | None:
        return self._items.get(observation_id)

"""Minimal in-memory workspace state for session/task observation indexing."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ObservationIndexRegisterRequest:
    """Typed request for recording an observation id under a session/task key."""

    session_id: str
    task_id: str
    observation_id: str


@dataclass(frozen=True, slots=True)
class ObservationIndexRegisterResult:
    """Deterministic result snapshot after index registration."""

    session_id: str
    task_id: str
    observation_ids: tuple[str, ...]


class InMemoryWorkspaceObservationIndex:
    """In-memory append-only index of observation ids by session/task."""

    def __init__(self) -> None:
        self._index: dict[tuple[str, str], list[str]] = {}

    def register(
        self, request: ObservationIndexRegisterRequest
    ) -> ObservationIndexRegisterResult:
        key = (request.session_id, request.task_id)
        observation_ids = self._index.setdefault(key, [])
        observation_ids.append(request.observation_id)
        return ObservationIndexRegisterResult(
            session_id=request.session_id,
            task_id=request.task_id,
            observation_ids=tuple(observation_ids),
        )

    def get_observation_ids(self, session_id: str, task_id: str) -> tuple[str, ...]:
        """Return a deterministic ordered snapshot for a session/task key."""

        return tuple(self._index.get((session_id, task_id), []))

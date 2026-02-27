"""Tests for minimal workspace session/task observation indexing."""

from src.workspace import (
    InMemoryWorkspaceObservationIndex,
    ObservationIndexRegisterRequest,
)


def test_register_initializes_key_with_first_observation_id() -> None:
    index = InMemoryWorkspaceObservationIndex()

    result = index.register(
        ObservationIndexRegisterRequest(
            session_id="session-1",
            task_id="task-1",
            observation_id="obs-1",
        )
    )

    assert result.session_id == "session-1"
    assert result.task_id == "task-1"
    assert result.observation_ids == ("obs-1",)
    assert index.get_observation_ids("session-1", "task-1") == ("obs-1",)


def test_register_appends_observations_for_repeated_session_task_key() -> None:
    index = InMemoryWorkspaceObservationIndex()
    first = ObservationIndexRegisterRequest(
        session_id="session-1",
        task_id="task-1",
        observation_id="obs-1",
    )
    second = ObservationIndexRegisterRequest(
        session_id="session-1",
        task_id="task-1",
        observation_id="obs-2",
    )

    first_result = index.register(first)
    second_result = index.register(second)

    assert first_result.observation_ids == ("obs-1",)
    assert second_result.observation_ids == ("obs-1", "obs-2")
    assert index.get_observation_ids("session-1", "task-1") == ("obs-1", "obs-2")

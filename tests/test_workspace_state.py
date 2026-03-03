"""Tests for minimal workspace session/task observation indexing."""

from src.store import CanonicalMemoryNode, InMemoryCanonicalMemoryStore
from src.workspace import (
    InMemoryWorkspaceObservationIndex,
    ObservationIndexRegisterRequest,
    ReactivationRequest,
    WorkspaceReactivationBoundary,
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


def test_reactivation_returns_not_requested_without_relevance_keys() -> None:
    boundary = WorkspaceReactivationBoundary(InMemoryCanonicalMemoryStore())

    result = boundary.reactivate(
        ReactivationRequest(
            session_id="session-1",
            task_id="task-1",
            relevance_keys=(),
        )
    )

    assert result.status == "not_requested"
    assert result.canonical_nodes == ()
    assert result.rule_id == "reactivation.not_requested"


def test_reactivation_loads_ranked_relevant_nodes_with_session_task_scope() -> None:
    store = InMemoryCanonicalMemoryStore()
    store.append_node(
        CanonicalMemoryNode(
            node_id="node-1",
            session_id="session-1",
            task_id="task-1",
            entity_ids=("ent-1",),
            proposition_ids=("prop-1",),
            relevance_keys=("Ada", "Math"),
        )
    )
    store.append_node(
        CanonicalMemoryNode(
            node_id="node-2",
            session_id="session-1",
            task_id="task-1",
            entity_ids=("ent-2",),
            proposition_ids=("prop-2",),
            relevance_keys=("math",),
        )
    )
    store.append_node(
        CanonicalMemoryNode(
            node_id="node-out-of-scope",
            session_id="session-2",
            task_id="task-1",
            entity_ids=("ent-x",),
            proposition_ids=("prop-x",),
            relevance_keys=("ada", "math"),
        )
    )
    boundary = WorkspaceReactivationBoundary(store)

    result = boundary.reactivate(
        ReactivationRequest(
            session_id="session-1",
            task_id="task-1",
            relevance_keys=("ada", "math"),
            limit=2,
        )
    )

    assert result.status == "loaded"
    assert tuple(node.node_id for node in result.canonical_nodes) == ("node-1", "node-2")
    assert result.hydrated_entity_ids == ("ent-1", "ent-2")
    assert result.hydrated_proposition_ids == ("prop-1", "prop-2")
    assert result.rule_id == "reactivation.loaded_relevant_subgraph"

"""Workspace package for transient epistemic state handling."""

from src.workspace.intake import (
    ObservationIntakeRequest,
    ObservationIntakeResult,
    WorkspaceObservationIntake,
)
from src.workspace.state import (
    InMemoryWorkspaceObservationIndex,
    ObservationIndexRegisterRequest,
    ObservationIndexRegisterResult,
)

__all__ = [
    "ObservationIntakeRequest",
    "ObservationIntakeResult",
    "ObservationIndexRegisterRequest",
    "ObservationIndexRegisterResult",
    "InMemoryWorkspaceObservationIndex",
    "WorkspaceObservationIntake",
]

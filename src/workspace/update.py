"""Composed deterministic workspace update boundary for v0.1q."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from src.core.models import Observation
from src.workspace.consolidation import (
    ConsolidationDecision,
    PromotionDecision,
    evaluate_promotion_eligibility,
    should_run_consolidation,
)
from src.workspace.intake import (
    IntakeStatus,
    ObservationIntakeRequest,
    WorkspaceObservationIntake,
)
from src.workspace.state import (
    InMemoryWorkspaceObservationIndex,
    ObservationIndexRegisterRequest,
)

IndexUpdateStatus = Literal["indexed", "already_indexed"]


@dataclass(frozen=True, slots=True)
class WorkspaceUpdateRequest:
    """Typed request for one composed workspace update call."""

    observation: Observation
    new_observations_since_last: int
    at_task_boundary: bool
    proposition_state: str
    proposition_freshness: float


@dataclass(frozen=True, slots=True)
class WorkspaceUpdateResult:
    """Deterministic composed update result across intake/index/gating."""

    observation_id: str
    session_id: str
    task_id: str
    intake_status: IntakeStatus
    stored: bool
    index_status: IndexUpdateStatus
    observation_ids: tuple[str, ...]
    consolidation: ConsolidationDecision
    promotion: PromotionDecision


class WorkspaceUpdateBoundary:
    """Compose intake + session/task indexing + policy gate metadata."""

    def __init__(
        self,
        *,
        intake: WorkspaceObservationIntake,
        index: InMemoryWorkspaceObservationIndex,
    ) -> None:
        self._intake = intake
        self._index = index

    def update(self, request: WorkspaceUpdateRequest) -> WorkspaceUpdateResult:
        """Apply one deterministic workspace update for a single observation."""

        if request.new_observations_since_last < 0:
            msg = "new_observations_since_last must be >= 0"
            raise ValueError(msg)

        observation = request.observation
        intake_result = self._intake.ingest(ObservationIntakeRequest(observation=observation))
        current_observation_ids = self._index.get_observation_ids(
            observation.session_id, observation.task_id
        )

        if observation.observation_id in current_observation_ids:
            index_status: IndexUpdateStatus = "already_indexed"
            observation_ids = current_observation_ids
        else:
            register_result = self._index.register(
                ObservationIndexRegisterRequest(
                    session_id=observation.session_id,
                    task_id=observation.task_id,
                    observation_id=observation.observation_id,
                )
            )
            index_status = "indexed"
            observation_ids = register_result.observation_ids

        consolidation = should_run_consolidation(
            new_observations_since_last=request.new_observations_since_last,
            at_task_boundary=request.at_task_boundary,
        )
        promotion = evaluate_promotion_eligibility(
            proposition_state=request.proposition_state,
            freshness=request.proposition_freshness,
        )

        return WorkspaceUpdateResult(
            observation_id=observation.observation_id,
            session_id=observation.session_id,
            task_id=observation.task_id,
            intake_status=intake_result.status,
            stored=intake_result.stored,
            index_status=index_status,
            observation_ids=observation_ids,
            consolidation=consolidation,
            promotion=promotion,
        )

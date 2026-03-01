"""Deterministic probe for one composed workspace update scenario."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.models import Observation
from src.store import InMemoryObservationStore
from src.workspace import (
    InMemoryWorkspaceObservationIndex,
    WorkspaceObservationIntake,
    WorkspaceUpdateBoundary,
    WorkspaceUpdateRequest,
)


def _build_observation() -> Observation:
    return Observation(
        observation_id="obs-probe-1",
        timestamp=datetime(2026, 2, 28, 13, 0, 0),
        source_id="probe-source",
        source_type="api",
        source_independence_group="probe-group",
        session_id="probe-session",
        task_id="probe-task",
        raw_payload='{"message":"probe"}',
        parsed_payload={"kind": "probe", "value": 1},
        ingest_status="ingested",
    )


def _build_boundary() -> WorkspaceUpdateBoundary:
    intake = WorkspaceObservationIntake(InMemoryObservationStore())
    index = InMemoryWorkspaceObservationIndex()
    return WorkspaceUpdateBoundary(intake=intake, index=index)


def _request_payload(request: WorkspaceUpdateRequest) -> dict[str, Any]:
    return {
        "observation_id": request.observation.observation_id,
        "timestamp": request.observation.timestamp.isoformat(),
        "session_id": request.observation.session_id,
        "task_id": request.observation.task_id,
        "new_observations_since_last": request.new_observations_since_last,
        "at_task_boundary": request.at_task_boundary,
        "proposition_state": request.proposition_state,
        "proposition_freshness": request.proposition_freshness,
    }


def main() -> None:
    boundary = _build_boundary()
    request = WorkspaceUpdateRequest(
        observation=_build_observation(),
        new_observations_since_last=25,
        at_task_boundary=False,
        proposition_state="accepted",
        proposition_freshness=0.50,
    )
    result = boundary.update(request)

    payload = {
        "probe_id": "workspace_update_probe_v0q",
        "request": _request_payload(request),
        "result": {
            "observation_id": result.observation_id,
            "session_id": result.session_id,
            "task_id": result.task_id,
            "intake_status": result.intake_status,
            "stored": result.stored,
            "index_status": result.index_status,
            "observation_ids": list(result.observation_ids),
            "consolidation": {
                "should_consolidate": result.consolidation.should_consolidate,
                "rule_id": result.consolidation.rule_id,
                "reason": result.consolidation.reason,
            },
            "promotion": {
                "eligible": result.promotion.eligible,
                "rule_id": result.promotion.rule_id,
                "reason": result.promotion.reason,
            },
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

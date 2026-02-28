"""Tool proposal validation schema and deterministic rejection codes for v0.1q."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Literal

ToolName = Literal[
    "record_observation",
    "create_or_link_entity_candidate",
    "propose_proposition",
    "attach_support",
    "attach_contradiction",
    "propose_test",
    "execute_test_result_ingest",
    "request_consolidation",
    "archive_episode",
]

ALLOWED_TOOL_NAMES: tuple[str, ...] = (
    "record_observation",
    "create_or_link_entity_candidate",
    "propose_proposition",
    "attach_support",
    "attach_contradiction",
    "propose_test",
    "execute_test_result_ingest",
    "request_consolidation",
    "archive_episode",
)


class ProposalRejectionCode(str, Enum):
    """Fixed enum contract for deterministic proposal rejection semantics."""

    INVALID_TOOL_NAME = "INVALID_TOOL_NAME"
    INVALID_PAYLOAD = "INVALID_PAYLOAD"
    MISSING_PROVENANCE = "MISSING_PROVENANCE"
    POLICY_VIOLATION = "POLICY_VIOLATION"
    DIRECT_CANONICAL_WRITE_FORBIDDEN = "DIRECT_CANONICAL_WRITE_FORBIDDEN"


@dataclass(frozen=True, slots=True)
class ToolProposal:
    """Schema for LLM-issued tool proposals before policy validation."""

    tool_name: str
    payload: dict[str, Any]


@dataclass(frozen=True, slots=True)
class ToolRejection:
    """Deterministic rejection payload exposed to runtime/orchestrator layers."""

    code: ProposalRejectionCode
    reason: str


@dataclass(frozen=True, slots=True)
class ToolValidationResult:
    """Normalized validation result for proposal-only tool boundaries."""

    status: Literal["accepted", "rejected", "transformed"]
    proposal: ToolProposal | None
    rejection: ToolRejection | None


def validate_tool_proposal(proposal: ToolProposal) -> ToolValidationResult:
    """Apply minimal deterministic schema checks for v0.1q proposal handling."""

    if proposal.tool_name not in ALLOWED_TOOL_NAMES:
        return ToolValidationResult(
            status="rejected",
            proposal=None,
            rejection=ToolRejection(
                code=ProposalRejectionCode.INVALID_TOOL_NAME,
                reason=f"Unsupported tool: {proposal.tool_name}",
            ),
        )

    if not isinstance(proposal.payload, dict):
        return ToolValidationResult(
            status="rejected",
            proposal=None,
            rejection=ToolRejection(
                code=ProposalRejectionCode.INVALID_PAYLOAD,
                reason="Tool payload must be an object.",
            ),
        )

    if proposal.tool_name == "record_observation" and "observation_id" not in proposal.payload:
        return ToolValidationResult(
            status="rejected",
            proposal=None,
            rejection=ToolRejection(
                code=ProposalRejectionCode.MISSING_PROVENANCE,
                reason="record_observation requires observation_id provenance anchor.",
            ),
        )

    if (
        proposal.tool_name == "request_consolidation"
        and proposal.payload.get("direct_write") is True
    ):
        return ToolValidationResult(
            status="rejected",
            proposal=None,
            rejection=ToolRejection(
                code=ProposalRejectionCode.DIRECT_CANONICAL_WRITE_FORBIDDEN,
                reason="Direct canonical writes are not permitted by tool proposals.",
            ),
        )

    normalized_payload = dict(sorted(proposal.payload.items(), key=lambda item: item[0]))
    normalized_proposal = ToolProposal(tool_name=proposal.tool_name, payload=normalized_payload)

    if tuple(normalized_payload.keys()) != tuple(proposal.payload.keys()):
        return ToolValidationResult(
            status="transformed",
            proposal=normalized_proposal,
            rejection=None,
        )

    return ToolValidationResult(status="accepted", proposal=proposal, rejection=None)

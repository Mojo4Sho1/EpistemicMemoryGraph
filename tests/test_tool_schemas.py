"""Tests for v0.1q tool proposal schema validation and rejection codes."""

from src.tools import (
    ProposalRejectionCode,
    ToolProposal,
    validate_tool_proposal,
)


def test_rejects_unknown_tool_name_with_fixed_code() -> None:
    result = validate_tool_proposal(ToolProposal(tool_name="unknown_tool", payload={}))

    assert result.status == "rejected"
    assert result.rejection is not None
    assert result.rejection.code == ProposalRejectionCode.INVALID_TOOL_NAME


def test_rejects_record_observation_without_provenance_anchor() -> None:
    result = validate_tool_proposal(
        ToolProposal(tool_name="record_observation", payload={"source": "x"})
    )

    assert result.status == "rejected"
    assert result.rejection is not None
    assert result.rejection.code == ProposalRejectionCode.MISSING_PROVENANCE


def test_rejects_direct_write_request_on_consolidation_tool() -> None:
    result = validate_tool_proposal(
        ToolProposal(
            tool_name="request_consolidation",
            payload={"direct_write": True},
        )
    )

    assert result.status == "rejected"
    assert result.rejection is not None
    assert result.rejection.code == ProposalRejectionCode.DIRECT_CANONICAL_WRITE_FORBIDDEN


def test_transforms_payload_to_deterministic_key_order() -> None:
    result = validate_tool_proposal(
        ToolProposal(
            tool_name="attach_support",
            payload={"z": 1, "a": 2},
        )
    )

    assert result.status == "transformed"
    assert result.proposal is not None
    assert tuple(result.proposal.payload.keys()) == ("a", "z")


def test_accepts_valid_observation_tool_proposal() -> None:
    result = validate_tool_proposal(
        ToolProposal(
            tool_name="record_observation",
            payload={"observation_id": "obs-1"},
        )
    )

    assert result.status == "accepted"
    assert result.rejection is None


def test_rejection_code_enum_is_stable() -> None:
    expected = {
        "INVALID_TOOL_NAME",
        "INVALID_PAYLOAD",
        "MISSING_PROVENANCE",
        "POLICY_VIOLATION",
        "DIRECT_CANONICAL_WRITE_FORBIDDEN",
    }

    assert {code.value for code in ProposalRejectionCode} == expected

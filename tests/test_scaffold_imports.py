"""Scaffold-level tests for initial constants and import wiring."""

from src.core.constants import BELIEF_STATES, EDGE_TYPES


def test_belief_states_match_spec_exactly() -> None:
    expected = {
        "tentative",
        "provisional",
        "accepted",
        "contested",
        "deprecated",
        "rejected",
    }
    assert set(BELIEF_STATES) == expected


def test_edge_types_match_spec_exactly() -> None:
    expected = {
        "supports",
        "contradicts",
        "about",
        "predicts",
        "tested_by",
        "derived_from",
        "possible_same_as",
        "supersedes",
    }
    assert set(EDGE_TYPES) == expected

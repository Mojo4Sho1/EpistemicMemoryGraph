"""v0 scaffold constants aligned with frozen memory-governance specs.

These constants are placeholders for early bootstrap wiring and should stay
strictly aligned with the documented v0 belief-state and edge-type sets.
"""

BELIEF_STATES = (
    "tentative",
    "provisional",
    "accepted",
    "contested",
    "deprecated",
    "rejected",
)

# Alias links are maintained as table-level identity mappings while
# `possible_same_as` is the explicit graph-level ambiguity edge.
IDENTITY_LINK_TYPES = (
    "alias",
    "possible_same_as",
)

EDGE_TYPES = (
    "supports",
    "contradicts",
    "about",
    "predicts",
    "tested_by",
    "derived_from",
    "possible_same_as",
    "supersedes",
)

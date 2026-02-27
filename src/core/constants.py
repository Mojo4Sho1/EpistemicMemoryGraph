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

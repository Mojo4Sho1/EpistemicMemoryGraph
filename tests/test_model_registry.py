"""Tests for internal model-id to served-name alias mapping."""

from __future__ import annotations

from src.eval import (
    ModelAliasError,
    get_phase2_model_ids,
    get_runtime_model_aliases,
    resolve_served_model_name,
)


def _eval_config() -> dict[str, object]:
    return {
        "phase2": {
            "model_panel": [
                {"model_id": "meta_llama3.2_1b_instruct"},
                {"model_id": "google_gemma3_1b"},
                {"model_id": "microsoft_phi4_mini"},
            ]
        },
        "runtime": {
            "model_id_aliases": {
                "meta_llama3.2_1b_instruct": "llama3.2:1b",
                "google_gemma3_1b": "gemma3:1b",
                "microsoft_phi4_mini": "phi4-mini",
            }
        },
    }


def test_get_phase2_model_ids_returns_ordered_ids() -> None:
    ids = get_phase2_model_ids(_eval_config())
    assert ids == (
        "meta_llama3.2_1b_instruct",
        "google_gemma3_1b",
        "microsoft_phi4_mini",
    )


def test_resolve_served_model_name_uses_alias_map() -> None:
    aliases = get_runtime_model_aliases(_eval_config())
    assert (
        resolve_served_model_name(
            internal_model_id="meta_llama3.2_1b_instruct",
            model_aliases=aliases,
            strict=True,
        )
        == "llama3.2:1b"
    )


def test_resolve_served_model_name_raises_when_missing_in_strict_mode() -> None:
    aliases = get_runtime_model_aliases(_eval_config())
    try:
        resolve_served_model_name(
            internal_model_id="unknown_model",
            model_aliases=aliases,
            strict=True,
        )
    except ModelAliasError:
        pass
    else:
        raise AssertionError("Expected ModelAliasError for missing alias in strict mode.")

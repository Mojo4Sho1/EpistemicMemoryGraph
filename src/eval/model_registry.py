"""Model alias mapping helpers for OpenAI-compatible runtime calls."""

from __future__ import annotations

from typing import Any, Mapping


class ModelAliasError(ValueError):
    """Raised when an internal model id cannot be mapped to a served model name."""


def get_runtime_model_aliases(eval_config: Mapping[str, Any]) -> dict[str, str]:
    """Extract internal-id -> served-model alias map from eval config."""

    runtime = eval_config.get("runtime", {})
    aliases = runtime.get("model_id_aliases", {})
    if not isinstance(aliases, dict):
        raise ModelAliasError("`runtime.model_id_aliases` must be a mapping.")
    normalized: dict[str, str] = {}
    for internal_id, served_name in aliases.items():
        if not isinstance(internal_id, str) or not isinstance(served_name, str):
            raise ModelAliasError("Model alias entries must map string -> string.")
        normalized[internal_id] = served_name
    return normalized


def resolve_served_model_name(
    *, internal_model_id: str, model_aliases: Mapping[str, str], strict: bool = True
) -> str:
    """Resolve one internal model id to an endpoint-served model name."""

    if internal_model_id in model_aliases:
        return model_aliases[internal_model_id]
    if strict:
        raise ModelAliasError(f"No runtime alias found for internal model id: {internal_model_id}")
    return internal_model_id


def get_phase2_model_ids(eval_config: Mapping[str, Any]) -> tuple[str, ...]:
    """Return ordered Phase 2 internal model ids from config."""

    phase2 = eval_config.get("phase2", {})
    model_panel = phase2.get("model_panel", ())
    if not isinstance(model_panel, list):
        raise ModelAliasError("`phase2.model_panel` must be a list.")
    ids: list[str] = []
    for model in model_panel:
        if not isinstance(model, dict):
            raise ModelAliasError("Each phase2 model_panel entry must be a mapping.")
        model_id = model.get("model_id")
        if not isinstance(model_id, str):
            raise ModelAliasError("Each phase2 model_panel entry must define string `model_id`.")
        ids.append(model_id)
    return tuple(ids)

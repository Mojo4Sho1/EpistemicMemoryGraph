"""Preflight probe for local Ollama OpenAI-compatible model serving."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

import yaml
from openai import OpenAI

from src.eval.model_registry import (
    get_phase2_model_ids,
    get_runtime_model_aliases,
    resolve_served_model_name,
)


def _load_eval_config(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Config must parse to a mapping: {path}")
    return payload


def _build_client(eval_config: dict[str, Any]) -> OpenAI:
    runtime_cfg = eval_config["runtime"]["openai_compatible"]
    api_key = os.getenv(runtime_cfg["api_key_env"], runtime_cfg["api_key_fallback"])
    return OpenAI(
        base_url=runtime_cfg["base_url"],
        api_key=api_key,
        timeout=float(runtime_cfg["timeout_seconds"]),
    )


def _probe_models(*, client: OpenAI, models: tuple[str, ...], max_tokens: int) -> None:
    for model_name in models:
        response = client.chat.completions.create(
            model=model_name,
            temperature=0.0,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": "Reply with exactly: preflight_ok"}],
        )
        content = response.choices[0].message.content or ""
        print(f"[ok] {model_name}: {content.strip()!r}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Probe local Ollama OpenAI-compatible endpoint and mapped Phase 2 models."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/eval_v0q.yaml"),
        help="Path to eval config file (default: configs/eval_v0q.yaml).",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=16,
        help="Max tokens for preflight completion checks (default: 16).",
    )
    args = parser.parse_args()

    eval_config = _load_eval_config(args.config)
    model_aliases = get_runtime_model_aliases(eval_config)
    phase2_internal_ids = get_phase2_model_ids(eval_config)
    served_model_names = tuple(
        resolve_served_model_name(
            internal_model_id=internal_id,
            model_aliases=model_aliases,
            strict=True,
        )
        for internal_id in phase2_internal_ids
    )

    client = _build_client(eval_config)
    available = client.models.list()
    available_names = {item.id for item in available.data}
    missing = tuple(name for name in served_model_names if name not in available_names)
    if missing:
        raise RuntimeError(
            "Missing mapped Ollama models on OpenAI-compatible endpoint: " f"{missing}"
        )

    print(f"[ok] endpoint reachable: {eval_config['runtime']['openai_compatible']['base_url']}")
    print(f"[ok] mapped models present: {served_model_names}")
    _probe_models(client=client, models=served_model_names, max_tokens=args.max_tokens)


if __name__ == "__main__":
    main()

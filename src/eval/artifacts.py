"""Artifact writing and reproducibility hashing helpers for v0.1q runs."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from src.eval.schemas import (
    AggregateMetrics,
    ConsolidationEvent,
    RunManifest,
    ScenarioResult,
    TransitionEvent,
)


def write_run_artifacts(
    *,
    artifacts_root: Path,
    run_date: datetime,
    git_sha: str,
    system: str,
    seed: int,
    model_id: str,
    config_snapshot: dict[str, Any],
    scenario_bundle: dict[str, Any],
    transitions: Iterable[TransitionEvent],
    consolidation_events: Iterable[ConsolidationEvent],
    scenario_results: Iterable[ScenarioResult],
    metrics_summary: AggregateMetrics,
) -> Path:
    """Write required artifact files and return created run directory."""

    run_dir = artifacts_root / build_run_directory_name(
        run_date=run_date,
        git_sha=git_sha,
        system=system,
        seed=seed,
    )
    run_dir.mkdir(parents=True, exist_ok=True)

    config_hash = stable_hash(config_snapshot)
    scenario_bundle_hash = stable_hash(scenario_bundle)
    reproducibility_hash = stable_hash(
        {
            "config_hash": config_hash,
            "scenario_bundle_hash": scenario_bundle_hash,
        }
    )

    manifest = RunManifest(
        model_id=model_id,
        git_sha=git_sha,
        system=system,
        seed=seed,
        timestamp_utc=run_date.replace(microsecond=0).isoformat() + "Z",
        config_hash=config_hash,
        scenario_bundle_hash=scenario_bundle_hash,
        reproducibility_hash=reproducibility_hash,
    )

    _write_json(run_dir / "manifest.json", manifest.to_dict())
    _write_yaml_like(run_dir / "config_snapshot.yaml", config_snapshot)
    _write_jsonl(run_dir / "transitions.jsonl", (item.to_dict() for item in transitions))
    _write_jsonl(
        run_dir / "consolidation_events.jsonl",
        (item.to_dict() for item in consolidation_events),
    )
    _write_jsonl(
        run_dir / "scenario_results.jsonl",
        (item.to_dict() for item in scenario_results),
    )
    _write_json(run_dir / "metrics_summary.json", metrics_summary.to_dict())

    return run_dir


def build_run_directory_name(
    *,
    run_date: datetime,
    git_sha: str,
    system: str,
    seed: int,
) -> str:
    """Build deterministic directory name: {date}_{git_sha}_{system}_{seed}."""

    date_part = run_date.strftime("%Y-%m-%d")
    short_sha = git_sha[:8]
    return f"{date_part}_{short_sha}_{system}_{seed}"


def stable_hash(payload: Any) -> str:
    """Compute stable SHA-256 hash over canonical JSON form of payload."""

    normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    lines = [json.dumps(row, sort_keys=True) for row in rows]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def _write_yaml_like(path: Path, payload: dict[str, Any]) -> None:
    lines = ["---"]
    lines.extend(_yaml_lines(payload, indent=0))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _yaml_lines(value: Any, *, indent: int) -> list[str]:
    prefix = " " * indent
    if isinstance(value, dict):
        lines: list[str] = []
        for key, item in value.items():
            if _is_scalar(item):
                lines.append(f"{prefix}{key}: {_yaml_scalar(item)}")
            else:
                lines.append(f"{prefix}{key}:")
                lines.extend(_yaml_lines(item, indent=indent + 2))
        return lines

    if isinstance(value, list):
        lines = []
        for item in value:
            if _is_scalar(item):
                lines.append(f"{prefix}- {_yaml_scalar(item)}")
            else:
                lines.append(f"{prefix}-")
                lines.extend(_yaml_lines(item, indent=indent + 2))
        return lines

    return [f"{prefix}{_yaml_scalar(value)}"]


def _is_scalar(value: Any) -> bool:
    return isinstance(value, (str, int, float, bool)) or value is None


def _yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    escaped = str(value).replace('"', '\\"')
    return f'"{escaped}"'

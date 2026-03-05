"""Phase 2 findings summary rendering helpers."""

from __future__ import annotations

import json
from pathlib import Path

from src.eval.schemas import FindingsSummary


def render_findings_summary_markdown(summary: FindingsSummary) -> str:
    """Render deterministic markdown summary for one experiment bundle."""

    lines = [
        f"# Findings Summary ({summary.phase_id})",
        "",
        "## Metadata",
        f"- Phase ID: `{summary.phase_id}`",
        f"- Stage ID: `{summary.stage_id}`",
        f"- Model ID: `{summary.model_id}`",
        f"- Task Families: {', '.join(summary.task_families)}",
        f"- Decision Gate Status: `{summary.decision_gate_status}`",
        "",
        "## Results",
        "| Metric | Delta | CI Low | CI High | p-value | Effect Size | Passed |",
        "| --- | ---: | ---: | ---: | ---: | ---: | :---: |",
    ]
    for result in summary.key_results:
        lines.append(
            "| "
            f"{result.metric_name} | {result.delta:.6f} | {result.ci_low:.6f} | "
            f"{result.ci_high:.6f} | {result.p_value:.6f} | {result.effect_size:.6f} | "
            f"{'YES' if result.passed else 'NO'} |"
        )

    lines.extend(
        [
            "",
            "## Failure Slices",
            "- Pending deeper slice taxonomy in subsequent evaluation loops.",
            "",
            "## Caveats",
        ]
    )
    for caveat in summary.caveats:
        lines.append(f"- {caveat}")

    lines.extend(
        [
            "",
            "## Interpretation",
            summary.interpretation,
            "",
        ]
    )
    return "\n".join(lines)


def write_findings_summary(*, output_dir: Path, summary: FindingsSummary) -> tuple[Path, Path]:
    """Write machine-readable and markdown findings summary artifacts."""

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "findings_summary.json"
    md_path = output_dir / "findings_summary.md"

    json_path.write_text(
        json.dumps(summary.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(render_findings_summary_markdown(summary), encoding="utf-8")
    return (json_path, md_path)

"""Deterministic probe for Stage 4 long-horizon interpretable-benefit workflow."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.eval import (
    LongHorizonStudyHarness,
    LongHorizonTaskFamily,
    evaluate_stage4_interpretable_benefit,
)
from src.eval.fairness import BaselineRunSpec


def _run_spec() -> BaselineRunSpec:
    return BaselineRunSpec(
        model_snapshot="model-locked",
        prompt_template_family="default-v1",
        tool_availability=("record_observation", "request_consolidation"),
        token_budget=4096,
        wall_clock_timeout_seconds=120,
        seed_set=(101, 202, 303, 404, 505),
    )


def main() -> int:
    task_families = (
        LongHorizonTaskFamily(
            family_id="policy-debug",
            description="Repeated policy-sensitive debugging steps.",
            governance_baseline=0.34,
            governance_governed=0.24,
            continuity_baseline=0.62,
            continuity_governed=0.76,
        ),
        LongHorizonTaskFamily(
            family_id="identity-reconciliation",
            description="Entity resolution over long dialogue turns.",
            governance_baseline=0.18,
            governance_governed=0.17,
            continuity_baseline=0.70,
            continuity_governed=0.69,
        ),
    )

    harness = LongHorizonStudyHarness()
    records = harness.run_stage4(
        artifacts_root=Path("artifacts"),
        run_date=datetime(2026, 3, 5, 9, 0, 0),
        git_sha="abcdef1234567890",
        model_id="model-governed",
        seeds=(101,),
        run_specs={
            "raw_text_log_retrieval": _run_spec(),
            "full_governed_system": _run_spec(),
        },
        config_snapshot={"eval": {"stage": "long_horizon"}},
        task_families=task_families,
    )
    result = evaluate_stage4_interpretable_benefit(task_families=task_families)

    payload = {
        "run_count": len(records),
        "task_families_with_paired_improvement": list(
            result.task_families_with_paired_improvement
        ),
        "interpretable_benefit_passed": result.interpretable_benefit_passed,
    }
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

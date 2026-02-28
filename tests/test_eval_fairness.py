"""Tests for baseline fairness preflight checks."""

from src.eval import BaselineRunSpec, check_baseline_fairness


def _spec(*, token_budget: int = 4096) -> BaselineRunSpec:
    return BaselineRunSpec(
        model_snapshot="model-locked",
        prompt_template_family="default-v1",
        tool_availability=("record_observation", "request_consolidation"),
        token_budget=token_budget,
        wall_clock_timeout_seconds=120,
        seed_set=(101, 202, 303, 404, 505),
    )


def test_fairness_passes_when_specs_match() -> None:
    result = check_baseline_fairness(
        {
            "raw_log": _spec(),
            "governed": _spec(),
        }
    )

    assert result.passed is True
    assert result.violations == ()


def test_fairness_fails_when_token_budget_differs() -> None:
    result = check_baseline_fairness(
        {
            "raw_log": _spec(token_budget=2048),
            "governed": _spec(token_budget=4096),
        }
    )

    assert result.passed is False
    assert any("token_budget" in violation for violation in result.violations)

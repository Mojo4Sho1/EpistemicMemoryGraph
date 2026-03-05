"""Deterministic statistical helpers for Phase 2 small/edge uplift analysis."""

from __future__ import annotations

from math import comb
from random import Random

from src.eval.schemas import StatisticalResult


def bootstrap_ci(
    values: tuple[float, ...],
    *,
    confidence_level: float = 0.95,
    n_resamples: int = 2000,
    seed: int = 0,
) -> tuple[float, float]:
    """Compute deterministic percentile bootstrap CI for the sample mean."""

    if not values:
        raise ValueError("bootstrap_ci requires at least one value")
    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level must be between 0 and 1")
    if n_resamples <= 0:
        raise ValueError("n_resamples must be positive")

    rng = Random(seed)
    n = len(values)
    boot_means: list[float] = []
    for _ in range(n_resamples):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        boot_means.append(sum(sample) / n)
    boot_means.sort()

    alpha = 1.0 - confidence_level
    lower_index = int((alpha / 2.0) * (n_resamples - 1))
    upper_index = int((1.0 - alpha / 2.0) * (n_resamples - 1))
    return (round(boot_means[lower_index], 6), round(boot_means[upper_index], 6))


def paired_permutation_pvalue(
    *,
    baseline_values: tuple[float, ...],
    governed_values: tuple[float, ...],
    lower_is_better: bool,
    n_resamples: int = 20000,
    exact_limit: int = 16,
    seed: int = 0,
) -> float:
    """Compute a two-sided paired sign-flip permutation p-value for mean deltas."""

    if len(baseline_values) != len(governed_values):
        raise ValueError("baseline_values and governed_values must have the same length")
    if not baseline_values:
        raise ValueError("paired_permutation_pvalue requires at least one pair")

    deltas = _paired_deltas(
        baseline_values=baseline_values,
        governed_values=governed_values,
        lower_is_better=lower_is_better,
    )
    observed = abs(sum(deltas) / len(deltas))
    n = len(deltas)

    if n <= exact_limit:
        total = 2**n
        extreme = 0
        for mask in range(total):
            signed = [(-delta if (mask >> i) & 1 else delta) for i, delta in enumerate(deltas)]
            if abs(sum(signed) / n) >= observed:
                extreme += 1
        return round(extreme / total, 6)

    rng = Random(seed)
    extreme = 0
    for _ in range(n_resamples):
        signed = [delta if rng.random() < 0.5 else -delta for delta in deltas]
        if abs(sum(signed) / n) >= observed:
            extreme += 1
    return round(extreme / n_resamples, 6)


def effect_size_cohens_dz(
    *,
    baseline_values: tuple[float, ...],
    governed_values: tuple[float, ...],
    lower_is_better: bool,
) -> float:
    """Compute paired-sample Cohen's dz effect size for oriented deltas."""

    deltas = _paired_deltas(
        baseline_values=baseline_values,
        governed_values=governed_values,
        lower_is_better=lower_is_better,
    )
    n = len(deltas)
    mean_delta = sum(deltas) / n
    if n == 1:
        return round(mean_delta, 6)

    variance = sum((delta - mean_delta) ** 2 for delta in deltas) / (n - 1)
    std = variance**0.5
    if std == 0:
        return 0.0
    return round(mean_delta / std, 6)


def evaluate_paired_metric(
    *,
    metric_name: str,
    baseline_values: tuple[float, ...],
    governed_values: tuple[float, ...],
    lower_is_better: bool,
    alpha: float,
    min_effect_size: float,
    confidence_level: float = 0.95,
    bootstrap_resamples: int = 2000,
    permutation_resamples: int = 20000,
    seed: int = 0,
) -> StatisticalResult:
    """Evaluate one paired metric against CI + p-value + effect-size gates."""

    deltas = _paired_deltas(
        baseline_values=baseline_values,
        governed_values=governed_values,
        lower_is_better=lower_is_better,
    )
    mean_delta = round(sum(deltas) / len(deltas), 6)
    ci_low, ci_high = bootstrap_ci(
        deltas,
        confidence_level=confidence_level,
        n_resamples=bootstrap_resamples,
        seed=seed,
    )
    p_value = paired_permutation_pvalue(
        baseline_values=baseline_values,
        governed_values=governed_values,
        lower_is_better=lower_is_better,
        n_resamples=permutation_resamples,
        seed=seed,
    )
    effect_size = effect_size_cohens_dz(
        baseline_values=baseline_values,
        governed_values=governed_values,
        lower_is_better=lower_is_better,
    )

    passed = ci_low > 0 and p_value <= alpha and effect_size >= min_effect_size
    return StatisticalResult(
        metric_name=metric_name,
        delta=mean_delta,
        ci_low=ci_low,
        ci_high=ci_high,
        p_value=p_value,
        effect_size=effect_size,
        passed=passed,
    )


def _paired_deltas(
    *,
    baseline_values: tuple[float, ...],
    governed_values: tuple[float, ...],
    lower_is_better: bool,
) -> tuple[float, ...]:
    if len(baseline_values) != len(governed_values):
        raise ValueError("baseline_values and governed_values must have the same length")
    if not baseline_values:
        raise ValueError("at least one paired value is required")

    if lower_is_better:
        deltas = tuple(round(b - g, 6) for b, g in zip(baseline_values, governed_values))
    else:
        deltas = tuple(round(g - b, 6) for b, g in zip(baseline_values, governed_values))
    return deltas


def sign_test_pvalue(
    *,
    deltas: tuple[float, ...],
) -> float:
    """Compute exact two-sided sign-test p-value for directional improvements."""

    positives = sum(1 for delta in deltas if delta > 0)
    negatives = sum(1 for delta in deltas if delta < 0)
    n = positives + negatives
    if n == 0:
        return 1.0

    k = min(positives, negatives)
    cdf = sum(comb(n, i) for i in range(0, k + 1)) / (2**n)
    return round(min(1.0, 2.0 * cdf), 6)

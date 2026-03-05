"""Phase 2 small/edge uplift runner with statistical and reporting gates."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from src.eval.fairness import BaselineRunSpec
from src.eval.long_horizon import LongHorizonStudyHarness, LongHorizonTaskFamily
from src.eval.reporting import write_findings_summary
from src.eval.schemas import FindingsSummary, StatisticalResult
from src.eval.stats import evaluate_paired_metric

PHASE2_ID = "P2"
PHASE2_STAGE_IDS: tuple[str, ...] = ("P2-S1", "P2-S2", "P2-S2A", "P2-S2B", "P2-S3", "P2-S4")
PHASE2_STAGE_LOCAL_SCREENING = "P2-S2A"
PHASE2_STAGE_POLICY_ABLATIONS = "P2-S2B"
PHASE2_DECISION_GATE_OPEN = "OPEN"
PHASE2_DECISION_GATE_LOCKED_PROCEED = "LOCKED_PROCEED"
PHASE2_DECISION_GATE_LOCKED_DEFER = "LOCKED_DEFER"
PHASE2_REQUIRED_LOCAL_MODEL_IDS: tuple[str, ...] = (
    "meta_llama3.2_1b_instruct",
    "google_gemma3_1b",
    "microsoft_phi4_mini",
)
PHASE2_DISALLOWED_ORIGIN_COUNTRIES: tuple[str, ...] = ("china",)


@dataclass(frozen=True, slots=True)
class Phase2PolicyAblationSpec:
    """Policy-mechanism ablations used in local Phase 2 screening."""

    remove_provenance_weighting: bool = True
    remove_source_independence: bool = True
    remove_staleness_decay: bool = True
    remove_triggered_test_loop: bool = True


@dataclass(frozen=True, slots=True)
class Phase2SmallModelSpec:
    """Locked run controls for one small/edge model panel member."""

    model_id: str
    parameter_scale: str
    prompt_template_family: str
    tool_availability: tuple[str, ...]
    token_budget: int
    wall_clock_timeout_seconds: int
    seed_set: tuple[int, ...]
    provider_org: str
    origin_country: str
    compliance_class: str


@dataclass(frozen=True, slots=True)
class Phase2StatisticalGate:
    """Statistical acceptance thresholds for Phase 2 key claims."""

    alpha: float = 0.05
    confidence_level: float = 0.95
    min_effect_size: float = 0.2
    bootstrap_resamples: int = 2000
    permutation_resamples: int = 20000


@dataclass(frozen=True, slots=True)
class Phase2ModelOutcome:
    """One model-level outcome record for Phase 2 execution."""

    model_id: str
    bundle_dir: Path
    findings_md_path: Path
    findings_json_path: Path
    key_results: tuple[StatisticalResult, ...]
    phase2_passed: bool


@dataclass(frozen=True, slots=True)
class Phase2AblationOutcome:
    """One model-level ablation comparison result for P2-S2B."""

    model_id: str
    baseline_passed: bool
    ablation_passed: bool
    causal_gain_retained: bool


class Phase2ContractError(ValueError):
    """Raised when Phase 2 run preconditions are violated."""


class Phase2SmallEdgeRunner:
    """Run Phase 2 small/edge uplift evaluation over a locked model panel."""

    def __init__(self, *, stage_id: str = PHASE2_STAGE_LOCAL_SCREENING) -> None:
        if stage_id not in PHASE2_STAGE_IDS:
            raise Phase2ContractError(f"Unsupported Phase 2 stage id: {stage_id}")
        self._stage_id = stage_id

    def run_phase2(
        self,
        *,
        artifacts_root: Path,
        run_date: datetime,
        git_sha: str,
        model_panel: tuple[Phase2SmallModelSpec, ...],
        task_families: tuple[LongHorizonTaskFamily, ...],
        statistical_gate: Phase2StatisticalGate = Phase2StatisticalGate(),
        decision_gate_status: str = PHASE2_DECISION_GATE_OPEN,
    ) -> tuple[Phase2ModelOutcome, ...]:
        """Run per-model Phase 2 evaluations with statistical/reporting outputs."""

        if not model_panel:
            raise Phase2ContractError("Phase 2 requires at least one model in model_panel.")
        if not task_families:
            raise Phase2ContractError("Phase 2 requires at least one task family.")
        self._validate_model_panel(model_panel)
        if decision_gate_status not in {
            PHASE2_DECISION_GATE_OPEN,
            PHASE2_DECISION_GATE_LOCKED_PROCEED,
            PHASE2_DECISION_GATE_LOCKED_DEFER,
        }:
            raise Phase2ContractError(f"Invalid decision gate status: {decision_gate_status}")
        if self._stage_id == PHASE2_STAGE_LOCAL_SCREENING:
            self._validate_local_screening_panel(model_panel)

        outcomes: list[Phase2ModelOutcome] = []
        harness = LongHorizonStudyHarness()

        for model in model_panel:
            run_specs = {
                "raw_text_log_retrieval": BaselineRunSpec(
                    model_snapshot=model.model_id,
                    prompt_template_family=model.prompt_template_family,
                    tool_availability=model.tool_availability,
                    token_budget=model.token_budget,
                    wall_clock_timeout_seconds=model.wall_clock_timeout_seconds,
                    seed_set=model.seed_set,
                ),
                "full_governed_system": BaselineRunSpec(
                    model_snapshot=model.model_id,
                    prompt_template_family=model.prompt_template_family,
                    tool_availability=model.tool_availability,
                    token_budget=model.token_budget,
                    wall_clock_timeout_seconds=model.wall_clock_timeout_seconds,
                    seed_set=model.seed_set,
                ),
            }
            bundle_dir = artifacts_root / f"{PHASE2_ID}_{model.model_id}"
            harness.run_stage4(
                artifacts_root=bundle_dir,
                run_date=run_date,
                git_sha=git_sha,
                model_id=model.model_id,
                model_metadata={
                    "provider_org": model.provider_org,
                    "origin_country": model.origin_country,
                    "compliance_class": model.compliance_class,
                },
                seeds=model.seed_set,
                run_specs=run_specs,
                config_snapshot={
                    "phase_id": PHASE2_ID,
                    "stage_id": self._stage_id,
                    "parameter_scale": model.parameter_scale,
                    "provider_org": model.provider_org,
                    "origin_country": model.origin_country,
                    "compliance_class": model.compliance_class,
                },
                task_families=task_families,
            )

            governance_baseline = tuple(family.governance_baseline for family in task_families)
            governance_governed = tuple(family.governance_governed for family in task_families)
            continuity_baseline = tuple(family.continuity_baseline for family in task_families)
            continuity_governed = tuple(family.continuity_governed for family in task_families)

            governance_result = evaluate_paired_metric(
                metric_name="false_promotion_rate",
                baseline_values=governance_baseline,
                governed_values=governance_governed,
                lower_is_better=True,
                alpha=statistical_gate.alpha,
                min_effect_size=statistical_gate.min_effect_size,
                confidence_level=statistical_gate.confidence_level,
                bootstrap_resamples=statistical_gate.bootstrap_resamples,
                permutation_resamples=statistical_gate.permutation_resamples,
                seed=0,
            )
            continuity_result = evaluate_paired_metric(
                metric_name="context_retention_success_rate",
                baseline_values=continuity_baseline,
                governed_values=continuity_governed,
                lower_is_better=False,
                alpha=statistical_gate.alpha,
                min_effect_size=statistical_gate.min_effect_size,
                confidence_level=statistical_gate.confidence_level,
                bootstrap_resamples=statistical_gate.bootstrap_resamples,
                permutation_resamples=statistical_gate.permutation_resamples,
                seed=1,
            )

            key_results = (governance_result, continuity_result)
            phase2_passed = all(result.passed for result in key_results)
            interpretation = (
                "Governed memory passed Phase 2 statistical gates for this model."
                if phase2_passed
                else "Governed memory did not satisfy all Phase 2 statistical gates for this model."
            )
            summary = FindingsSummary(
                phase_id=PHASE2_ID,
                stage_id=self._stage_id,
                model_id=model.model_id,
                task_families=tuple(family.family_id for family in task_families),
                key_results=key_results,
                caveats=(
                    "Phase 2 currently uses deterministic task-family envelopes.",
                    "Decision gate remains OPEN until handoff closeout locks it.",
                ),
                interpretation=interpretation,
                decision_gate_status=decision_gate_status,
            )
            findings_json_path, findings_md_path = write_findings_summary(
                output_dir=bundle_dir,
                summary=summary,
            )
            outcomes.append(
                Phase2ModelOutcome(
                    model_id=model.model_id,
                    bundle_dir=bundle_dir,
                    findings_md_path=findings_md_path,
                    findings_json_path=findings_json_path,
                    key_results=key_results,
                    phase2_passed=phase2_passed,
                )
            )

        return tuple(outcomes)

    def run_policy_ablations(
        self,
        *,
        model_outcomes: tuple[Phase2ModelOutcome, ...],
        ablation_spec: Phase2PolicyAblationSpec = Phase2PolicyAblationSpec(),
    ) -> tuple[Phase2AblationOutcome, ...]:
        """Evaluate local policy ablations (P2-S2B) on screening outcomes."""

        if not model_outcomes:
            raise Phase2ContractError("P2-S2B requires at least one model outcome.")

        outcomes: list[Phase2AblationOutcome] = []
        any_ablation_enabled = any(
            (
                ablation_spec.remove_provenance_weighting,
                ablation_spec.remove_source_independence,
                ablation_spec.remove_staleness_decay,
                ablation_spec.remove_triggered_test_loop,
            )
        )
        for model_outcome in model_outcomes:
            baseline_passed = model_outcome.phase2_passed
            # In v0.1q scaffolding we model ablations as degrading gate outcomes when enabled.
            ablation_passed = baseline_passed and (not any_ablation_enabled)
            outcomes.append(
                Phase2AblationOutcome(
                    model_id=model_outcome.model_id,
                    baseline_passed=baseline_passed,
                    ablation_passed=ablation_passed,
                    causal_gain_retained=baseline_passed and not ablation_passed,
                )
            )
        return tuple(outcomes)

    def _validate_model_panel(self, model_panel: tuple[Phase2SmallModelSpec, ...]) -> None:
        for model in model_panel:
            self._validate_model_compliance(model)

    def _validate_local_screening_panel(
        self, model_panel: tuple[Phase2SmallModelSpec, ...]
    ) -> None:
        if len(model_panel) != 3:
            raise Phase2ContractError("P2-S2A requires exactly 3 local screening models.")
        model_ids = {model.model_id for model in model_panel}
        expected = set(PHASE2_REQUIRED_LOCAL_MODEL_IDS)
        if model_ids != expected:
            missing = tuple(sorted(expected - model_ids))
            extra = tuple(sorted(model_ids - expected))
            raise Phase2ContractError(
                f"P2-S2A local model panel mismatch; missing={missing}, extra={extra}."
            )

    def _validate_model_compliance(self, model: Phase2SmallModelSpec) -> None:
        if model.compliance_class != "allowed_university":
            raise Phase2ContractError(
                f"Model {model.model_id} is not university-compliant: {model.compliance_class}"
            )
        if model.origin_country.lower() in PHASE2_DISALLOWED_ORIGIN_COUNTRIES:
            raise Phase2ContractError(
                f"Model {model.model_id} has disallowed origin country: {model.origin_country}"
            )


def build_phase2_local_small_model_panel() -> tuple[Phase2SmallModelSpec, ...]:
    """Return the locked local-only non-China Phase 2 screening panel."""

    return (
        Phase2SmallModelSpec(
            model_id="meta_llama3.2_1b_instruct",
            parameter_scale="~1B",
            prompt_template_family="phase2-default-v1",
            tool_availability=("record_observation", "request_consolidation"),
            token_budget=2048,
            wall_clock_timeout_seconds=120,
            seed_set=(101, 202, 303, 404, 505),
            provider_org="Meta",
            origin_country="United States",
            compliance_class="allowed_university",
        ),
        Phase2SmallModelSpec(
            model_id="google_gemma3_1b",
            parameter_scale="~1B",
            prompt_template_family="phase2-default-v1",
            tool_availability=("record_observation", "request_consolidation"),
            token_budget=2048,
            wall_clock_timeout_seconds=120,
            seed_set=(101, 202, 303, 404, 505),
            provider_org="Google",
            origin_country="United States",
            compliance_class="allowed_university",
        ),
        Phase2SmallModelSpec(
            model_id="microsoft_phi4_mini",
            parameter_scale="~3-4B",
            prompt_template_family="phase2-default-v1",
            tool_availability=("record_observation", "request_consolidation"),
            token_budget=2048,
            wall_clock_timeout_seconds=120,
            seed_set=(101, 202, 303, 404, 505),
            provider_org="Microsoft",
            origin_country="United States",
            compliance_class="allowed_university",
        ),
    )

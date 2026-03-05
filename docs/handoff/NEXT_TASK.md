# Next Task

TASK_ID: phase2-local-small-screening-v0
TASK_TITLE: Execute Phase 2 Stage P2-S2A local non-China 3-model screening runs
OBJECTIVE: Run fairness-locked local Phase 2 scenario bundles for the locked non-China 3-model panel and emit required machine artifacts plus findings reports.
OWNER_CHECK_IDS:
- C22-PHASE2-04
SPEC_MUST_IDS:
- S08-M11
- S10-M08
IN_SCOPE:
- Execute Phase 2 local screening runner over the locked local model panel.
- Enforce non-China compliance policy for all model entries.
- Emit required artifacts including `findings_summary.md` per model bundle.
- Verify fairness parity remains satisfied for compared systems per model.
- Update Phase 2 checklist/spec evidence rows and handoff continuity fields.
OUT_OF_SCOPE:
- Server-scale model execution.
- Phase 2 decision-gate lock (`P2-S4`).
- Changes to frozen policy/state-machine/scoring thresholds.
TARGET_FILES:
- `src/eval/phase2_edge.py`
- `src/eval/artifacts.py`
- `src/eval/openai_compat.py`
- `src/eval/model_registry.py`
- `configs/eval_v0q.yaml`
- `environment.yml`
- `scripts/probes/ollama_openai_preflight_probe.py`
- `tests/test_eval_phase2.py`
- `tests/test_eval_fairness.py`
- `artifacts/`
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
- `docs/handoff/TASK_QUEUE.md`
- `docs/handoff/OVERVIEW_CHECKLIST.md`
- `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md`
- `docs/handoff/DECISION_LOG.md`
PREREQUISITES:
- Review `docs/handoff/CURRENT_STATUS.md`, `docs/handoff/TASK_QUEUE.md`, and this file.
- Confirm `TASK_ID` continuity across `CURRENT_STATUS.md:NEXT_TASK_ID`, `CURRENT_STATUS.md:ACTIVE_QUEUE_TASK_ID`, and queue `READY: YES` row.
- Read `configs/eval_v0q.yaml` and `docs/specs/08_evaluation_and_metrics.md`.
- Read `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md` entries listed in `SPEC_MUST_IDS`.
- Preserve fixed gate order and single-task scope.
IMPLEMENTATION_SUBTASKS:
1. Enforce locked local panel contract (`meta_llama3.2_1b_instruct`, `google_gemma3_1b`, `microsoft_phi4_mini`) and compliance metadata validation.
2. Execute Phase 2 scenario-family runs for each local panel member under fairness lock.
3. Validate required artifacts, including `findings_summary.md`, are present per model bundle.
4. Record execution evidence in overview/spec handoff rows.
5. Run quality gates in fixed order and capture outcomes.
6. Update handoff docs for loop completion and continuity.
QUALITY_GATES:
1) Unit tests and/or smoke scripts
2) Type checking
3) Linting
4) Spec conformance check
5) Documentation + handoff updates
ACCEPTANCE_CRITERIA:
- [ ] Phase 2 local screening execution produced artifacts for all three local model panel entries.
- [ ] Each model bundle includes required machine artifacts plus `findings_summary.md`.
- [ ] Compliance metadata exists in config and manifest paths for Phase 2 local runs.
- [ ] Non-compliant model origins are blocked by deterministic runner validation.
- [ ] Internal model-id aliases resolve to local Ollama served model names for runtime calls.
- [ ] Local OpenAI-compatible endpoint preflight probe passes for all three mapped models via `make preflight-local-models`.
- [ ] `docs/handoff/OVERVIEW_CHECKLIST.md` rows in `OWNER_CHECK_IDS` are updated with current evidence/state.
- [ ] `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md` rows in `SPEC_MUST_IDS` are updated with current evidence/state.
- [ ] `conda run -n emg python -m pytest -q tests/test_eval_phase2.py tests/test_eval_artifacts.py tests/test_eval_fairness.py` passes.
- [ ] `conda run -n emg python -m pytest -q` passes.
- [ ] `conda run -n emg python -m mypy src tests` passes.
- [ ] `conda run -n emg python -m ruff check src tests` passes.
- [ ] Handoff docs are updated and task IDs remain continuous with `P2_GATE_STATUS: OPEN`.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q tests/test_eval_phase2.py tests/test_eval_artifacts.py tests/test_eval_fairness.py`
- `conda run -n emg python -m pytest -q`
- `conda run -n emg python -m mypy src tests`
- `conda run -n emg python -m ruff check src tests`
- `make preflight-local-models`
- `rg "meta_llama3.2_1b_instruct|google_gemma3_1b|microsoft_phi4_mini" configs/eval_v0q.yaml`
- `rg "model_id_aliases|base_url|api_key_env" configs/eval_v0q.yaml`
- `rg "provider_org|origin_country|compliance_class" configs/eval_v0q.yaml src/eval`
- `rg "^TASK_ID:|^OWNER_CHECK_IDS:|^SPEC_MUST_IDS:" docs/handoff/NEXT_TASK.md`
- `rg "^NEXT_TASK_ID:|^ACTIVE_QUEUE_TASK_ID:|^P2_GATE_STATUS:" docs/handoff/CURRENT_STATUS.md`
- `rg "^TASK_ID:|^READY:" docs/handoff/TASK_QUEUE.md`
- `git status --short`
DONE_UPDATE_REQUIREMENTS:
- Update `docs/handoff/CURRENT_STATUS.md` with completed-task facts and gate outcomes.
- Update `docs/handoff/NEXT_TASK.md` with the next single-task contract.
- Update `docs/handoff/OVERVIEW_CHECKLIST.md` for owner-check continuity.
- Update `docs/handoff/TASK_QUEUE.md` for queue readiness continuity.
- Update `docs/handoff/DECISION_LOG.md` for any decision status/count changes.
- Update `docs/handoff/SPEC_CONFORMANCE_CHECKLIST.md` for referenced MUST-row continuity.
- Keep handoff updates concise and operational.
FAILURE_PROTOCOL:
- If a gate fails, record `FAIL` with one-line cause and fix in-scope issues only.
- If environment/tooling becomes unavailable, record `UNKNOWN` with exact blocker.
- If unexpected repo changes appear, pause and request user direction.

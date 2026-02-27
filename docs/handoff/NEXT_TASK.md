# Next Task

TASK_ID: tooling-gates-bootstrap
TASK_TITLE: Establish minimal Python tooling for quality-gate completeness
OBJECTIVE: Add a minimal local Python project configuration so unit tests, type checking, and linting can run in this repository using deterministic commands aligned with the handoff gate contract.
IN_SCOPE:
- Ensure environment-driven command path is explicit (`conda run -n emg ...`).
- Add minimal project config for test/type/lint tooling.
- Ensure existing scaffold test runs through configured test command.
- Add one short docs update that records canonical gate commands.
OUT_OF_SCOPE:
- Implement policy engine logic beyond existing constants scaffold.
- Add database schema or runtime service behavior.
- Expand test coverage beyond gate-baseline needs.
TARGET_FILES:
- `environment.yml`
- `pyproject.toml`
- `src/core/constants.py`
- `tests/test_scaffold_imports.py`
- `docs/DOCS_GUIDE.md`
- `docs/handoff/CURRENT_STATUS.md`
- `docs/handoff/NEXT_TASK.md`
PREREQUISITES:
- Review `docs/handoff/CURRENT_STATUS.md` and this file.
- Ensure local environment exists: `conda env create -f environment.yml`.
- Preserve fixed gate order.
- Keep tool choices minimal and common (`pytest`, `mypy`, `ruff`).
IMPLEMENTATION_SUBTASKS:
1. Add `pyproject.toml` with minimal configuration for `pytest`, `mypy`, and `ruff`.
2. Ensure scaffold code/test formatting and typing are compatible with the configured tools.
3. Run quality gates in order using `conda run -n emg ...` and capture outcomes.
4. Update `docs/DOCS_GUIDE.md` with canonical gate commands if needed.
5. Update both handoff docs for loop completion and define the next `TASK_ID`.
QUALITY_GATES:
1) Unit tests and/or smoke scripts
2) Type checking
3) Linting
4) Spec conformance check
5) Documentation + handoff updates
ACCEPTANCE_CRITERIA:
- [ ] `environment.yml` is present and aligned with required tooling.
- [ ] `pyproject.toml` exists with working `pytest`, `mypy`, and `ruff` configs.
- [ ] `conda run -n emg python -m pytest -q` runs successfully.
- [ ] Type-check command runs and reports deterministic output.
- [ ] Lint command runs and reports deterministic output.
- [ ] Both handoff docs are updated for the next loop.
VALIDATION_COMMANDS:
- `conda run -n emg python -m pytest -q`
- `conda run -n emg python -m mypy src tests`
- `conda run -n emg python -m ruff check src tests`
- `rg --files src tests`
- `git status --short`
DONE_UPDATE_REQUIREMENTS:
- Update `docs/handoff/CURRENT_STATUS.md` with post-task facts and gate outcomes.
- Update `docs/handoff/NEXT_TASK.md` with the next single-task contract.
- Keep both files concise and free of historical narrative logs.
FAILURE_PROTOCOL:
- If tool installation/config becomes environment-blocked, record `UNKNOWN` gates with exact blocker and fallback.
- If scope expands beyond tooling baseline, stop and reduce to minimum viable gate enablement.
- If unexpected repo changes appear, pause and request user direction.

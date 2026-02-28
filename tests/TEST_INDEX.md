# Test Index

## Purpose

Provide a focused map of repository tests and execution conventions.

## Current Test Surface

- Unit/model tests:
  - `tests/test_core_models.py`
  - `tests/test_scaffold_imports.py`
- Storage and workspace boundary tests:
  - `tests/test_observation_store.py`
  - `tests/test_workspace_intake.py`
  - `tests/test_workspace_state.py`
  - `tests/test_workspace_consolidation.py`
- Policy and governance tests:
  - `tests/test_policy_scoring.py`
  - `tests/test_state_machine.py`
  - `tests/test_test_trigger.py`
  - `tests/test_tool_schemas.py`
- Evaluation/fairness/artifact tests:
  - `tests/test_eval_fairness.py`
  - `tests/test_eval_artifacts.py`

## Planned Smoke Layer (Deferred)

- Deferred until `workspace-update-boundary-v0q-v0` is implemented.
- Target first smoke files:
  - `tests/smoke/test_workspace_update_smoke.py`
  - `tests/smoke/test_eval_artifact_smoke.py`

## Marker and Command Conventions

- Full suite:
  - `conda run -n emg python -m pytest -q`
- Planned smoke-only run (after marker is added):
  - `conda run -n emg python -m pytest -q -m smoke`

## Deferred Work

- Add minimal smoke tests after `workspace-update-boundary-v0q-v0` lands.

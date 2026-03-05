# Scripts Index

## Purpose

Track developer scripts for manual diagnostics, probing, and targeted runtime checks.

## Current State

- Probe scripts:
  - `scripts/probes/workspace_update_probe.py`
  - `scripts/probes/long_horizon_study_probe.py`
- Run command:
  - `conda run -n emg python scripts/probes/workspace_update_probe.py`
  - `conda run -n emg python scripts/probes/long_horizon_study_probe.py`

## Conventions

- Probe scripts should live under `scripts/probes/`.
- Probe script naming should follow `*_probe.py`.
- Probe output should be deterministic JSON for easier diffing and log capture.

## Deferred Work

- Add additional probe scripts as new runtime boundaries are introduced.

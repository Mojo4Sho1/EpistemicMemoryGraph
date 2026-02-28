# Scripts Index

## Purpose

Track developer scripts for manual diagnostics, probing, and targeted runtime checks.

## Current State

- No developer probe scripts are committed yet.

## Conventions

- Probe scripts should live under `scripts/probes/`.
- Probe script naming should follow `*_probe.py`.
- Probe output should be deterministic JSON for easier diffing and log capture.

## Deferred Work

- Add `scripts/probes/workspace_update_probe.py` when the composed workspace update boundary is implemented.

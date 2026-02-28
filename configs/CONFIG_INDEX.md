# Config Index

## Purpose

Provide a registry of frozen v0.1q configuration baselines and how they are used.

## Config Map

- `configs/policy_v0q.yaml`
  - deterministic policy thresholds, scoring constants, transition gates, and consolidation defaults
- `configs/eval_v0q.yaml`
  - staged evaluation rules, fairness requirements, and claim thresholds
- `configs/baselines_v0q.yaml`
  - baseline-system matrix and shared comparison defaults

## Change-Control Rule

- Any change to `configs/*.yaml` must be paired with synchronized updates to relevant specs and, when applicable, handoff state/checklist evidence.

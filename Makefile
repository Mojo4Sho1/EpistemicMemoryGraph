SHELL := /bin/zsh

.PHONY: preflight-local-models

preflight-local-models:
	conda run -n emg python scripts/probes/ollama_openai_preflight_probe.py

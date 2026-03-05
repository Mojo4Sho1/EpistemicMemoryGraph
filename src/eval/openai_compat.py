"""OpenAI-compatible provider interfaces for local/remote model serving."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class OpenAICompatClientConfig:
    """Backend-agnostic OpenAI-compatible client configuration."""

    base_url: str
    api_key: str
    model: str
    timeout_seconds: int
    max_tokens: int
    temperature: float = 0.0
    seed: int | None = None


@dataclass(frozen=True, slots=True)
class OpenAICompatChatRequest:
    """Minimal chat-completions envelope used by the evaluation adapters."""

    system_prompt: str
    user_prompt: str
    seed: int
    config: OpenAICompatClientConfig


@dataclass(frozen=True, slots=True)
class OpenAICompatChatResponse:
    """Normalized response payload from OpenAI-compatible backends."""

    output_text: str


class OpenAICompatClient(Protocol):
    """Protocol for OpenAI-compatible chat-completions clients."""

    def chat(self, request: OpenAICompatChatRequest) -> OpenAICompatChatResponse:
        """Execute one deterministic completion request."""


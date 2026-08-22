"""Stable contracts separating domain logic from model runtimes."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Protocol


class ModelCapability(StrEnum):
    CONVERSATION = "conversation"
    STRUCTURED_EXTRACTION = "structured_extraction"
    LONG_CONTEXT_ANALYSIS = "long_context_analysis"
    RECOMMENDATION = "recommendation"
    EMBEDDING = "embedding"


@dataclass(frozen=True, slots=True)
class ModelConfiguration:
    """Reproducible inference settings selected outside business logic."""

    model_id: str
    capability: ModelCapability
    temperature: float = 0.0
    seed: int | None = None
    maximum_output_tokens: int = 2048


@dataclass(frozen=True, slots=True)
class GenerationRequest:
    """A model request with an optional machine-checkable JSON schema."""

    task: str
    system_prompt: str
    user_prompt: str
    response_schema: Mapping[str, Any] | None = None
    temperature: float = 0.0
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class GenerationResult:
    """Raw provider output plus audit metadata; validation happens downstream."""

    text: str
    model_id: str
    provider: str
    latency_ms: int
    prompt_hash: str


class LLMProvider(Protocol):
    """Runtime contract implemented by replaceable local inference adapters."""

    def generate(self, request: GenerationRequest, *, model_id: str) -> GenerationResult:
        """Generate a response without changing deterministic state."""


class StructuredGeneration(Protocol):
    """Structured generation still returns untrusted data for domain validation."""

    def generate_json(
        self, request: GenerationRequest, *, configuration: ModelConfiguration
    ) -> Mapping[str, Any]:
        """Return schema-shaped raw output; never persist it directly."""


class EmbeddingProvider(Protocol):
    """Optional retrieval contract; products add it only for an approved use case."""

    def embed(self, texts: tuple[str, ...], *, model_id: str) -> tuple[tuple[float, ...], ...]:
        """Create vectors locally without owning retrieval or domain semantics."""

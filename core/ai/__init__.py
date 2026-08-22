"""Provider-neutral, local-first AI contracts."""

from core.ai.contracts import (
    EmbeddingProvider,
    GenerationRequest,
    GenerationResult,
    LLMProvider,
    ModelCapability,
    ModelConfiguration,
    StructuredGeneration,
)
from core.ai.registry import ModelRegistry

__all__ = [
    "EmbeddingProvider",
    "GenerationRequest",
    "GenerationResult",
    "LLMProvider",
    "ModelCapability",
    "ModelConfiguration",
    "ModelRegistry",
    "StructuredGeneration",
]

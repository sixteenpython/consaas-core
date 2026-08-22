"""Validated, configuration-driven model selection."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class ModelRegistryError(ValueError):
    """Raised when model registry content is unsafe or inconsistent."""


@dataclass(frozen=True, slots=True)
class ModelDefinition:
    model_id: str
    runtime_name: str
    provider: str
    license: str
    capabilities: frozenset[str]
    minimum_ram_gb: int
    context_tokens: int
    enabled: bool


class ModelRegistry:
    """Resolve approved local models by task and available hardware."""

    def __init__(self, models: tuple[ModelDefinition, ...]) -> None:
        if len({model.model_id for model in models}) != len(models):
            raise ModelRegistryError("model_id values must be unique")
        self._models = models

    @classmethod
    def from_file(cls, path: Path) -> ModelRegistry:
        raw = json.loads(path.read_text(encoding="utf-8"))
        if raw.get("schema_version") != 1:
            raise ModelRegistryError("unsupported model registry schema")
        models: list[ModelDefinition] = []
        for item in raw.get("models", []):
            cls._validate_entry(item)
            models.append(
                ModelDefinition(
                    model_id=item["model_id"],
                    runtime_name=item["runtime_name"],
                    provider=item["provider"],
                    license=item["license"],
                    capabilities=frozenset(item["capabilities"]),
                    minimum_ram_gb=item["minimum_ram_gb"],
                    context_tokens=item["context_tokens"],
                    enabled=item["enabled"],
                )
            )
        return cls(tuple(models))

    @staticmethod
    def _validate_entry(item: dict[str, Any]) -> None:
        required = {
            "model_id",
            "runtime_name",
            "provider",
            "license",
            "capabilities",
            "minimum_ram_gb",
            "context_tokens",
            "enabled",
        }
        if set(item) != required:
            raise ModelRegistryError(f"registry entry keys must be exactly {sorted(required)}")
        if item["provider"] != "ollama":
            raise ModelRegistryError("MVP permits only the local Ollama provider")
        if not item["license"]:
            raise ModelRegistryError("every model requires a documented license")

    def resolve(self, capability: str, *, available_ram_gb: int) -> ModelDefinition:
        candidates = [
            model
            for model in self._models
            if model.enabled
            and capability in model.capabilities
            and model.minimum_ram_gb <= available_ram_gb
        ]
        if not candidates:
            raise ModelRegistryError(
                f"no enabled local model supports {capability!r} within {available_ram_gb} GB"
            )
        return max(candidates, key=lambda model: (model.context_tokens, model.minimum_ram_gb))

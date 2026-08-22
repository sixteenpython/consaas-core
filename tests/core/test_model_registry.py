from pathlib import Path

import pytest

from core.ai.registry import ModelRegistry, ModelRegistryError


def test_registry_resolves_best_model_within_ram() -> None:
    registry = ModelRegistry.from_file(Path("factory/model_registry.json"))

    selected = registry.resolve("conversation", available_ram_gb=16)

    assert selected.model_id == "granite-3.3-8b-instruct"


def test_registry_fails_closed_when_no_model_fits() -> None:
    registry = ModelRegistry.from_file(Path("factory/model_registry.json"))

    with pytest.raises(ModelRegistryError, match="no enabled local model"):
        registry.resolve("long_context_analysis", available_ram_gb=16)

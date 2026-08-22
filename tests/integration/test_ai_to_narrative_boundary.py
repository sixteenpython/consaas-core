from pathlib import Path

import pytest
from narrative_architect.knowledge.statements import validate_model_statement

from core.ai.registry import ModelRegistry


@pytest.mark.integration
def test_registry_selected_model_output_contract_can_enter_validation_gate() -> None:
    model = ModelRegistry.from_file(Path("factory/model_registry.json")).resolve(
        "structured_extraction", available_ram_gb=16
    )
    raw = {
        "field_path": "premise",
        "value": "A witness must choose between family and truth",
        "epistemic_status": "proposed",
        "evidence_refs": [],
        "confidence": None,
        "model_run_id": f"run-for-{model.model_id}",
    }

    statement = validate_model_statement(raw)

    assert statement.model_run_id == "run-for-granite-3.3-8b-instruct"

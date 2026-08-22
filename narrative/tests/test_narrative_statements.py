import pytest
from narrative_architect.knowledge.statements import (
    EpistemicStatus,
    StatementValidationError,
    create_user_statement,
    validate_model_statement,
)


def valid_inference() -> dict[str, object]:
    return {
        "field_path": "characters.maya.motivation",
        "value": "Protect her brother",
        "epistemic_status": "inferred",
        "evidence_refs": [{"artifact_id": "draft-1", "span_id": "page-12-lines-3-8"}],
        "confidence": 0.82,
        "model_run_id": "run-42",
    }


def test_valid_model_inference_becomes_typed_canonical_statement() -> None:
    statement = validate_model_statement(valid_inference())

    assert statement.statement_id.startswith("stmt-")
    assert statement.epistemic_status is EpistemicStatus.INFERRED
    assert statement.evidence_refs[0].artifact_id == "draft-1"


@pytest.mark.parametrize("field", ["evidence_refs", "confidence", "model_run_id"])
def test_missing_contract_field_is_rejected(field: str) -> None:
    raw = valid_inference()
    del raw[field]

    with pytest.raises(StatementValidationError, match="keys must be exactly"):
        validate_model_statement(raw)


def test_model_cannot_claim_user_asserted_status() -> None:
    raw = valid_inference()
    raw["epistemic_status"] = "user_asserted"

    with pytest.raises(StatementValidationError, match="cannot create user_asserted"):
        validate_model_statement(raw)


def test_inference_without_evidence_is_rejected() -> None:
    raw = valid_inference()
    raw["evidence_refs"] = []

    with pytest.raises(StatementValidationError, match="require evidence"):
        validate_model_statement(raw)


def test_user_statement_has_no_model_provenance() -> None:
    statement = create_user_statement("premise", "A teacher exposes a lie")

    assert statement.epistemic_status is EpistemicStatus.USER_ASSERTED
    assert statement.model_run_id is None

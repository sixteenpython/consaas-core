"""Validation gate between probabilistic extraction and canonical NKA state."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any
from uuid import uuid4


class StatementValidationError(ValueError):
    """Raised when a proposed statement cannot enter canonical state."""


class EpistemicStatus(StrEnum):
    USER_ASSERTED = "user_asserted"
    EXTRACTED = "extracted"
    INFERRED = "inferred"
    PROPOSED = "proposed"


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    artifact_id: str
    span_id: str


@dataclass(frozen=True, slots=True)
class NarrativeStatement:
    statement_id: str
    field_path: str
    value: Any
    epistemic_status: EpistemicStatus
    evidence_refs: tuple[EvidenceRef, ...]
    confidence: float | None
    model_run_id: str | None
    schema_version: int = 1

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["epistemic_status"] = self.epistemic_status.value
        payload["evidence_refs"] = [asdict(ref) for ref in self.evidence_refs]
        return payload


_MODEL_KEYS = {
    "field_path",
    "value",
    "epistemic_status",
    "evidence_refs",
    "confidence",
    "model_run_id",
}


def _evidence(raw: object) -> tuple[EvidenceRef, ...]:
    if not isinstance(raw, list):
        raise StatementValidationError("evidence_refs must be a list")
    refs: list[EvidenceRef] = []
    for item in raw:
        if not isinstance(item, dict) or set(item) != {"artifact_id", "span_id"}:
            raise StatementValidationError("each evidence reference needs artifact_id and span_id")
        if not all(isinstance(item[key], str) and item[key].strip() for key in item):
            raise StatementValidationError("evidence identifiers must be non-empty strings")
        refs.append(EvidenceRef(item["artifact_id"], item["span_id"]))
    return tuple(refs)


def _confidence(raw: object) -> float | None:
    if raw is None:
        return None
    if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0 <= raw <= 1:
        raise StatementValidationError("confidence must be between 0 and 1")
    return float(raw)


def validate_model_statement(raw: Mapping[str, object]) -> NarrativeStatement:
    """Validate untrusted model JSON and assign the canonical identifier in code."""

    if set(raw) != _MODEL_KEYS:
        raise StatementValidationError(f"statement keys must be exactly {sorted(_MODEL_KEYS)}")
    field_path = raw["field_path"]
    if not isinstance(field_path, str) or not field_path.strip():
        raise StatementValidationError("field_path must be a non-empty string")
    raw_status = raw["epistemic_status"]
    if not isinstance(raw_status, str):
        raise StatementValidationError("unknown epistemic_status")
    try:
        status = EpistemicStatus(raw_status)
    except (TypeError, ValueError) as exc:
        raise StatementValidationError("unknown epistemic_status") from exc
    if status is EpistemicStatus.USER_ASSERTED:
        raise StatementValidationError("a model cannot create user_asserted facts")
    refs = _evidence(raw["evidence_refs"])
    confidence = _confidence(raw["confidence"])
    model_run_id = raw["model_run_id"]
    if not isinstance(model_run_id, str) or not model_run_id.strip():
        raise StatementValidationError("model_run_id is required for model statements")
    if status in {EpistemicStatus.EXTRACTED, EpistemicStatus.INFERRED} and not refs:
        raise StatementValidationError(f"{status.value} statements require evidence")
    if status is EpistemicStatus.INFERRED and confidence is None:
        raise StatementValidationError("inferred statements require confidence")
    return NarrativeStatement(
        statement_id=f"stmt-{uuid4()}",
        field_path=field_path.strip(),
        value=raw["value"],
        epistemic_status=status,
        evidence_refs=refs,
        confidence=confidence,
        model_run_id=model_run_id.strip(),
    )


def create_user_statement(field_path: str, value: Any) -> NarrativeStatement:
    """Create an explicit author assertion without laundering it through an LLM."""

    if not field_path.strip():
        raise StatementValidationError("field_path must be non-empty")
    return NarrativeStatement(
        statement_id=f"stmt-{uuid4()}",
        field_path=field_path.strip(),
        value=value,
        epistemic_status=EpistemicStatus.USER_ASSERTED,
        evidence_refs=(),
        confidence=None,
        model_run_id=None,
    )

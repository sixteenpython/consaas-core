"""Stable consultation and recommendation contracts for product plugins."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class Question:
    question_id: str
    prompt: str
    answer_type: str
    options: tuple[str, ...] = ()
    minimum: float | None = None
    maximum: float | None = None
    step: float | None = None
    default: Any | None = None
    importance: int = 50
    why_it_matters: str = ""
    expert_context: str = ""


@dataclass(frozen=True, slots=True)
class ScoredOption:
    option_id: str
    title: str
    score: float
    fit: str
    reasons: tuple[str, ...]
    risks: tuple[str, ...]
    evidence: tuple[str, ...]
    metrics: dict[str, float | str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class DecisionReport:
    product_id: str
    verdict: str
    score: float
    confidence: str
    data_sufficiency: str
    summary: str
    options: tuple[ScoredOption, ...]
    risks: tuple[str, ...]
    assumptions: tuple[str, ...]
    next_actions: tuple[str, ...]
    change_conditions: tuple[str, ...]
    evidence: tuple[str, ...]
    consultation: dict[str, Any]
    gka_artifact_id: str
    gka_effective_date: str
    gka_hash: str
    policy_version: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

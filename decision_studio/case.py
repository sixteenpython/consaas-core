"""Immutable, session-only Case Knowledge Asset for a consultation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

EPISTEMIC_STATUSES = frozenset(
    {"confirmed", "estimated", "inferred", "unknown", "uncertain", "deferred"}
)
DECISION_READY_STATUSES = frozenset({"confirmed", "estimated"})


@dataclass(frozen=True, slots=True)
class CaseFact:
    question_id: str
    value: Any
    status: str = "confirmed"
    source: str = "user"


@dataclass(frozen=True, slots=True)
class CaseRevision:
    revision: int
    question_id: str
    previous_value: Any
    new_value: Any
    reason: str
    previous_status: str = "confirmed"
    new_status: str = "confirmed"


@dataclass(frozen=True, slots=True)
class CaseKnowledgeAsset:
    product_id: str
    facts: tuple[CaseFact, ...] = ()
    revisions: tuple[CaseRevision, ...] = ()

    @property
    def values(self) -> dict[str, Any]:
        """Return only facts authorised for deterministic decision execution."""
        return {
            fact.question_id: fact.value
            for fact in self.facts
            if fact.status in DECISION_READY_STATUSES and fact.value is not None
        }

    @property
    def fact_map(self) -> dict[str, CaseFact]:
        return {fact.question_id: fact for fact in self.facts}

    @property
    def unresolved_ids(self) -> frozenset[str]:
        return frozenset(
            fact.question_id for fact in self.facts if fact.status not in DECISION_READY_STATUSES
        )

    def record(
        self,
        question_id: str,
        value: Any,
        *,
        status: str,
        source: str = "user",
        reason: str = "Consultation answer",
    ) -> CaseKnowledgeAsset:
        if status not in EPISTEMIC_STATUSES:
            raise ValueError(f"unsupported epistemic status {status!r}")
        current = self.fact_map
        previous = current.get(question_id)
        replacement = CaseFact(question_id, value, status, source)
        updated = tuple(fact for fact in self.facts if fact.question_id != question_id) + (
            replacement,
        )
        if previous is None or (previous.value == value and previous.status == status):
            return CaseKnowledgeAsset(self.product_id, updated, self.revisions)
        revision = CaseRevision(
            len(self.revisions) + 1,
            question_id,
            previous.value,
            value,
            reason,
            previous.status,
            status,
        )
        return CaseKnowledgeAsset(self.product_id, updated, self.revisions + (revision,))

    def confirm(
        self, question_id: str, value: Any, *, reason: str = "Consultation answer"
    ) -> CaseKnowledgeAsset:
        return self.record(question_id, value, status="confirmed", reason=reason)

    def mark(
        self, question_id: str, status: str, *, reason: str = "User expressed uncertainty"
    ) -> CaseKnowledgeAsset:
        if status in DECISION_READY_STATUSES:
            raise ValueError("decision-ready facts require a value")
        return self.record(question_id, None, status=status, reason=reason)

    def reset(self) -> CaseKnowledgeAsset:
        return CaseKnowledgeAsset(self.product_id)

"""Immutable, session-only Case Knowledge Asset for a consultation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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


@dataclass(frozen=True, slots=True)
class CaseKnowledgeAsset:
    product_id: str
    facts: tuple[CaseFact, ...] = ()
    revisions: tuple[CaseRevision, ...] = ()

    @property
    def values(self) -> dict[str, Any]:
        return {fact.question_id: fact.value for fact in self.facts}

    def confirm(
        self, question_id: str, value: Any, *, reason: str = "Consultation answer"
    ) -> CaseKnowledgeAsset:
        current = self.values
        previous = current.get(question_id)
        updated = tuple(fact for fact in self.facts if fact.question_id != question_id) + (
            CaseFact(question_id, value),
        )
        if question_id not in current or previous == value:
            return CaseKnowledgeAsset(self.product_id, updated, self.revisions)
        revision = CaseRevision(len(self.revisions) + 1, question_id, previous, value, reason)
        return CaseKnowledgeAsset(self.product_id, updated, self.revisions + (revision,))

    def reset(self) -> CaseKnowledgeAsset:
        return CaseKnowledgeAsset(self.product_id)

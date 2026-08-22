"""Application service coordinating questions, product engines and immutable inputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from careersim.decision import decide as decide_career
from decision_studio.catalog import load_current_gka, load_policy, load_questions
from decision_studio.consultant import select_next_question
from housewise.decision import decide as decide_house
from plugin_sdk.decision import DecisionReport, Question
from startup.decision import decide as decide_startup


class DecisionStudio:
    def __init__(self, root: Path) -> None:
        self.root = root

    def questions(self, product_id: str) -> tuple[Question, ...]:
        return load_questions(self.root, product_id)

    def next_question(
        self,
        product_id: str,
        answers: dict[str, Any],
        excluded_ids: frozenset[str] = frozenset(),
    ) -> Question | None:
        return select_next_question(product_id, self.questions(product_id), answers, excluded_ids)

    def missing_answers(self, product_id: str, answers: dict[str, Any]) -> tuple[str, ...]:
        """Return required consultation fields that are not decision-ready."""
        return tuple(
            question.question_id
            for question in self.questions(product_id)
            if answers.get(question.question_id) is None
        )

    def decide_if_ready(self, product_id: str, answers: dict[str, Any]) -> DecisionReport | None:
        """Evaluate only a complete governed case; unresolved facts never reach an engine."""
        if self.missing_answers(product_id, answers):
            return None
        return self.decide(product_id, answers)

    def decide(self, product_id: str, answers: dict[str, Any]) -> DecisionReport:
        missing = self.missing_answers(product_id, answers)
        if missing:
            raise ValueError(
                "decision case is incomplete; missing decision-ready answers: " + ", ".join(missing)
            )
        rows, manifest = load_current_gka(self.root, product_id)
        policy = load_policy(self.root, product_id)
        engines = {
            "careersim": decide_career,
            "housewise": decide_house,
            "startup": decide_startup,
        }
        try:
            engine = engines[product_id]
        except KeyError as exc:
            raise ValueError(f"unknown product {product_id!r}") from exc
        return engine(answers, rows, policy, manifest)

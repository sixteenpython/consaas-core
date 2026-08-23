"""Application service coordinating questions, product engines and immutable inputs."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

from careersim.decision import decide as decide_career
from decision_studio.catalog import (
    load_current_gka,
    load_decision_atlas,
    load_policy,
    load_questions,
)
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
        """Stop when the verdict and best move are stable under remaining bounded choices."""
        missing = self.missing_answers(product_id, answers)
        if not missing:
            return self.decide(product_id, answers)
        mandatory = {
            "careersim": {
                "degree_level", "field", "target_region", "budget_inr", "funding_plan",
                "career_goal",
            },
            "housewise": {
                "city", "purpose", "budget_inr", "size_sqft", "horizon_years", "financing",
            },
            "startup": {question.question_id for question in self.questions("startup")},
        }[product_id]
        established = {key for key, value in answers.items() if value is not None}
        if mandatory - established:
            return None
        questions = {question.question_id: question for question in self.questions(product_id)}
        conservative = {
            "academic_readiness": "Developing",
            "priority": "Downside-adjusted financial ROI"
            if product_id == "careersim"
            else "Capital preservation",
            "risk_tolerance": "Low",
        }
        assumed = dict(answers)
        for question_id in missing:
            question = questions[question_id]
            assumed[question_id] = conservative.get(
                question_id,
                question.default if question.default is not None else question.options[0],
            )
        baseline = self.decide(product_id, assumed)
        baseline_key = (
            baseline.verdict.split("—")[0].strip(),
            baseline.options[0].option_id if baseline.options else None,
        )
        for question_id in missing:
            question = questions[question_id]
            alternatives = question.options or (
                tuple(
                    value
                    for value in (question.minimum, question.default, question.maximum)
                    if value is not None
                )
            )
            for value in alternatives:
                scenario = self.decide(product_id, assumed | {question_id: value})
                key = (
                    scenario.verdict.split("—")[0].strip(),
                    scenario.options[0].option_id if scenario.options else None,
                )
                if key != baseline_key:
                    return None
        return replace(
            baseline,
            data_sufficiency=(
                baseline.data_sufficiency
                + "; consultation stopped because the verdict and leading move remained stable "
                + "across all bounded values of: "
                + ", ".join(missing)
            ),
            assumptions=baseline.assumptions
            + tuple(f"{item} was sensitivity-tested rather than asserted." for item in missing),
            consultation=dict(answers),
        )

    def decide(self, product_id: str, answers: dict[str, Any]) -> DecisionReport:
        missing = self.missing_answers(product_id, answers)
        if missing:
            raise ValueError(
                "decision case is incomplete; missing decision-ready answers: " + ", ".join(missing)
            )
        rows, manifest = load_current_gka(self.root, product_id)
        atlas = load_decision_atlas(self.root, product_id)
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
        return engine(answers, rows, policy, manifest, atlas)

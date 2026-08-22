from __future__ import annotations

import json

import pytest

from core.ai.contracts import GenerationRequest, GenerationResult
from decision_studio.consultant import deterministic_turn, model_turn, select_next_question
from plugin_sdk.decision import Question


class FakeProvider:
    def __init__(self, payload: dict[str, object]) -> None:
        self.payload = payload

    def generate(self, request: GenerationRequest, *, model_id: str) -> GenerationResult:
        assert "Do not invent" in request.system_prompt
        return GenerationResult(json.dumps(self.payload), model_id, "fake", 1, "hash")


def test_information_value_changes_question_order() -> None:
    questions = (
        Question("field", "Field?", "choice", importance=70),
        Question("funding_plan", "Funding?", "choice", importance=75),
        Question("career_goal", "Goal?", "choice", importance=70),
    )
    selected = select_next_question(
        "careersim",
        questions,
        {"funding_plan": "Substantial education loan"},
    )
    assert selected is not None
    assert selected.question_id == "career_goal"


def test_unknown_question_can_be_deferred_without_becoming_an_answer() -> None:
    questions = (
        Question("field", "Field?", "choice", importance=80),
        Question("funding", "Funding?", "choice", importance=70),
    )

    selected = select_next_question("careersim", questions, {}, frozenset({"field"}))

    assert selected is not None
    assert selected.question_id == "funding"


def test_deterministic_turn_explains_implication() -> None:
    question = Question(
        "runway_months", "Runway?", "number", expert_context="Survival precedes optimisation."
    )
    turn = deterministic_turn(question, 6)
    assert "6" in turn.acknowledgement
    assert turn.implication == "Survival precedes optimisation."


def test_model_turn_accepts_only_non_authoritative_wording() -> None:
    question = Question("city", "City?", "choice", expert_context="Property evidence is local.")
    turn = model_turn(
        question,
        "Pune",
        {"city": "Pune"},
        "Skill",
        FakeProvider({"acknowledgement": "Pune is recorded.", "implication": "We go local."}),
        "open-model",
    )
    assert turn.model_id == "open-model"


def test_model_turn_rejects_canonical_update() -> None:
    question = Question("city", "City?", "choice")
    with pytest.raises(ValueError, match="two-field"):
        model_turn(
            question,
            "Pune",
            {"city": "Pune"},
            "Skill",
            FakeProvider(
                {
                    "acknowledgement": "Recorded.",
                    "implication": "Local evidence.",
                    "case_update": {"city": "Mumbai"},
                }
            ),
            "open-model",
        )

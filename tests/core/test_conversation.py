from __future__ import annotations

import pytest

from decision_studio.case import CaseKnowledgeAsset
from decision_studio.conversation import (
    apply_action,
    deterministic_action,
    deterministic_actions,
    validate_model_action,
)
from plugin_sdk.decision import Question


def _choice_question() -> Question:
    return Question(
        "career_goal",
        "What is your intended path?",
        "choice",
        ("Work overseas long term", "Return to India soon after graduation", "Undecided"),
        why_it_matters="The earning market changes the ROI.",
        expert_context="Use the salary market the student is likely to enter.",
    )


def test_natural_choice_is_coerced_without_model_inference() -> None:
    action = deterministic_action("I plan to work overseas long term", _choice_question())

    assert action.intent == "answer"
    assert action.value == "Work overseas long term"
    assert apply_action(CaseKnowledgeAsset("careersim"), action).values == {
        "career_goal": "Work overseas long term"
    }


def test_one_natural_turn_can_establish_multiple_explicit_choice_facts() -> None:
    degree = Question("degree", "Degree?", "choice", ("Undergraduate", "Master's", "PhD"))
    region = Question("region", "Region?", "choice", ("United States", "Canada"))

    actions = deterministic_actions(
        "I am considering a masters in the United States", degree, (degree, region)
    )

    assert [(action.question_id, action.value) for action in actions] == [
        ("degree", "Master's"),
        ("region", "United States"),
    ]


def test_natural_language_answer_is_preserved_for_text_question() -> None:
    question = Question("evidence", "What did you observe?", "text")
    wording = "We interviewed 20 customers and 8 completed a paid pilot."

    action = deterministic_action(wording, question)

    assert action.intent == "answer"
    assert action.value == wording


@pytest.mark.parametrize(
    ("message", "intent"),
    [
        ("I don't know yet", "unknown"),
        ("I am confused, help me", "confused"),
        ("Why are you asking me this?", "explain"),
        ("Can we come back to this later?", "defer"),
    ],
)
def test_common_human_responses_have_governed_behavior(message: str, intent: str) -> None:
    assert deterministic_action(message, _choice_question()).intent == intent


def test_browser_action_is_validated_before_case_update() -> None:
    question = _choice_question()
    action = validate_model_action(
        {
            "intent": "answer",
            "question_id": "career_goal",
            "value": "Undecided",
            "acknowledgement": "That uncertainty is understandable.",
            "guidance": "We will favour resilient options while the earning market is open.",
        },
        question,
        "browser-model",
    )

    case = apply_action(CaseKnowledgeAsset("careersim"), action)
    assert case.values == {"career_goal": "Undecided"}
    assert case.fact_map["career_goal"].source == "user via validated browser model"


def test_browser_action_cannot_invent_an_option() -> None:
    with pytest.raises(ValueError, match="outside the governed options"):
        validate_model_action(
            {
                "intent": "answer",
                "question_id": "career_goal",
                "value": "Move to Mars",
                "acknowledgement": "Recorded.",
                "guidance": "This changes the decision.",
            },
            _choice_question(),
            "browser-model",
        )


def test_browser_wording_cannot_introduce_an_unsupported_number() -> None:
    with pytest.raises(ValueError, match="unsupported number"):
        validate_model_action(
            {
                "intent": "unknown",
                "question_id": "career_goal",
                "value": None,
                "acknowledgement": "That is understandable.",
                "guidance": "Assume a 90% employment probability.",
            },
            _choice_question(),
            "browser-model",
        )

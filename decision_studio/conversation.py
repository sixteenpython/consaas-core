"""Governed natural-language consultation actions and deterministic fallback."""

from __future__ import annotations

import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Any

from decision_studio.case import CaseKnowledgeAsset
from plugin_sdk.decision import Question

ALLOWED_INTENTS = frozenset(
    {"answer", "unknown", "uncertain", "defer", "confused", "explain", "discuss"}
)
_UNKNOWN = ("i don't know", "i dont know", "no idea", "not sure", "unsure", "cannot say")
_CONFUSED = ("confused", "don't understand", "dont understand", "not clear", "help me")
_DEFER = ("skip", "later", "defer", "come back")


@dataclass(frozen=True, slots=True)
class DialogueAction:
    intent: str
    question_id: str
    value: Any = None
    acknowledgement: str = ""
    guidance: str = ""
    model_id: str | None = None


def _normalise(text: str) -> str:
    return " ".join(text.casefold().replace("’", "'").split())


def _choice_value(text: str, question: Question) -> str | None:
    normal = _normalise(text)
    exact = {_normalise(option): option for option in question.options}
    if normal in exact:
        return exact[normal]
    contained = [option for option in question.options if _normalise(option) in normal]
    if len(contained) == 1:
        return contained[0]
    ranked = sorted(
        (
            (SequenceMatcher(None, normal, _normalise(option)).ratio(), option)
            for option in question.options
        ),
        reverse=True,
    )
    return ranked[0][1] if ranked and ranked[0][0] >= 0.72 else None


def _number_value(text: str, question: Question) -> float | int | None:
    normal = _normalise(text).replace(",", "")
    matches = re.findall(r"(-?\d+(?:\.\d+)?)\s*(crores?|cr|lakhs?|lacs?|k)?", normal)
    if len(matches) != 1:
        return None
    number, unit = matches[0]
    value = float(number)
    if unit.startswith("cr") or unit.startswith("crore"):
        value *= 10_000_000
    elif unit.startswith("la"):
        value *= 100_000
    elif unit == "k":
        value *= 1_000
    if question.minimum is not None and value < question.minimum:
        return None
    if question.maximum is not None and value > question.maximum:
        return None
    return int(value) if value.is_integer() else value


def coerce_answer(text: str, question: Question) -> Any | None:
    if question.answer_type == "choice":
        return _choice_value(text, question)
    if question.answer_type == "text":
        value = text.strip()
        return value if len(value) >= 8 else None
    return _number_value(text, question)


def deterministic_action(text: str, question: Question) -> DialogueAction:
    """Interpret common consultation language without requiring any model runtime."""
    normal = _normalise(text)
    if any(phrase in normal for phrase in _UNKNOWN):
        return DialogueAction(
            "unknown",
            question.question_id,
            acknowledgement="That is a perfectly valid answer; I will not invent it.",
            guidance=(
                "I’ll mark this as unknown and continue. If it becomes decisive, I’ll show you "
                "what evidence or reasonable range would resolve it."
            ),
        )
    if any(phrase in normal for phrase in _CONFUSED):
        return DialogueAction(
            "confused",
            question.question_id,
            acknowledgement="No problem—let’s make the decision simpler.",
            guidance=(
                f"{question.why_it_matters} You can answer approximately or ask me for an example."
            ),
        )
    if any(phrase in normal for phrase in _DEFER):
        return DialogueAction(
            "defer",
            question.question_id,
            acknowledgement="We can come back to that.",
            guidance="I’ll continue with another decision-relevant issue and keep this visible.",
        )
    if normal.startswith("why") or "why are you asking" in normal:
        return DialogueAction(
            "explain",
            question.question_id,
            acknowledgement="It is reasonable to ask why this matters.",
            guidance=question.expert_context or question.why_it_matters,
        )
    value = coerce_answer(text, question)
    if value is not None:
        return DialogueAction(
            "answer",
            question.question_id,
            value,
            "I’ve captured that as a confirmed part of your case.",
            question.expert_context or question.why_it_matters,
        )
    return DialogueAction(
        "discuss",
        question.question_id,
        acknowledgement="I understand the concern you are bringing to the decision.",
        guidance=(
            "I have kept your wording in the conversation, but I have not converted it into a "
            "confirmed fact. Let’s resolve the current issue without guessing."
        ),
    )


def validate_model_action(raw: dict[str, Any], question: Question, model_id: str) -> DialogueAction:
    """Validate a browser/model-proposed action before it can affect the case."""
    required = {"intent", "question_id", "value", "acknowledgement", "guidance"}
    if set(raw) != required:
        raise ValueError("dialogue action keys do not match the governed contract")
    intent = raw["intent"]
    if intent not in ALLOWED_INTENTS:
        raise ValueError("dialogue intent is not permitted")
    if raw["question_id"] != question.question_id:
        raise ValueError("dialogue action targeted a question outside the current turn")
    if not all(
        isinstance(raw[key], str) and raw[key].strip() for key in ("acknowledgement", "guidance")
    ):
        raise ValueError("model wording must be non-empty text")
    wording = f"{raw['acknowledgement']} {raw['guidance']}"
    if len(wording) > 900:
        raise ValueError("model wording exceeded the bounded turn size")
    prohibited = ("guaranteed", "definitely accept", "final verdict", "decision score")
    if any(phrase in wording.casefold() for phrase in prohibited):
        raise ValueError("model wording attempted an authoritative claim")
    value = raw["value"]
    if intent == "answer":
        if question.answer_type == "choice":
            if value not in question.options:
                raise ValueError("model proposed a choice outside the governed options")
        elif question.answer_type == "text":
            if not isinstance(value, str) or len(value.strip()) < 8 or len(value) > 2_000:
                raise ValueError("model proposed invalid bounded text")
        elif not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError("model proposed a non-numeric value")
        elif (question.minimum is not None and value < question.minimum) or (
            question.maximum is not None and value > question.maximum
        ):
            raise ValueError("model proposed a value outside the governed bounds")
    elif value is not None:
        raise ValueError("non-answer dialogue actions cannot persist a value")
    allowed_numbers = set(re.findall(r"\d+(?:\.\d+)?", str(value))) if value is not None else set()
    wording_numbers = set(re.findall(r"\d+(?:\.\d+)?", wording.replace(",", "")))
    if not wording_numbers.issubset(allowed_numbers):
        raise ValueError("model wording introduced an unsupported number")
    return DialogueAction(
        intent,
        question.question_id,
        value,
        raw["acknowledgement"].strip(),
        raw["guidance"].strip(),
        model_id,
    )


def apply_action(case: CaseKnowledgeAsset, action: DialogueAction) -> CaseKnowledgeAsset:
    if action.intent == "answer":
        source = "user via validated browser model" if action.model_id else "user"
        return case.record(
            action.question_id,
            action.value,
            status="confirmed",
            source=source,
            reason="Validated conversational answer",
        )
    statuses = {"unknown": "unknown", "uncertain": "uncertain", "defer": "deferred"}
    if action.intent in statuses:
        return case.mark(action.question_id, statuses[action.intent])
    return case


def browser_prompt(text: str, question: Question, case: CaseKnowledgeAsset) -> dict[str, Any]:
    """Build a compact serialisable prompt; the browser component owns no canonical state."""
    return {
        "user_message": text,
        "current_question": {
            "id": question.question_id,
            "prompt": question.prompt,
            "type": question.answer_type,
            "options": list(question.options),
            "minimum": question.minimum,
            "maximum": question.maximum,
            "why_it_matters": question.why_it_matters,
            "governed_implication": question.expert_context,
        },
        "confirmed_case": case.values,
        "required_output": {
            "intent": "answer|unknown|uncertain|defer|confused|explain|discuss",
            "question_id": question.question_id,
            "value": "governed answer or null",
            "acknowledgement": "concise natural acknowledgement",
            "guidance": "concise guidance using only supplied information",
        },
    }

"""Adaptive, governed dialogue policy for the virtual domain consultants."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from core.ai.contracts import GenerationRequest, LLMProvider
from plugin_sdk.decision import Question


@dataclass(frozen=True, slots=True)
class ExpertTurn:
    acknowledgement: str
    implication: str
    model_id: str | None = None
    prompt_hash: str | None = None


def select_next_question(
    product_id: str,
    questions: tuple[Question, ...],
    answers: dict[str, Any],
    excluded_ids: frozenset[str] = frozenset(),
) -> Question | None:
    """Choose the unresolved question with greatest current decision value."""
    unanswered = [
        question
        for question in questions
        if question.question_id not in answers and question.question_id not in excluded_ids
    ]
    if not unanswered:
        return None

    def value(question: Question) -> tuple[int, int]:
        score = question.importance
        key = question.question_id
        if product_id == "careersim":
            if answers.get("funding_plan") == "Substantial education loan":
                score += 25 if key in {"career_goal", "risk_tolerance"} else 0
            if answers.get("degree_level") == "PhD":
                score += 30 if key == "funding_plan" else 0
            if answers.get("target_region") and key == "career_goal":
                score += 15
        elif product_id == "housewise":
            if answers.get("financing") == "Stretched":
                score += 25 if key in {"budget_inr", "horizon_years"} else 0
            if answers.get("purpose") == "Long-term investment":
                score += 15 if key in {"priority", "horizon_years"} else 0
        elif product_id == "startup":
            if float(answers.get("runway_months", 99)) < 9:
                score += 30 if key in {"monthly_revenue_inr", "customer_evidence"} else 0
            if answers.get("stage") in {"Early traction", "Scaling"}:
                score += 15 if key in {"retention_pct", "gross_margin_pct"} else 0
        return score, -questions.index(question)

    return max(unanswered, key=value)


def deterministic_turn(question: Question, answer: Any) -> ExpertTurn:
    shown = str(answer)
    acknowledgement = f"I’ve recorded **{shown}**."
    tailored = {
        ("career_goal", "Work overseas long term"): (
            "I will test whether post-study work access and employment evidence are strong enough "
            "to support the overseas earning case."
        ),
        ("career_goal", "Work overseas then return to India"): (
            "I will value the initial overseas earning window but also test whether the degree "
            "still makes sense after returning to the Indian labour market."
        ),
        ("career_goal", "Return to India soon after graduation"): (
            "I will use the India-return income reference rather than justify the investment with "
            "an overseas salary headline."
        ),
        ("career_goal", "Research / academic career"): (
            "I will give greater weight to funded research pathways, supervision and academic "
            "depth than to immediate corporate salary."
        ),
        ("career_goal", "Undecided"): (
            "Because the earning market is unresolved, I will favour options that preserve "
            "mobility without requiring fragile debt assumptions."
        ),
        ("funding_plan", "Substantial education loan"): (
            "Debt-service resilience is now a central constraint; high-cost options must survive "
            "a delayed-employment and early-return-to-India scenario."
        ),
        ("funding_plan", "Dependent on scholarship / assistantship"): (
            "An option is not financially feasible until the funding is written and sufficiently "
            "durable, so conditional awards will be treated as unresolved evidence."
        ),
        ("financing", "Stretched"): (
            "This is a potential affordability veto: household resilience comes before an "
            "optimistic appreciation case."
        ),
        ("customer_evidence", "Interviews / assertion only"): (
            "The next recommendation must prioritise behavioural or paid validation before scale."
        ),
    }
    implication = tailored.get(
        (question.question_id, shown), question.expert_context or question.why_it_matters
    )
    return ExpertTurn(acknowledgement, implication)


def model_turn(
    question: Question,
    answer: Any,
    case_values: dict[str, Any],
    skill: str,
    provider: LLMProvider,
    model_id: str,
) -> ExpertTurn:
    """Generate non-authoritative expert wording over confirmed case facts."""
    payload = {
        "just_confirmed": {question.question_id: answer},
        "confirmed_case": case_values,
        "governed_implication": question.expert_context or question.why_it_matters,
    }
    request = GenerationRequest(
        task="word_consultant_turn",
        system_prompt=(
            f"{skill}\n\nRespond like a concise, thoughtful domain consultant. Use only the "
            "confirmed facts and governed implication supplied. Do not invent numbers, evidence, "
            "rules or recommendations. Return JSON with exactly acknowledgement and implication."
        ),
        user_prompt=json.dumps(payload, ensure_ascii=False),
        response_schema={"type": "object"},
        temperature=0.2,
    )
    generated = provider.generate(request, model_id=model_id)
    raw = json.loads(generated.text)
    if set(raw) != {"acknowledgement", "implication"}:
        raise ValueError("consultant wording violated the two-field contract")
    if not all(isinstance(raw[key], str) and raw[key].strip() for key in raw):
        raise ValueError("consultant wording must contain non-empty text")
    return ExpertTurn(
        raw["acknowledgement"].strip(),
        raw["implication"].strip(),
        generated.model_id,
        generated.prompt_hash,
    )

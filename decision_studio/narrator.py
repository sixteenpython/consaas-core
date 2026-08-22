"""Validated optional model narration over an immutable deterministic report."""

from __future__ import annotations

import json
from dataclasses import dataclass

from core.ai.contracts import GenerationRequest, LLMProvider
from plugin_sdk.decision import DecisionReport


@dataclass(frozen=True, slots=True)
class ConsultantNarrative:
    executive_summary: str
    challenge: str
    questions: tuple[str, ...]
    model_id: str
    prompt_hash: str


def narrate(
    report: DecisionReport,
    skill: str,
    provider: LLMProvider,
    model_id: str,
) -> ConsultantNarrative:
    frozen = {
        "verdict": report.verdict,
        "score": report.score,
        "confidence": report.confidence,
        "summary": report.summary,
        "options": [
            {"title": item.title, "score": item.score, "reasons": item.reasons, "risks": item.risks}
            for item in report.options
        ],
        "risks": report.risks,
        "next_actions": report.next_actions,
    }
    request = GenerationRequest(
        task="explain_validated_decision",
        system_prompt=(
            f"{skill}\n\nYou are wording an already-authoritative deterministic result. "
            "Do not change its verdict, score, options or facts. Return only JSON with keys "
            "executive_summary, challenge and questions (an array of exactly three strings)."
        ),
        user_prompt=json.dumps(frozen, ensure_ascii=False),
        response_schema={"type": "object"},
        temperature=0.1,
    )
    generated = provider.generate(request, model_id=model_id)
    raw = json.loads(generated.text)
    summary = raw.get("executive_summary")
    challenge = raw.get("challenge")
    questions = raw.get("questions")
    if not isinstance(summary, str) or not isinstance(challenge, str):
        raise ValueError("model narrative did not satisfy the text contract")
    if (
        not isinstance(questions, list)
        or len(questions) != 3
        or not all(isinstance(item, str) for item in questions)
    ):
        raise ValueError("model narrative did not supply exactly three questions")
    forbidden = {"verdict", "score", "options"}.intersection(raw)
    if forbidden:
        raise ValueError(f"model attempted to overwrite deterministic fields: {sorted(forbidden)}")
    return ConsultantNarrative(
        summary.strip(),
        challenge.strip(),
        tuple(item.strip() for item in questions),
        generated.model_id,
        generated.prompt_hash,
    )

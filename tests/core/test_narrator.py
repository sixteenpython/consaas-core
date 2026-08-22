from __future__ import annotations

import json

import pytest

from core.ai.contracts import GenerationRequest, GenerationResult
from decision_studio.narrator import narrate
from plugin_sdk.decision import DecisionReport


class FakeProvider:
    def __init__(self, payload: dict[str, object]) -> None:
        self.payload = payload

    def generate(self, request: GenerationRequest, *, model_id: str) -> GenerationResult:
        assert "do not change" in request.system_prompt.lower()
        return GenerationResult(json.dumps(self.payload), model_id, "fake", 1, "abc123")


def _report() -> DecisionReport:
    return DecisionReport(
        "careersim",
        "CONDITIONAL",
        64.0,
        "Medium",
        "Foundation",
        "Summary",
        (),
        (),
        (),
        (),
        (),
        (),
        {},
        "asset-1",
        "2026-08-22",
        "hash",
        "0.1.0",
    )


def test_narrator_accepts_only_non_authoritative_explanation() -> None:
    result = narrate(
        _report(),
        "Skill",
        FakeProvider(
            {
                "executive_summary": "The trade-off is clear.",
                "challenge": "Verify the downside.",
                "questions": ["One?", "Two?", "Three?"],
            }
        ),
        "open-model",
    )
    assert result.challenge == "Verify the downside."


def test_narrator_rejects_attempt_to_overwrite_verdict() -> None:
    with pytest.raises(ValueError, match="overwrite"):
        narrate(
            _report(),
            "Skill",
            FakeProvider(
                {
                    "executive_summary": "Changed.",
                    "challenge": "None.",
                    "questions": ["One?", "Two?", "Three?"],
                    "verdict": "BUY",
                }
            ),
            "open-model",
        )

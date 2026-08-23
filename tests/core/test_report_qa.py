from __future__ import annotations

from decision_studio.report_qa import answer_report_question, report_to_markdown
from plugin_sdk.decision import DecisionReport, ScoredOption


def _report() -> DecisionReport:
    option = ScoredOption("one", "Best move", 75, "Strong fit", ("Reason one",), (), (), {})
    return DecisionReport(
        "careersim", "GO", 75, "High", "Sufficient", "Proceed carefully.", (option,),
        ("Risk one",), ("Assumption one",), ("Verify the offer",), ("Cost rises",),
        ("Source one",), {}, "artifact", "2026-08-23", "a" * 64, "1.0",
    )


def test_follow_up_retrieves_frozen_report_evidence() -> None:
    assert "Source one" in answer_report_question(_report(), "Show me the evidence")
    assert "Risk one" in answer_report_question(_report(), "What could go wrong?")


def test_plain_english_download_contains_verdict_and_provenance() -> None:
    rendered = report_to_markdown(_report())
    assert "## Verdict: GO" in rendered
    assert "`artifact`" in rendered

from __future__ import annotations

from pathlib import Path

from decision_studio.service import DecisionStudio
from tests.integration.test_decision_studio import _strong_startup_case

ROOT = Path(__file__).parents[2]


def test_careersim_returns_three_robust_scenario_ranked_paths() -> None:
    answers = {
        "degree_level": "Master's",
        "field": "Data / AI",
        "target_region": "Multiple regions",
        "budget_inr": 6_500_000,
        "funding_plan": "Mixed family funding and modest loan",
        "academic_readiness": "Competitive",
        "career_goal": "Work overseas then return to India",
        "priority": "Downside-adjusted financial ROI",
        "risk_tolerance": "Moderate",
    }
    service = DecisionStudio(ROOT)
    first = service.decide("careersim", answers)
    second = service.decide("careersim", answers)
    assert len(first.options) == 3
    assert [item.title for item in first.options] == [item.title for item in second.options]
    metrics = first.options[0].metrics
    assert metrics["downside incremental NPV ₹"] <= metrics["base incremental NPV ₹"]
    assert metrics["base incremental NPV ₹"] <= metrics["upside incremental NPV ₹"]
    assert "base incremental IRR %" in metrics


def test_housewise_returns_three_diligence_zones_with_ordered_scenarios() -> None:
    answers = {
        "city": "Bengaluru",
        "purpose": "Both home and investment",
        "budget_inr": 15_000_000,
        "size_sqft": 1000,
        "horizon_years": 10,
        "financing": "Comfortable buffer",
        "priority": "Capital preservation",
        "risk_tolerance": "Low",
    }
    report = DecisionStudio(ROOT).decide("housewise", answers)
    assert len(report.options) == 3
    metrics = report.options[0].metrics
    assert metrics["downside leveraged equity IRR %"] <= metrics["base leveraged equity IRR %"]
    assert metrics["base leveraged equity IRR %"] <= metrics["upside leveraged equity IRR %"]
    assert "no exact title or project has been approved" in report.data_sufficiency


def test_startupeval_consaas_reference_is_strong_but_vague_case_is_not() -> None:
    service = DecisionStudio(ROOT)
    strong = service.decide("startup", _strong_startup_case())
    vague = service.decide(
        "startup",
        {
            key: "We have an idea and believe it will probably work but have no evidence yet."
            for key in _strong_startup_case()
        },
    )
    assert strong.verdict == "STRONG"
    assert strong.summary.startswith("GO—but fund the next proof milestone")
    assert strong.options[0].title.startswith("GO —")
    assert "low semantic overlap" not in " ".join(strong.risks)
    assert (
        strong.options[0].metrics["Horse (business model)"]
        > strong.options[0].metrics["Jockey (founder execution)"]
    )
    assert vague.verdict != "STRONG"
    assert vague.score < strong.score
    assert "weakest point" in vague.risks[0]

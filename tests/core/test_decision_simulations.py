from __future__ import annotations

from itertools import product
from pathlib import Path

from decision_studio.service import DecisionStudio

ROOT = Path(__file__).parents[2]


def test_career_and_house_decision_surface_simulations() -> None:
    service = DecisionStudio(ROOT)
    observed = 0
    for degree, field, budget, funding, goal in product(
        ("Undergraduate", "Master's", "PhD"),
        ("Engineering / technology", "Data / AI", "Business / management"),
        (3_000_000, 6_500_000, 15_000_000),
        (
            "Family-funded with little or no debt",
            "Mixed family funding and modest loan",
            "Substantial education loan",
        ),
        (
            "Work overseas long term",
            "Work overseas then return to India",
            "Return to India soon after graduation",
        ),
    ):
        report = service.decide(
            "careersim",
            {
                "degree_level": degree,
                "field": field,
                "target_region": "Multiple regions",
                "budget_inr": budget,
                "funding_plan": funding,
                "academic_readiness": "Competitive",
                "career_goal": goal,
                "priority": "Downside-adjusted financial ROI",
                "risk_tolerance": "Moderate",
            },
        )
        assert 0 <= report.score <= 100
        assert len(report.options) <= 3
        observed += 1

    for city, budget, horizon, financing in product(
        ("Bengaluru", "Mumbai", "Pune", "Hyderabad", "Chennai", "Delhi NCR", "Kolkata"),
        (7_500_000, 15_000_000, 30_000_000),
        (3, 8, 15),
        ("Comfortable buffer", "Manageable", "Stretched"),
    ):
        report = service.decide(
            "housewise",
            {
                "city": city,
                "purpose": "Both home and investment",
                "budget_inr": budget,
                "size_sqft": 1000,
                "horizon_years": horizon,
                "financing": financing,
                "priority": "Capital preservation",
                "risk_tolerance": "Low",
            },
        )
        assert 0 <= report.score <= 100
        assert len(report.options) <= 3
        observed += 1

    assert observed == 432

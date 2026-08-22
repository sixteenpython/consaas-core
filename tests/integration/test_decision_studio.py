from __future__ import annotations

from pathlib import Path

import pytest

from decision_studio.service import DecisionStudio

ROOT = Path(__file__).parents[2]


@pytest.mark.integration
@pytest.mark.parametrize(
    ("product_id", "answers"),
    [
        (
            "careersim",
            {
                "degree_level": "Postgraduate",
                "field": "Data / AI",
                "budget_inr": 2500000,
                "geography": "India or overseas",
                "academic_readiness": "Competitive",
                "priority": "Career outcomes",
                "risk_tolerance": "Moderate",
            },
        ),
        (
            "housewise",
            {
                "city": "Bengaluru",
                "purpose": "Both home and investment",
                "budget_inr": 15000000,
                "size_sqft": 1000,
                "horizon_years": 10,
                "financing": "Comfortable buffer",
                "priority": "Capital preservation",
                "risk_tolerance": "Low",
            },
        ),
        (
            "startup",
            {
                "role": "Founder",
                "stage": "Early traction",
                "sector": "Enterprise software",
                "monthly_revenue_inr": 1400000,
                "monthly_growth_pct": 14,
                "retention_pct": 84,
                "gross_margin_pct": 80,
                "runway_months": 16,
                "customer_evidence": "Repeated paid use",
                "team_strength": "Strong with one key gap",
                "regulatory_risk": "Low",
            },
        ),
    ],
)
def test_each_product_builds_an_explainable_recommendation(
    product_id: str, answers: dict[str, object]
) -> None:
    report = DecisionStudio(ROOT).decide(product_id, answers)

    assert report.product_id == product_id
    assert report.verdict
    assert 0 <= report.score <= 100
    assert len(report.options) >= 2
    assert report.next_actions
    assert report.change_conditions
    assert report.gka_artifact_id.startswith(product_id)
    assert len(report.gka_hash) == 64


def test_declared_priority_and_role_change_the_prescription() -> None:
    service = DecisionStudio(ROOT)
    career = {
        "degree_level": "Postgraduate",
        "field": "Data / AI",
        "budget_inr": 2500000,
        "geography": "India or overseas",
        "academic_readiness": "Competitive",
        "priority": "Career outcomes",
        "risk_tolerance": "Moderate",
    }
    outcomes = service.decide("careersim", career)
    low_debt = service.decide("careersim", {**career, "priority": "Low debt"})
    assert outcomes.score != low_debt.score

    startup = {
        "role": "Founder",
        "stage": "Early traction",
        "sector": "Enterprise software",
        "monthly_revenue_inr": 1400000,
        "monthly_growth_pct": 14,
        "retention_pct": 84,
        "gross_margin_pct": 80,
        "runway_months": 16,
        "customer_evidence": "Repeated paid use",
        "team_strength": "Strong with one key gap",
        "regulatory_risk": "Low",
    }
    founder = service.decide("startup", startup)
    investor = service.decide("startup", {**startup, "role": "Investor"})
    assert founder.next_actions != investor.next_actions

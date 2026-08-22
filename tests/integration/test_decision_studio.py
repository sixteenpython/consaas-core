from __future__ import annotations

from pathlib import Path

import pytest

from decision_studio.catalog import load_metric_catalog
from decision_studio.service import DecisionStudio

ROOT = Path(__file__).parents[2]


@pytest.mark.integration
@pytest.mark.parametrize(
    ("product_id", "answers"),
    [
        (
            "careersim",
            {
                "degree_level": "Master's",
                "field": "Data / AI",
                "target_region": "Multiple regions",
                "budget_inr": 6500000,
                "funding_plan": "Mixed family funding and modest loan",
                "academic_readiness": "Competitive",
                "career_goal": "Work overseas then return to India",
                "priority": "Downside-adjusted financial ROI",
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
        "degree_level": "Master's",
        "field": "Data / AI",
        "target_region": "Multiple regions",
        "budget_inr": 6500000,
        "funding_plan": "Mixed family funding and modest loan",
        "academic_readiness": "Competitive",
        "career_goal": "Work overseas then return to India",
        "priority": "Career acceleration",
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


def test_unknown_fact_blocks_reassessment_after_unrelated_revision() -> None:
    service = DecisionStudio(ROOT)
    incomplete_startup = {
        "role": "Founder",
        "stage": "Scaling",
        "sector": "Fintech",
        "monthly_revenue_inr": 500000,
        "monthly_growth_pct": 8,
        "retention_pct": 65,
        "gross_margin_pct": 55,
        "customer_evidence": "Repeated paid use",
        "team_strength": "Complete and proven",
        "regulatory_risk": "Low",
    }

    # Runway is explicitly unknown, so revising role must not call the Startup engine.
    revised = {**incomplete_startup, "role": "Investor"}
    assert service.missing_answers("startup", revised) == ("runway_months",)
    assert service.decide_if_ready("startup", revised) is None
    with pytest.raises(ValueError, match="runway_months"):
        service.decide("startup", revised)

    # Older anonymous sessions may retain an explicit null for an unresolved fact.
    null_runway = {**revised, "runway_months": None}
    assert service.missing_answers("startup", null_runway) == ("runway_months",)
    assert service.decide_if_ready("startup", null_runway) is None


@pytest.mark.parametrize("product_id", ["careersim", "housewise", "startup"])
def test_each_promoted_gka_declares_broad_decision_coverage(product_id: str) -> None:
    catalog = load_metric_catalog(ROOT, product_id)
    metrics = catalog["metrics"]

    assert len(metrics) >= 20
    assert {item["coverage"] for item in metrics}.issubset(
        {"available", "planned_connector", "required_case_evidence"}
    )
    assert all(item["decision_use"] and item["preferred_source"] for item in metrics)

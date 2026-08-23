from __future__ import annotations

from pathlib import Path

import pytest

from decision_studio.catalog import load_metric_catalog
from decision_studio.service import DecisionStudio

ROOT = Path(__file__).parents[2]


def _strong_startup_case() -> dict[str, object]:
    return {
        "problem_customer": (
            "Indian founders and small advisory teams making costly education, property and "
            "startup decisions lack affordable evidence-backed advice; we are scaling a working "
            "decision-intelligence studio."
        ),
        "problem_evidence": (
            "We observed repeated user sessions across three live products. Customers used the "
            "recommendations, returned for monthly decisions and tested 30 structured "
            "consultations with completed decision briefs."
        ),
        "problem_cost": (
            "A wrong overseas degree can destroy ₹40–80 lakh, a weak property choice can lock "
            "capital for 10 years, and founders spend months building before testing demand."
        ),
        "current_alternatives": (
            "Customers use fragmented portals, sales-led advisers and generic chatbots. These "
            "show information or fluent prose but do not preserve evidence, quantify downside "
            "or expose a reproducible verdict trail."
        ),
        "payer_evidence": (
            "The user or advisory institution pays. We observed repeat product use and explicit "
            "willingness to pay for verified briefs; the next pilot tests paid conversion at "
            "₹999 with 50 qualified users."
        ),
        "solution_outcome": (
            "ConSaaS converts a case into a versioned knowledge asset, runs deterministic domain "
            "engines and produces three evidence-linked options. The measurable outcome is fewer "
            "irreversible decisions made with fatal unknowns unresolved."
        ),
        "traction_evidence": (
            "We built and launched Vriddhi, Narrative Architect and Decision Studio, measured "
            "repeat usage, completed 30 guided cases and retained 65% of pilot users over the "
            "relevant repeat period."
        ),
        "business_economics": (
            "We acquire through domain content and institutional pilots, serve with deterministic "
            "engines plus optional open-weight language models, charge per brief or subscription, "
            "and target 80% gross margin with repeat usage."
        ),
        "founder_fit": (
            "The team has built, shipped and operated multiple decision products in investments, "
            "education and narrative diagnosis, and has direct access to Indian students, "
            "founders and household decision makers."
        ),
        "execution_learning": (
            "We launched an early rigid questionnaire, observed confusion, then changed it into a "
            "canonical conversational case model. We tested the revised flow and improved "
            "completion across 30 guided sessions."
        ),
        "risk_milestone": (
            "The fatal risk is paid repeat demand. Over 8 weeks and a ₹2 lakh budget we will test "
            "50 qualified users; pass means 15 paid briefs and 40% repeat intent, otherwise we "
            "narrow the segment."
        ),
    }


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
            _strong_startup_case(),
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


def test_declared_priority_and_evidence_change_the_prescription() -> None:
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

    strong = _strong_startup_case()
    evidenced = service.decide("startup", strong)
    asserted = service.decide(
        "startup",
        {
            **strong,
            "payer_evidence": "We believe people will probably pay, but we have not tested it.",
        },
    )
    assert evidenced.score > asserted.score
    assert evidenced.verdict == "STRONG"
    assert asserted.verdict != "STRONG"


def test_unknown_fact_blocks_reassessment_after_unrelated_revision() -> None:
    service = DecisionStudio(ROOT)
    incomplete_startup = _strong_startup_case()
    incomplete_startup.pop("risk_milestone")

    # The milestone is explicitly unknown, so revising another fact must not call the engine.
    revised = {
        **incomplete_startup,
        "problem_customer": str(incomplete_startup["problem_customer"]) + " Revised.",
    }
    assert service.missing_answers("startup", revised) == ("risk_milestone",)
    assert service.decide_if_ready("startup", revised) is None
    with pytest.raises(ValueError, match="risk_milestone"):
        service.decide("startup", revised)

    # Older anonymous sessions may retain an explicit null for an unresolved fact.
    null_milestone = {**revised, "risk_milestone": None}
    assert service.missing_answers("startup", null_milestone) == ("risk_milestone",)
    assert service.decide_if_ready("startup", null_milestone) is None


@pytest.mark.parametrize("product_id", ["careersim", "housewise", "startup"])
def test_each_promoted_gka_declares_broad_decision_coverage(product_id: str) -> None:
    catalog = load_metric_catalog(ROOT, product_id)
    metrics = catalog["metrics"]

    assert len(metrics) >= 20
    assert {item["coverage"] for item in metrics}.issubset(
        {"available", "planned_connector", "required_case_evidence"}
    )
    assert all(item["decision_use"] and item["preferred_source"] for item in metrics)

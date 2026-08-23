from __future__ import annotations

import json
from pathlib import Path

from decision_studio.service import DecisionStudio

ROOT = Path(__file__).parents[2]


def test_every_promoted_universe_row_is_precomputed_once() -> None:
    for product_id in ("careersim", "housewise", "startup"):
        current = json.loads(
            (ROOT / "knowledge" / "releases" / product_id / "current.json").read_text()
        )
        release = ROOT / current["release_path"]
        atlas = json.loads((release / "decision_atlas.json").read_text())
        scenarios = json.loads((release / "scenario_matrix.json").read_text())
        rows = (release / "grand_knowledge_asset.csv").read_text().splitlines()[1:]
        atlas_ids = [item["record_id"] for item in atlas["entries"]]
        scenario_ids = [item["record_id"] for item in scenarios]
        assert atlas["universe_size"] == len(rows) == len(atlas_ids)
        assert len(atlas_ids) == len(set(atlas_ids))
        assert set(atlas_ids) == set(scenario_ids)
        assert all(item["downside"] <= item["base"] <= item["upside"] for item in scenarios)


def test_customer_decision_copy_leads_with_action_not_engine_jargon() -> None:
    service = DecisionStudio(ROOT)
    cases = {
        "careersim": {
            "degree_level": "Master's",
            "field": "Data / AI",
            "target_region": "Multiple regions",
            "budget_inr": 6_500_000,
            "funding_plan": "Mixed family funding and modest loan",
            "academic_readiness": "Competitive",
            "career_goal": "Work overseas then return to India",
            "priority": "Downside-adjusted financial ROI",
            "risk_tolerance": "Moderate",
        },
        "housewise": {
            "city": "Bengaluru",
            "purpose": "Both home and investment",
            "budget_inr": 15_000_000,
            "size_sqft": 1_000,
            "horizon_years": 10,
            "financing": "Comfortable buffer",
            "priority": "Capital preservation",
            "risk_tolerance": "Low",
        },
    }
    allowed = {
        "GO",
        "ADJUST",
        "DO NOT INVEST YET",
        "BUY ONLY IF ADJUSTED",
        "BUY",
        "RENT/WAIT",
        "WAIT",
    }
    for product_id, answers in cases.items():
        report = service.decide(product_id, answers)
        lead = f"{report.summary} {report.next_actions[0]}".casefold()
        assert any(report.summary.startswith(prefix) for prefix in allowed)
        assert not any(term in lead for term in ("decision atlas", "pareto", "feature matrix"))
        assert report.options[0].title in report.summary


def test_wait_cases_give_an_explicit_do_not_commit_action() -> None:
    service = DecisionStudio(ROOT)
    career = service.decide(
        "careersim",
        {
            "degree_level": "Master's",
            "field": "Data / AI",
            "target_region": "United States",
            "budget_inr": 1_000_000,
            "funding_plan": "Substantial education loan",
            "academic_readiness": "Competitive",
            "career_goal": "Work overseas long term",
            "priority": "Downside-adjusted financial ROI",
            "risk_tolerance": "Low",
        },
    )
    house = service.decide(
        "housewise",
        {
            "city": "Mumbai",
            "purpose": "Primary home",
            "budget_inr": 2_000_000,
            "size_sqft": 4_000,
            "horizon_years": 10,
            "financing": "Stretched",
            "priority": "Capital preservation",
            "risk_tolerance": "Low",
        },
    )
    assert career.verdict.startswith("WAIT")
    assert career.next_actions[0].startswith("Do not borrow")
    assert house.verdict.startswith("WAIT")
    assert house.next_actions[0].startswith("Do not pay")

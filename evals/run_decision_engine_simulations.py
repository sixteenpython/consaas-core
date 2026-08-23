"""Deterministic release simulation matrix for Decision Studio v0.4."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from decision_studio.service import DecisionStudio
from plugin_sdk.decision import DecisionReport
from tests.integration.test_decision_studio import _strong_startup_case

ROOT = Path(__file__).parents[1]


def _rows(product_id: str) -> list[dict[str, str]]:
    with (ROOT / product_id / "data" / "seed.csv").open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _check_report(report: DecisionReport) -> None:
    _require(0 <= report.score <= 100, "report score escaped bounds")
    _require(len(report.options) <= 3, "report option count escaped bounds")
    _require(
        bool(report.options) or report.verdict.startswith("WAIT"), "empty options without WAIT"
    )
    _require(
        all(0 <= option.score <= 100 for option in report.options),
        "option score escaped bounds",
    )
    _require(bool(report.evidence), "report lost provenance")


def run() -> dict[str, object]:
    service = DecisionStudio(ROOT)
    outcomes: dict[str, Counter[str]] = {
        "careersim": Counter(),
        "housewise": Counter(),
        "startup": Counter(),
    }
    count = 0
    for row in _rows("careersim"):
        for budget in (4_000_000, 8_000_000):
            for funding in (
                "Family-funded with little or no debt",
                "Mixed family funding and modest loan",
            ):
                for risk in ("Low", "Moderate", "High"):
                    answers = {
                        "degree_level": row["degree_level"],
                        "field": row["field"],
                        "target_region": row["target_region"],
                        "budget_inr": budget,
                        "funding_plan": funding,
                        "academic_readiness": "Competitive",
                        "career_goal": "Work overseas then return to India",
                        "priority": "Downside-adjusted financial ROI",
                        "risk_tolerance": risk,
                    }
                    report = service.decide("careersim", answers)
                    _check_report(report)
                    if not report.options:
                        outcomes["careersim"][report.verdict] += 1
                        count += 1
                        continue
                    metrics = report.options[0].metrics
                    _require(
                        metrics["downside incremental NPV ₹"]
                        <= metrics["base incremental NPV ₹"]
                        <= metrics["upside incremental NPV ₹"],
                        "CareerSim scenario order failed",
                    )
                    outcomes["careersim"][report.verdict] += 1
                    count += 1

    go_case = {
        "degree_level": "Master's",
        "field": "Data / AI",
        "target_region": "Multiple regions",
        "budget_inr": 12_000_000,
        "funding_plan": "Family-funded with little or no debt",
        "academic_readiness": "Strong",
        "career_goal": "Work overseas long term",
        "priority": "Career acceleration",
        "risk_tolerance": "High",
    }
    go_report = service.decide("careersim", go_case)
    _require(go_report.verdict.startswith("GO"), "CareerSim positive calibration gate failed")
    outcomes["careersim"][go_report.verdict] += 1
    count += 1

    for row in _rows("housewise"):
        for financing in ("Comfortable buffer", "Manageable", "Stretched"):
            for risk in ("Low", "Moderate", "High"):
                answers = {
                    "city": row["city"],
                    "purpose": "Both home and investment",
                    "budget_inr": 15_000_000,
                    "size_sqft": 1000,
                    "horizon_years": 10,
                    "financing": financing,
                    "priority": "Capital preservation",
                    "risk_tolerance": risk,
                }
                report = service.decide("housewise", answers)
                _check_report(report)
                metrics = report.options[0].metrics
                _require(
                    metrics["downside leveraged equity IRR %"]
                    <= metrics["base leveraged equity IRR %"]
                    <= metrics["upside leveraged equity IRR %"],
                    "HouseWise scenario order failed",
                )
                if financing == "Stretched":
                    _require(
                        report.verdict.startswith("RENT/WAIT"),
                        "stretched financing gate failed",
                    )
                outcomes["housewise"][report.verdict] += 1
                count += 1

    strong = _strong_startup_case()
    startup_cases = (
        strong,
        {**strong, "payer_evidence": "We believe users might pay but have not tested payment."},
        {key: "We have an idea and hope it works, but there is no evidence yet." for key in strong},
    )
    for answers in startup_cases:
        report = service.decide("startup", answers)
        _check_report(report)
        outcomes["startup"][report.verdict] += 1
        count += 1
    _require(outcomes["startup"]["STRONG"] == 1, "StartupEval calibration gate failed")
    return {
        "simulation_count": count,
        "outcomes": {key: dict(value) for key, value in outcomes.items()},
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, ensure_ascii=True))

"""Exhaust bounded Decision Studio surfaces and fail on nonsensical reports.

This evaluation calls the frozen product engines directly so thousands of cases can be
replayed quickly without repeatedly loading the same promoted release from disk.
"""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Callable
from itertools import product
from pathlib import Path
from typing import Any

from careersim.decision import decide as decide_career
from decision_studio.catalog import load_current_gka, load_decision_atlas, load_policy
from housewise.decision import decide as decide_house
from plugin_sdk.decision import DecisionReport
from startup.decision import decide as decide_startup

ROOT = Path(__file__).parents[1]
INTERNAL_JARGON = ("decision atlas", "pareto", "precomputed pathway", "feature matrix")


def _engine(
    product_id: str, function: Callable[..., DecisionReport]
) -> Callable[[dict[str, Any]], DecisionReport]:
    rows, manifest = load_current_gka(ROOT, product_id)
    atlas = load_decision_atlas(ROOT, product_id)
    policy = load_policy(ROOT, product_id)
    return lambda answers: function(answers, rows, policy, manifest, atlas)


def _report_failures(report: DecisionReport) -> list[str]:
    failures: list[str] = []
    if not 0 <= report.score <= 100:
        failures.append("score outside 0..100")
    if len(report.options) > 3:
        failures.append("more than three recommended moves")
    if not report.summary or not report.next_actions:
        failures.append("missing plain-English summary or call to action")
    customer_copy = f"{report.summary} {report.next_actions[0]}".casefold()
    if any(term in customer_copy for term in INTERNAL_JARGON):
        failures.append("customer-facing decision leads with implementation jargon")
    if report.options and len({item.option_id for item in report.options}) != len(report.options):
        failures.append("duplicate recommended option")
    for item in report.options:
        if len(item.reasons) < 2 or not item.metrics or not item.evidence:
            failures.append(f"{item.option_id} lacks reasons, numbers or evidence")
    if not report.options and "WAIT" not in report.verdict:
        failures.append("no feasible option without an explicit WAIT verdict")
    return failures


def _strong_startup() -> dict[str, str]:
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


def main() -> int:
    career = _engine("careersim", decide_career)
    house = _engine("housewise", decide_house)
    startup = _engine("startup", decide_startup)
    counts: Counter[str] = Counter()
    failures: list[str] = []

    for values in product(
        ("Undergraduate", "Master's", "PhD"),
        (
            "Engineering / technology",
            "Business / management",
            "Data / AI",
            "Healthcare / life sciences",
            "Social sciences / public policy",
            "Flexible / undecided",
        ),
        ("United States", "Canada", "United Kingdom", "Europe", "Australia", "Multiple regions"),
        (1_000_000, 6_500_000, 30_000_000),
        (
            "Family-funded with little or no debt",
            "Mixed family funding and modest loan",
            "Substantial education loan",
            "Dependent on scholarship / assistantship",
        ),
        (
            "Work overseas long term",
            "Work overseas then return to India",
            "Return to India soon after graduation",
            "Research / academic career",
            "Undecided",
        ),
        ("Low", "Moderate", "High"),
    ):
        answer = dict(
            zip(
                (
                    "degree_level",
                    "field",
                    "target_region",
                    "budget_inr",
                    "funding_plan",
                    "career_goal",
                    "risk_tolerance",
                ),
                values,
                strict=True,
            )
        )
        answer |= {
            "academic_readiness": "Competitive",
            "priority": "Downside-adjusted financial ROI",
        }
        report = career(answer)
        counts[f"careersim:{report.verdict.split('—')[0].strip()}"] += 1
        failures.extend(f"CareerSim: {item}" for item in _report_failures(report))

    for values in product(
        ("Bengaluru", "Mumbai", "Pune", "Hyderabad", "Chennai", "Delhi NCR", "Kolkata"),
        ("Primary home", "Long-term investment", "Both home and investment"),
        (2_000_000, 15_000_000, 100_000_000),
        (400, 1_000, 4_000),
        (1, 5, 10, 30),
        ("Comfortable buffer", "Manageable", "Stretched"),
        ("Low", "Moderate", "High"),
    ):
        answer = dict(
            zip(
                (
                    "city",
                    "purpose",
                    "budget_inr",
                    "size_sqft",
                    "horizon_years",
                    "financing",
                    "risk_tolerance",
                ),
                values,
                strict=True,
            )
        )
        answer["priority"] = "Capital preservation"
        report = house(answer)
        counts[f"housewise:{report.verdict.split('—')[0].strip()}"] += 1
        failures.extend(f"HouseWise: {item}" for item in _report_failures(report))
        if (
            answer["financing"] == "Stretched"
            and report.options
            and not report.verdict.startswith("RENT/WAIT")
        ):
            failures.append("HouseWise: stretched financing escaped the RENT/WAIT veto")
        if answer["horizon_years"] == 1 and report.verdict.startswith("BUY —"):
            failures.append("HouseWise: one-year holding period received an unconditional BUY")

    strong = _strong_startup()
    startup_cases = {
        "strong": strong,
        "vague": {key: "I have an idea but I do not know yet." for key in strong},
        "no_payer": strong
        | {
            "payer_evidence": (
                "Nobody has paid and we do not know who would pay; this is only our belief."
            )
        },
        "no_learning": strong
        | {
            "execution_learning": (
                "We have not built or tested anything and have not changed our view."
            )
        },
        "no_problem_proof": strong
        | {
            "problem_evidence": (
                "This is our belief; we have not observed, interviewed or tested anyone yet."
            )
        },
    }
    expected = {"strong": "STRONG", "vague": "FORGET IT"}
    for name, answer in startup_cases.items():
        report = startup(answer)
        counts[f"startup:{report.verdict.split('—')[0].strip()}"] += 1
        failures.extend(f"StartupEval {name}: {item}" for item in _report_failures(report))
        if name in expected and not report.verdict.startswith(expected[name]):
            failures.append(f"StartupEval {name}: expected {expected[name]}, got {report.verdict}")
        if name in {"no_payer", "no_learning", "no_problem_proof"} and report.verdict == "STRONG":
            failures.append(f"StartupEval {name}: critical evidence failure still received STRONG")

    result = {
        "cases_evaluated": sum(counts.values()),
        "verdict_distribution": dict(sorted(counts.items())),
        "failures": failures[:50],
        "failure_count": len(failures),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

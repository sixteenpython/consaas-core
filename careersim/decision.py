"""CareerSim deterministic education-investment simulation and optimisation engine."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.optimization import (
    bounded,
    internal_rate_of_return,
    pareto_front,
    present_value,
    ranking_stability,
)
from plugin_sdk.decision import DecisionReport, ScoredOption


@dataclass(frozen=True, slots=True)
class CareerCandidate:
    option: ScoredOption
    objectives: dict[str, float]


def _number(row: dict[str, str], key: str) -> float:
    return float(row[key])


def _lakhs(value: float) -> str:
    return f"₹{value / 100000:.1f} lakh"


def _salary_band(row: dict[str, str], career_goal: str) -> tuple[float, float, float]:
    overseas = (
        _number(row, "salary_p10_inr"),
        _number(row, "salary_p50_inr"),
        _number(row, "salary_p90_inr"),
    )
    if career_goal == "Return to India soon after graduation":
        midpoint = _number(row, "india_return_salary_inr")
        return midpoint * 0.72, midpoint, midpoint * 1.45
    if career_goal == "Work overseas then return to India":
        india = _number(row, "india_return_salary_inr")
        return tuple((value + india) / 2 for value in overseas)  # type: ignore[return-value]
    if career_goal == "Research / academic career":
        return tuple(value * 0.82 for value in overseas)  # type: ignore[return-value]
    return overseas


def _incremental_cashflows(
    economic_cost: float, salary: float, counterfactual: float, tax_rate: float
) -> tuple[float, ...]:
    premium = salary * (1 - tax_rate) - counterfactual
    return (-economic_cost, *(premium * 1.05**year for year in range(10)))


def _candidate(
    row: dict[str, str],
    answers: dict[str, Any],
    budget: float,
    atlas_entry: dict[str, Any],
) -> CareerCandidate | None:
    if row["degree_level"] != answers["degree_level"]:
        return None
    if answers["field"] != "Flexible / undecided" and row["field"] not in {
        answers["field"],
        "Flexible / undecided",
    }:
        return None
    if (
        answers["target_region"] != "Multiple regions"
        and row["target_region"] != answers["target_region"]
    ):
        return None
    cost = _number(row, "total_cost_inr")
    funded = row["funding_model"] in {"Funded", "Usually stipend-funded", "Usually salaried"}
    if cost > budget * 1.5 and not funded:
        return None
    duration = _number(row, "duration_years")
    counterfactual = _number(row, "counterfactual_salary_inr")
    economic_cost = cost + counterfactual * duration
    salary_band = _salary_band(row, str(answers["career_goal"]))
    tax_rate = _number(row, "tax_rate_pct") / 100
    cashflows = tuple(
        _incremental_cashflows(economic_cost, salary, counterfactual, tax_rate)
        for salary in salary_band
    )
    npvs = tuple(present_value(flow, 0.08) for flow in cashflows)
    base_irr = internal_rate_of_return(cashflows[1])
    outcome_probability = (
        _number(row, "completion_probability_pct")
        / 100
        * _number(row, "employment_probability_score")
        / 100
    )
    positive_probability = (
        0.88 if npvs[0] > 0 else 0.68 if npvs[1] > 0 else 0.38 if npvs[2] > 0 else 0.12
    ) * outcome_probability
    affordability = bounded(budget / max(cost, 1) * 100)
    loan_ratio = {
        "Family-funded with little or no debt": 0.08,
        "Mixed family funding and modest loan": 0.35,
        "Substantial education loan": 0.70,
        "Dependent on scholarship / assistantship": 0.45,
    }[str(answers["funding_plan"])]
    if funded:
        loan_ratio *= 0.2
    debt = cost * loan_ratio
    debt_resilience = bounded(100 - debt / max(salary_band[1] * (1 - tax_rate), 1) * 34)
    downside_score = bounded(50 + npvs[0] / max(economic_cost, 1) * 35)
    value_score = bounded(50 + npvs[1] / max(economic_cost, 1) * 32)
    evidence = _number(row, "evidence_score")
    work_rights = _number(row, "work_rights_score")
    quality = _number(row, "quality_score")
    risk_fit = bounded(
        100
        - (_number(row, "risk_score") + _number(row, "visa_uncertainty_score"))
        / 2
        * {"Low": 1.2, "Moderate": 1.0, "High": 0.8}[str(answers["risk_tolerance"])]
    )
    score = (
        positive_probability * 100 * 0.23
        + value_score * 0.18
        + downside_score * 0.14
        + affordability * 0.13
        + debt_resilience * 0.10
        + work_rights * 0.07
        + quality * 0.05
        + risk_fit * 0.06
        + evidence * 0.04
    )
    priority_score = {
        "Downside-adjusted financial ROI": (downside_score + value_score + debt_resilience) / 3,
        "Career acceleration": _number(row, "employability_score"),
        "Low debt": (affordability + debt_resilience) / 2,
        "Academic depth": quality,
        "International mobility": work_rights,
        "Long-term optionality": (quality + work_rights + risk_fit) / 3,
    }[str(answers["priority"])]
    score = bounded(score + (priority_score - 50) * 0.08)
    adjustment = max(0.0, cost - budget)
    fit = "Investable within ceiling" if adjustment == 0 else "Adjust funding or option"
    risks = [row["notes"]]
    if adjustment:
        risks.append(f"The current all-in estimate exceeds the ceiling by ₹{adjustment:,.0f}.")
    if npvs[0] < 0:
        risks.append("The downside scenario does not recover the full economic investment.")
    if debt_resilience < 55:
        risks.append("Debt remains fragile relative to the relevant post-study income.")
    option = ScoredOption(
        row["record_id"],
        row["option_name"],
        round(score, 1),
        fit,
        (
            f"The precomputed Decision Atlas classifies this as a {atlas_entry['pathway']} "
            f"pathway ({float(atlas_entry['pathway_score']):.0f}/100).",
            f"Probability-weighted positive-NPV estimate is {positive_probability * 100:.0f}%.",
            f"Ten-year incremental NPV is ₹{npvs[1] / 100000:.1f} lakh in the base "
            f"case and ₹{npvs[0] / 100000:.1f} lakh in the downside case.",
            f"All-in cost is ₹{cost / 100000:.1f} lakh versus the responsible ceiling "
            f"of ₹{budget / 100000:.1f} lakh.",
        ),
        tuple(risks),
        (f"{row['source_id']} · observed {row['observed_on']}", row["source_url"]),
        {
            "all-in education investment ₹": round(cost),
            "economic cost including foregone income ₹": round(economic_cost),
            "downside incremental NPV ₹": round(npvs[0]),
            "base incremental NPV ₹": round(npvs[1]),
            "upside incremental NPV ₹": round(npvs[2]),
            "base incremental IRR %": round((base_irr or -1) * 100, 1),
            "probability of positive NPV %": round(positive_probability * 100, 1),
            "debt resilience score": round(debt_resilience, 1),
            "evidence authority score": evidence,
            "required funding adjustment ₹": round(adjustment),
            "precomputed pathway": str(atlas_entry["pathway"]),
            "cost to risk-adjusted uplift": float(atlas_entry["cost_to_risk_adjusted_uplift"]),
        },
    )
    return CareerCandidate(
        option,
        {
            "return": value_score,
            "downside": downside_score,
            "affordability": affordability,
            "resilience": debt_resilience,
            "authority": evidence,
        },
    )


def decide(
    answers: dict[str, Any],
    rows: list[dict[str, str]],
    policy: dict[str, Any],
    manifest: dict[str, Any],
    atlas: dict[str, Any] | None = None,
) -> DecisionReport:
    budget = float(answers["budget_inr"])
    atlas_by_id = {item["record_id"]: item for item in (atlas or {}).get("entries", [])}
    fallback = {
        "pathway": "Unclassified",
        "pathway_score": 0,
        "cost_to_risk_adjusted_uplift": 0,
    }
    candidates = [
        candidate
        for row in rows
        if (
            candidate := _candidate(
                row, answers, budget, atlas_by_id.get(row["record_id"], fallback)
            )
        )
    ]
    objectives = [candidate.objectives for candidate in candidates]
    frontier_indices = pareto_front(
        objectives, ("return", "downside", "affordability", "resilience", "authority")
    )
    ordered = sorted(
        (candidates[index] for index in frontier_indices),
        key=lambda item: item.option.score,
        reverse=True,
    )
    for candidate in sorted(candidates, key=lambda item: item.option.score, reverse=True):
        if candidate not in ordered:
            ordered.append(candidate)
    ranked = tuple(candidate.option for candidate in ordered[:3])
    top = ranked[0] if ranked else None
    if top is None:
        verdict, top_score = "WAIT — NO FEASIBLE PROGRAMME PATH IS COVERED", 0.0
        summary = (
            f"WAIT—do not stretch beyond the responsible {_lakhs(budget)} ceiling. None of the "
            "currently covered paths fits the degree, field, destination and funding constraints "
            "well enough. Secure material funding, widen the destination set or reduce the cost "
            "before paying an application deposit."
        )
        lead_action = (
            "Do not borrow or commit a deposit yet; first find a funded or lower-cost path that "
            f"fits within the {_lakhs(budget)} ceiling."
        )
    elif (
        top.score >= float(policy["verdict_thresholds"]["strong"])
        and top.fit == "Investable within ceiling"
    ):
        verdict, top_score = "GO — PROCEED TO PROGRAMME-LEVEL DILIGENCE", top.score
        summary = (
            f"GO to offer-level diligence for {top.title}. It is the strongest covered match for "
            "your goal and funding limits, but this is not yet permission to enrol: verify the "
            "actual offer, scholarship, employment outcomes and loan terms before paying."
        )
        lead_action = (
            f"Shortlist {top.title} first and obtain its written all-in cost, funding and recent "
            "graduate outcomes before committing money."
        )
    elif top.score >= float(policy["verdict_thresholds"]["conditional"]):
        verdict, top_score = (
            "ADJUST — CHANGE COST, FUNDING OR DESTINATION BEFORE COMMITTING",
            top.score,
        )
        adjustment = float(top.metrics["required funding adjustment ₹"])
        if adjustment > 0:
            gap = f"It is about {_lakhs(adjustment)} above your responsible ceiling. "
        else:
            gap = "Its return is plausible, but the downside or debt burden is not yet robust. "
        summary = (
            f"ADJUST before committing. {top.title} is the best covered direction, but not yet a "
            f"safe investment on the present terms. {gap}Lower the net cost, improve funding or "
            "choose a more resilient destination before paying a deposit."
        )
        lead_action = (
            f"Keep {top.title} only as a conditional shortlist; negotiate funding and re-run the "
            "decision using the written offer before paying."
        )
    else:
        verdict, top_score = (
            "DO NOT INVEST YET — THE DOWNSIDE-ADJUSTED RETURN IS TOO WEAK",
            top.score,
        )
        summary = (
            f"DO NOT INVEST YET. Even {top.title}, the strongest covered match, does not currently "
            "compensate for the full cost, debt and downside risk. A lower-cost or funded route "
            "must materially improve the numbers before an overseas degree is responsible."
        )
        lead_action = (
            "Pause applications that require non-refundable money; first test a lower-cost, "
            "funded or India-return-compatible route."
        )
    return DecisionReport(
        "careersim",
        verdict,
        top_score,
        ranking_stability([option.score for option in ranked]),
        "Pathway-level reference universe; verify exact programme offer, funding and "
        "current policy",
        summary,
        ranked,
        tuple(dict.fromkeys(risk for option in ranked for risk in option.risks)),
        (
            "Forecasts are scenarios, not guaranteed salaries or immigration outcomes.",
            "Programme fees, offers and employment distributions require verification.",
            "The confirmed case accurately represents the student's constraints.",
        ),
        (
            lead_action,
            "Verify tuition, living costs, scholarship and loan terms.",
            "Request programme-specific employment distributions.",
            "Re-run with the written offer before paying a deposit.",
        ),
        (
            "A scholarship, lower-cost destination or smaller loan can change ADJUST to GO.",
            "A weaker visa or employment scenario can reverse the ranking.",
        ),
        tuple(dict.fromkeys(evidence for option in ranked for evidence in option.evidence))
        or (f"{manifest['artifact_id']} · no feasible covered path",),
        dict(answers),
        manifest["artifact_id"],
        manifest["effective_date"],
        manifest["content_sha256"],
        str(policy["policy_version"]),
    )

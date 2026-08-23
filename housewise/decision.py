"""HouseWise deterministic ownership simulation and Pareto optimisation engine."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.optimization import bounded, internal_rate_of_return, pareto_front, ranking_stability
from plugin_sdk.decision import DecisionReport, ScoredOption


@dataclass(frozen=True, slots=True)
class HouseCandidate:
    option: ScoredOption
    objectives: dict[str, float]


def _number(row: dict[str, str], key: str) -> float:
    return float(row[key])


def _annual_payment(principal: float, rate: float, years: int) -> float:
    if principal <= 0:
        return 0.0
    return principal * rate / (1 - (1 + rate) ** -years)


def _remaining_loan(principal: float, rate: float, years: int, elapsed: int) -> float:
    if principal <= 0 or elapsed >= years:
        return 0.0
    payment = _annual_payment(principal, rate, years)
    return principal * (1 + rate) ** elapsed - payment * ((1 + rate) ** elapsed - 1) / rate


def _cashflows(
    purchase_price: float,
    transaction_cost: float,
    debt_ratio: float,
    annual_net_rent: float,
    growth_rate: float,
    horizon: int,
) -> tuple[float, ...]:
    loan = purchase_price * debt_ratio
    equity = purchase_price - loan + transaction_cost
    rate = 0.085
    payment = _annual_payment(loan, rate, 20)
    annual = annual_net_rent - payment
    terminal = purchase_price * (1 + growth_rate) ** horizon - _remaining_loan(
        loan, rate, 20, horizon
    )
    return (-equity, *(annual for _ in range(max(0, horizon - 1))), annual + terminal)


def _candidate(
    row: dict[str, str], answers: dict[str, Any], policy: dict[str, Any]
) -> HouseCandidate | None:
    if row["city"] != answers["city"]:
        return None
    size = float(answers["size_sqft"])
    budget = float(answers["budget_inr"])
    horizon = int(float(answers["horizon_years"]))
    base_price = _number(row, "indicative_price_per_sqft") * size
    transaction_cost = base_price * _number(row, "transaction_cost_pct") / 100
    acquisition_cost = base_price + transaction_cost
    if acquisition_cost > budget * 1.45:
        return None
    debt_ratio = {"Comfortable buffer": 0.50, "Manageable": 0.65, "Stretched": 0.80}[
        str(answers["financing"])
    ]
    vacancy = _number(row, "vacancy_pct") / 100
    annual_rent = base_price * _number(row, "rental_yield_pct") / 100 * (1 - vacancy)
    maintenance = base_price * _number(row, "maintenance_pct") / 100
    net_rent = annual_rent - maintenance
    growth_rates = tuple(
        _number(row, key) / 100
        for key in ("price_growth_p10_pct", "price_growth_p50_pct", "price_growth_p90_pct")
    )
    cashflows = tuple(
        _cashflows(base_price, transaction_cost, debt_ratio, net_rent, growth, horizon)
        for growth in growth_rates
    )
    irrs = tuple(internal_rate_of_return(flow) for flow in cashflows)
    irr_values = tuple((value if value is not None else -1.0) * 100 for value in irrs)
    downside, base, upside = irr_values
    probability_loss = 0.12 if downside > 0 else 0.30 if base > 0 else 0.62 if upside > 0 else 0.88
    affordability = bounded(budget / max(acquisition_cost, 1) * 100)
    climate = 100 - (_number(row, "climate_risk_score") + _number(row, "water_risk_score")) / 2
    liquidity = _number(row, "liquidity_score")
    liveability = _number(row, "liveability_score")
    evidence = _number(row, "evidence_score")
    resilience = bounded(100 - debt_ratio * 45 - _number(row, "risk_score") * 0.25)
    return_score = bounded(50 + base * 4)
    downside_score = bounded(50 + downside * 4)
    score = (
        return_score * 0.24
        + downside_score * 0.16
        + affordability * 0.16
        + resilience * 0.12
        + liquidity * 0.10
        + liveability * 0.08
        + climate * 0.06
        + evidence * 0.08
    )
    priority_score = {
        "Daily liveability": liveability,
        "Capital preservation": (liquidity + downside_score + resilience) / 3,
        "Rental income": bounded(_number(row, "rental_yield_pct") * 22),
        "Growth potential": return_score,
        "Liquidity": liquidity,
    }[str(answers["priority"])]
    score = bounded(score + (priority_score - 50) * 0.08)
    if horizon < int(policy["minimum_horizon_years"]):
        score = bounded(score - 10)
    adjustment = max(0.0, acquisition_cost - budget)
    max_price = base_price * min(1.0, budget / max(acquisition_cost, 1))
    fit = "Within ceiling" if not adjustment else "Price or size adjustment required"
    risks = [row["notes"]]
    if row["legal_evidence"] != "property_verified":
        risks.append("Title and project approvals remain property-level decision gates.")
    if adjustment:
        risks.append(f"Indicative acquisition cost exceeds the ceiling by ₹{adjustment:,.0f}.")
    if downside < 0:
        risks.append("The downside scenario produces a negative leveraged equity return.")
    if str(answers["financing"]) == "Stretched":
        risks.append("The proposed financing leaves insufficient shock absorption.")
    option = ScoredOption(
        row["record_id"],
        row["option_name"],
        round(score, 1),
        fit,
        (
            f"Indicative acquisition cost is ₹{acquisition_cost / 100000:.1f} lakh for "
            f"{size:.0f} sq ft.",
            f"Leveraged equity IRR spans {downside:.1f}% downside to {upside:.1f}% "
            f"upside; base is {base:.1f}%.",
            f"Liquidity is {liquidity:.0f}/100 and evidence authority is "
            f"{evidence:.0f}/100 before property diligence.",
        ),
        tuple(risks),
        (f"{row['source_id']} · observed {row['observed_on']}", row["source_url"]),
        {
            "indicative acquisition cost ₹": round(acquisition_cost),
            "recommended maximum base price ₹": round(max_price),
            "downside leveraged equity IRR %": round(downside, 1),
            "base leveraged equity IRR %": round(base, 1),
            "upside leveraged equity IRR %": round(upside, 1),
            "probability of negative return %": round(probability_loss * 100, 1),
            "net rental yield reference %": round(net_rent / max(base_price, 1) * 100, 2),
            "liquidity score": liquidity,
            "household resilience score": round(resilience, 1),
            "evidence authority score": evidence,
            "required budget adjustment ₹": round(adjustment),
        },
    )
    return HouseCandidate(
        option,
        {
            "return": return_score,
            "downside": downside_score,
            "affordability": affordability,
            "liquidity": liquidity,
            "resilience": resilience,
            "authority": evidence,
        },
    )


def decide(
    answers: dict[str, Any],
    rows: list[dict[str, str]],
    policy: dict[str, Any],
    manifest: dict[str, Any],
) -> DecisionReport:
    candidates = [candidate for row in rows if (candidate := _candidate(row, answers, policy))]
    objectives = [candidate.objectives for candidate in candidates]
    frontier_indices = pareto_front(
        objectives, ("return", "downside", "affordability", "liquidity", "resilience", "authority")
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
        verdict, score = "WAIT — NO FEASIBLE SEARCH ZONE IS COVERED", 0.0
    elif str(answers["financing"]) == "Stretched":
        verdict, score = "RENT/WAIT — DO NOT FORCE A FRAGILE PURCHASE", top.score
    elif top.score >= float(policy["verdict_thresholds"]["strong"]) and top.fit == "Within ceiling":
        verdict, score = "BUY — SUBJECT TO PROPERTY-LEVEL LEGAL AND TECHNICAL DILIGENCE", top.score
    elif top.score >= float(policy["verdict_thresholds"]["conditional"]):
        verdict, score = "BUY ONLY IF ADJUSTED — USE THE MAXIMUM PRICE AND RISK GATES", top.score
    else:
        verdict, score = "RENT/WAIT — CURRENT RISK-ADJUSTED VALUE IS WEAK", top.score
    return DecisionReport(
        "housewise",
        verdict,
        score,
        ranking_stability([option.score for option in ranked]),
        "Micro-market search-zone evidence; no exact title or project has been approved",
        "HouseWise simulates complete ownership cash flows and retains robust non-dominated "
        "search zones before property diligence.",
        ranked,
        tuple(dict.fromkeys(risk for option in ranked for risk in option.risks)),
        (
            "Price and rent forecasts are scenarios rather than valuations.",
            "Exact legal title and approvals remain mandatory gates.",
            "Financing categories are planning approximations until lender terms are entered.",
        ),
        (
            "Verify RERA filings title approvals and encumbrances.",
            "Obtain comparable registered transactions and an engineering inspection.",
            "Re-run using negotiated price and written loan terms.",
        ),
        (
            "A lower price or larger equity buffer can change an adjusted verdict to BUY.",
            "Adverse legal climate or water evidence must override the score.",
        ),
        tuple(dict.fromkeys(evidence for option in ranked for evidence in option.evidence))
        or (f"{manifest['artifact_id']} · no feasible covered search zone",),
        dict(answers),
        manifest["artifact_id"],
        manifest["effective_date"],
        manifest["content_sha256"],
        str(policy["policy_version"]),
    )

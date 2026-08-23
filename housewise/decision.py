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


def _lakhs(value: float) -> str:
    return f"₹{value / 100000:.1f} lakh"


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
    row: dict[str, str],
    answers: dict[str, Any],
    policy: dict[str, Any],
    atlas_entry: dict[str, Any],
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
            f"The precomputed Decision Atlas classifies this as a {atlas_entry['pathway']} "
            f"pathway ({float(atlas_entry['pathway_score']):.0f}/100).",
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
            "precomputed pathway": str(atlas_entry["pathway"]),
            "cost to growth and yield": float(atlas_entry["cost_to_growth_and_yield"]),
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
    atlas: dict[str, Any] | None = None,
) -> DecisionReport:
    atlas_by_id = {item["record_id"]: item for item in (atlas or {}).get("entries", [])}
    fallback = {"pathway": "Unclassified", "pathway_score": 0, "cost_to_growth_and_yield": 0}
    candidates = [
        candidate
        for row in rows
        if (
            candidate := _candidate(
                row, answers, policy, atlas_by_id.get(row["record_id"], fallback)
            )
        )
    ]
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
        summary = (
            f"WAIT—do not force a purchase. The {_lakhs(float(answers['budget_inr']))} all-in "
            f"ceiling and {float(answers['size_sqft']):.0f} sq ft requirement do not produce a "
            "responsible option in the currently covered city zones. Reduce the required size, "
            "increase the cash buffer responsibly or keep renting while you search."
        )
        lead_action = (
            "Do not pay a booking amount; first change the size, location or budget constraint "
            "until at least one covered zone fits without financial strain."
        )
    elif str(answers["financing"]) == "Stretched":
        verdict, score = "RENT/WAIT — DO NOT FORCE A FRAGILE PURCHASE", top.score
        summary = (
            f"RENT/WAIT. {top.title} may be the strongest covered location, but the proposed "
            "financing leaves too little room for income, interest-rate or repair shocks. A good "
            "property is still a bad purchase when it makes the household fragile."
        )
        lead_action = (
            "Keep renting and rebuild the equity and emergency buffer before making any booking "
            "payment."
        )
    elif top.score >= float(policy["verdict_thresholds"]["strong"]) and top.fit == "Within ceiling":
        verdict, score = "BUY — SUBJECT TO PROPERTY-LEVEL LEGAL AND TECHNICAL DILIGENCE", top.score
        summary = (
            f"BUY can be justified in {top.title}, subject to one non-negotiable condition: the "
            "exact property must clear title, approval, engineering and price diligence. The zone "
            "fits the current budget and offers the best covered balance of return, resilience "
            "and resale ability."
        )
        lead_action = (
            f"Search in {top.title} first, but pay nothing until the exact property's title, "
            "approvals, condition and negotiated all-in price are independently verified."
        )
    elif top.score >= float(policy["verdict_thresholds"]["conditional"]):
        verdict, score = "BUY ONLY IF ADJUSTED — USE THE MAXIMUM PRICE AND RISK GATES", top.score
        maximum = float(top.metrics["recommended maximum base price ₹"])
        summary = (
            f"BUY ONLY IF ADJUSTED. {top.title} is the best covered search zone, but the present "
            f"size-price combination is not yet safe. Keep the base property price at or below "
            f"{_lakhs(maximum)}, preserve the household buffer and reject any property that fails "
            "legal or technical diligence."
        )
        lead_action = (
            f"Use {_lakhs(maximum)} as the maximum base-price gate for {top.title}; walk away if "
            "the negotiated property exceeds it or weakens your safety buffer."
        )
    else:
        verdict, score = "RENT/WAIT — CURRENT RISK-ADJUSTED VALUE IS WEAK", top.score
        summary = (
            f"RENT/WAIT. Even {top.title}, the strongest covered zone, does not offer enough "
            "risk-adjusted value for the current holding period and financing assumptions. "
            "Preserve flexibility instead of paying transaction costs for a weak ownership case."
        )
        lead_action = (
            "Do not pay a booking amount; keep renting and revisit the purchase after the price, "
            "holding period or financing position improves."
        )
    return DecisionReport(
        "housewise",
        verdict,
        score,
        ranking_stability([option.score for option in ranked]),
        "Micro-market search-zone evidence; no exact title or project has been approved",
        summary,
        ranked,
        tuple(dict.fromkeys(risk for option in ranked for risk in option.risks)),
        (
            "Price and rent forecasts are scenarios rather than valuations.",
            "Exact legal title and approvals remain mandatory gates.",
            "Financing categories are planning approximations until lender terms are entered.",
        ),
        (
            lead_action,
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

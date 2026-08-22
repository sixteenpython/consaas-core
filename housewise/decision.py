"""Deterministic HouseWise Foundation decision engine."""

from __future__ import annotations

from typing import Any

from plugin_sdk.decision import DecisionReport, ScoredOption


def _bounded(value: float) -> float:
    return max(0.0, min(100.0, value))


def decide(
    answers: dict[str, Any],
    rows: list[dict[str, str]],
    policy: dict[str, Any],
    manifest: dict[str, Any],
) -> DecisionReport:
    budget = float(answers["budget_inr"])
    size = float(answers["size_sqft"])
    risk_multiplier = {"Low": 1.2, "Moderate": 1.0, "High": 0.75}[answers["risk_tolerance"]]
    weights = policy["weights"]
    options: list[ScoredOption] = []
    for row in rows:
        if row["city"] != answers["city"]:
            continue
        price = float(row["indicative_price_per_sqft"])
        purchase_cost = price * size * (1 + float(policy["transaction_cost_buffer"]))
        affordability = _bounded(budget / purchase_cost * 100)
        liveability = float(row["liveability_score"])
        liquidity = float(row["liquidity_score"])
        transit = float(row["transit_score"])
        growth = float(row["growth_score"])
        yield_score = _bounded(float(row["rental_yield_pct"]) * 22)
        risk_fit = _bounded(100 - float(row["risk_score"]) * risk_multiplier)
        dimensions = {
            "affordability": affordability,
            "liveability": liveability,
            "liquidity": liquidity,
            "transit": transit,
            "rental_yield": yield_score,
            "growth": growth,
            "risk_fit": risk_fit,
        }
        score = sum(dimensions[key] * float(weight) for key, weight in weights.items())
        priority_dimension = {
            "Daily liveability": liveability,
            "Capital preservation": (liquidity + risk_fit) / 2,
            "Rental income": yield_score,
            "Growth potential": growth,
            "Liquidity": liquidity,
        }[answers["priority"]]
        score += (priority_dimension - 50) * 0.08
        if answers["purpose"] == "Primary home":
            score += (liveability - growth) * 0.05
        elif answers["purpose"] == "Long-term investment":
            score += (growth + liquidity - 150) * 0.04
        risks = [row["notes"]]
        if purchase_cost > budget:
            risks.append("Indicative acquisition cost exceeds the declared all-in ceiling.")
        if answers["financing"] == "Stretched":
            score -= 9
            risks.append("The household buffer is too thin for rate, repair or income shocks.")
        if float(answers["horizon_years"]) < float(policy["minimum_horizon_years"]):
            score -= 8
            risks.append(
                "The holding period may be too short to absorb transaction costs and illiquidity."
            )
        options.append(
            ScoredOption(
                row["record_id"],
                row["option_name"],
                round(_bounded(score), 1),
                "Indicatively affordable" if purchase_cost <= budget else "Over budget",
                (
                    f"Indicative all-in acquisition cost is ₹{purchase_cost / 100000:.1f} lakh "
                    f"for {size:.0f} sq ft.",
                    f"Liveability {liveability:.0f}/100 · liquidity {liquidity:.0f}/100 · "
                    f"transit {transit:.0f}/100.",
                ),
                tuple(risks),
                (f"{row['source_id']} · observed {row['observed_on']}", row["source_url"]),
                {
                    "indicative all-in cost ₹": round(purchase_cost),
                    "rental yield reference %": float(row["rental_yield_pct"]),
                },
            )
        )
    ranked = tuple(sorted(options, key=lambda item: item.score, reverse=True)[:3])
    top = ranked[0] if ranked else None
    top_score = top.score if top else 0.0
    thresholds = policy["verdict_thresholds"]
    if not top:
        verdict = "NEEDS MORE EVIDENCE — CITY COVERAGE IS INCOMPLETE"
    elif answers["financing"] == "Stretched" or top.fit == "Over budget":
        verdict = "WAIT — DO NOT FORCE THIS PURCHASE"
    elif top_score >= thresholds["strong"]:
        verdict = "PROMISING SEARCH ZONE — BEGIN PROPERTY-LEVEL DILIGENCE"
    elif top_score >= thresholds["conditional"]:
        verdict = "CONDITIONAL — SHORTLIST ONLY AFTER RISK CHECKS"
    else:
        verdict = "WAIT OR RENT — CURRENT FIT IS WEAK"
    return DecisionReport(
        "housewise",
        verdict,
        top_score,
        "Low",
        "City archetypes only; no property, title or project has been assessed",
        "The result identifies where diligence may be worth spending—not a property to buy.",
        ranked,
        tuple(dict.fromkeys(risk for option in ranked for risk in option.risks)),
        (
            "Indicative price bands may differ materially by micro-market and property.",
            "Declared size and budget include the user's true constraints.",
        ),
        (
            "Verify title, approvals, encumbrances and RERA disclosures with qualified "
            "professionals.",
            "Inspect flood, water, access and construction quality at the exact site.",
            "Obtain three comparable registered transactions and a downside EMI scenario.",
        ),
        (
            "A lower negotiated price or larger equity buffer could improve feasibility.",
            "Verified transit completion can change access value.",
            "Adverse legal, climate or supply evidence should veto an otherwise attractive score.",
        ),
        tuple(dict.fromkeys(evidence for option in ranked for evidence in option.evidence)),
        dict(answers),
        manifest["artifact_id"],
        manifest["effective_date"],
        manifest["content_sha256"],
        policy["policy_version"],
    )

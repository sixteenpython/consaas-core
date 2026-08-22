"""Deterministic CareerSim Foundation decision engine."""

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
    risk_multiplier = {"Low": 1.2, "Moderate": 1.0, "High": 0.75}[answers["risk_tolerance"]]
    weights = policy["weights"]
    options: list[ScoredOption] = []
    for row in rows:
        if answers["geography"] == "India only" and row["geography"] != "India":
            continue
        cost = float(row["total_cost_inr"])
        field_fit = (
            100 if row["field"] == answers["field"] else 62 if "Flexible" in row["field"] else 30
        )
        degree_fit = 100 if row["degree_level"] == answers["degree_level"] else 25
        affordability = _bounded((budget / cost) * 100)
        quality = float(row["quality_score"])
        employability = float(row["employability_score"])
        salary_value = _bounded(float(row["median_start_salary_inr"]) / cost * 180)
        risk_fit = _bounded(100 - float(row["risk_score"]) * risk_multiplier)
        dimensions = {
            "field_fit": field_fit,
            "degree_fit": degree_fit,
            "affordability": affordability,
            "quality": quality,
            "employability": employability,
            "salary_value": salary_value,
            "risk_fit": risk_fit,
        }
        score = sum(dimensions[key] * float(weight) for key, weight in weights.items())
        priority_dimension = {
            "Career outcomes": (employability + salary_value) / 2,
            "Low debt": affordability,
            "Academic depth": quality,
            "International mobility": 100 if row["geography"] == "Overseas" else 45,
            "Optionality": 85 if "Flexible" in row["field"] else (quality + employability) / 2,
        }[answers["priority"]]
        score += (priority_dimension - 50) * 0.08
        if answers["geography"] == "Overseas preferred" and row["geography"] == "Overseas":
            score += 4
        reasons = [
            f"Total indicative cost uses {cost / 100000:.1f} lakh of your "
            f"{budget / 100000:.1f} lakh ceiling.",
            f"Quality and employability references are {quality:.0f}/100 and "
            f"{employability:.0f}/100.",
        ]
        risks = [row["notes"]]
        if affordability < 100:
            risks.append("The indicative total cost exceeds the declared responsible budget.")
        if answers["academic_readiness"] == "Developing" and quality >= 85:
            risks.append("This is an ambitious admissions case; build a credible safety option.")
            score -= 5
        options.append(
            ScoredOption(
                row["record_id"],
                row["option_name"],
                round(_bounded(score), 1),
                "Within budget" if affordability >= 100 else "Funding gap",
                tuple(reasons),
                tuple(risks),
                (f"{row['source_id']} · observed {row['observed_on']}", row["source_url"]),
                {
                    "indicative total cost ₹": cost,
                    "starting salary reference ₹": float(row["median_start_salary_inr"]),
                },
            )
        )
    ranked = tuple(sorted(options, key=lambda item: item.score, reverse=True)[:3])
    top = ranked[0] if ranked else None
    top_score = top.score if top else 0.0
    thresholds = policy["verdict_thresholds"]
    if not top:
        verdict = "NEEDS MORE EVIDENCE"
    elif top_score >= thresholds["strong"] and top.fit == "Within budget":
        verdict = "STRONG FIT — VERIFY THE SPECIFIC PROGRAMME"
    elif top_score >= thresholds["conditional"]:
        verdict = "CONDITIONAL FIT — RESOLVE THE FUNDING OR ADMISSION RISK"
    else:
        verdict = "DO NOT COMMIT YET — EXPAND THE OPTION SET"
    return DecisionReport(
        "careersim",
        verdict,
        top_score,
        "Medium" if ranked else "Low",
        "Foundation archetypes; programme-level verification required",
        "The recommendation balances fit, total affordability and outcome resilience "
        "rather than prestige alone.",
        ranked,
        tuple(dict.fromkeys(risk for option in ranked for risk in option.risks)),
        (
            "Costs and salaries are indicative archetype references, not forecasts.",
            "The learner's answers are accurate and current.",
        ),
        (
            "Verify fees, scholarships, curriculum and audited placement disclosures.",
            "Apply to one ambitious, one balanced and one resilient option.",
            "Model debt repayment under a downside salary case.",
        ),
        (
            "A material scholarship could change affordability ranking.",
            "A stronger admissions profile could make selective options more credible.",
            "Verified programme outcomes could change the quality score.",
        ),
        tuple(dict.fromkeys(evidence for option in ranked for evidence in option.evidence)),
        dict(answers),
        manifest["artifact_id"],
        manifest["effective_date"],
        manifest["content_sha256"],
        policy["policy_version"],
    )

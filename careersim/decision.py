"""Deterministic overseas-education ROI engine for Indian students."""

from __future__ import annotations

from typing import Any

from plugin_sdk.decision import DecisionReport, ScoredOption


def _bounded(value: float) -> float:
    return max(0.0, min(100.0, value))


def _funding_fit(plan: str, funding_model: str, affordability: float) -> float:
    funded = "funded" in funding_model.lower() or "stipend" in funding_model.lower()
    if plan == "Dependent on scholarship / assistantship":
        return 100.0 if funded else 35.0
    if plan == "Substantial education loan":
        return _bounded(115 - (100 - affordability) * 1.3)
    if plan == "Mixed family funding and modest loan":
        return _bounded((affordability + (75 if funded else 55)) / 2)
    return affordability


def decide(
    answers: dict[str, Any],
    rows: list[dict[str, str]],
    policy: dict[str, Any],
    manifest: dict[str, Any],
) -> DecisionReport:
    budget = float(answers["budget_inr"])
    risk_multiplier = {"Low": 1.25, "Moderate": 1.0, "High": 0.78}[answers["risk_tolerance"]]
    weights = policy["weights"]
    options: list[ScoredOption] = []
    for row in rows:
        if (
            answers["target_region"] != "Multiple regions"
            and row["target_region"] != answers["target_region"]
        ):
            continue
        cost = float(row["total_cost_inr"])
        field_fit = (
            100.0
            if row["field"] == answers["field"]
            else 78.0
            if "Flexible" in row["field"] or answers["field"] == "Flexible / undecided"
            else 35.0
        )
        degree_fit = 100.0 if row["degree_level"] == answers["degree_level"] else 0.0
        destination_fit = 100.0 if answers["target_region"] == row["target_region"] else 82.0
        affordability = _bounded((budget / max(cost, 1)) * 100)
        quality = float(row["quality_score"])
        employability = (
            float(row["employability_score"]) + float(row["employment_probability_score"])
        ) / 2
        salary = (
            float(row["india_return_salary_inr"])
            if answers["career_goal"] == "Return to India soon after graduation"
            else float(row["overseas_start_salary_inr"])
        )
        salary_value = _bounded(salary / max(cost, 1) * 115)
        work_rights = float(row["work_rights_score"])
        funding_fit = _funding_fit(answers["funding_plan"], row["funding_model"], affordability)
        compound_risk = (float(row["risk_score"]) + float(row["visa_uncertainty_score"])) / 2
        risk_fit = _bounded(100 - compound_risk * risk_multiplier)
        dimensions = {
            "field_fit": field_fit,
            "degree_fit": degree_fit,
            "destination_fit": destination_fit,
            "affordability": affordability,
            "quality": quality,
            "employability": employability,
            "salary_value": salary_value,
            "work_rights": work_rights,
            "funding_fit": funding_fit,
            "risk_fit": risk_fit,
        }
        score = sum(dimensions[key] * float(weight) for key, weight in weights.items())
        priority_dimension = {
            "Downside-adjusted financial ROI": (salary_value + affordability + risk_fit) / 3,
            "Career acceleration": employability,
            "Low debt": (affordability + funding_fit) / 2,
            "Academic depth": quality,
            "International mobility": work_rights,
            "Long-term optionality": (quality + employability + work_rights) / 3,
        }[answers["priority"]]
        score += (priority_dimension - 50) * 0.1
        if answers["career_goal"] == "Research / academic career" and row["degree_level"] == "PhD":
            score += 6
        risks = [row["notes"]]
        if affordability < 100 and "funded" not in row["funding_model"].lower():
            risks.append("The indicative all-in cost exceeds the responsible family ceiling.")
        if answers["funding_plan"] == "Substantial education loan" and cost > salary * 1.4:
            risks.append("Debt would be large relative to the relevant starting-income reference.")
            score -= 7
        if answers["academic_readiness"] == "Developing" and quality >= 88:
            risks.append(
                "Admission is ambitious; retain credible balanced and resilient applications."
            )
            score -= 5
        if answers["career_goal"] == "Return to India soon after graduation":
            risks.append(
                "ROI uses the lower India-return salary reference, not an overseas headline."
            )
        funded_path = row["degree_level"] == "PhD" and (
            "funded" in row["funding_model"].lower() or "stipend" in row["funding_model"].lower()
        )
        fit = (
            "Funding-dependent research path"
            if funded_path
            else "Within responsible ceiling"
            if affordability >= 100
            else "Funding gap"
        )
        options.append(
            ScoredOption(
                row["record_id"],
                row["option_name"],
                round(_bounded(score), 1),
                fit,
                (
                    f"Indicative all-in investment is ₹{cost / 100000:.1f} lakh versus your "
                    f"₹{budget / 100000:.1f} lakh responsible ceiling.",
                    f"Relevant starting-income reference is ₹{salary / 100000:.1f} lakh; "
                    f"employment evidence scores {employability:.0f}/100.",
                    f"Post-study work-path score is {work_rights:.0f}/100 and the indicative "
                    f"payback horizon is {float(row['roi_horizon_years']):.1f} years.",
                ),
                tuple(risks),
                (f"{row['source_id']} · observed {row['observed_on']}", row["source_url"]),
                {
                    "indicative all-in investment ₹": cost,
                    "relevant starting-income reference ₹": salary,
                    "employment evidence score": round(employability, 1),
                    "post-study work-path score": work_rights,
                    "indicative payback horizon years": float(row["roi_horizon_years"]),
                },
            )
        )
    ranked = tuple(sorted(options, key=lambda item: item.score, reverse=True)[:3])
    top = ranked[0] if ranked else None
    top_score = top.score if top else 0.0
    thresholds = policy["verdict_thresholds"]
    if not top:
        verdict = "NEEDS MORE EVIDENCE — EXPAND THE DESTINATION OR FIELD SET"
    elif top_score >= thresholds["strong"] and top.fit != "Funding gap":
        verdict = "PROMISING ROI — VERIFY THE EXACT PROGRAMME AND FUNDING"
    elif top_score >= thresholds["conditional"]:
        verdict = "CONDITIONAL ROI — RESOLVE FUNDING, VISA OR EMPLOYMENT RISK"
    else:
        verdict = "DO NOT COMMIT YET — THE DOWNSIDE IS TOO FRAGILE"
    return DecisionReport(
        "careersim",
        verdict,
        top_score,
        "Low" if not ranked else "Medium",
        "Overseas archetypes only; exact programme, funding, visa and outcome evidence required",
        "The assessment tests whether an overseas degree is worth its full cost and downside risk "
        "for an Indian student—not whether the institution is prestigious.",
        ranked,
        tuple(dict.fromkeys(risk for option in ranked for risk in option.risks)),
        (
            "Costs and salaries are illustrative INR-normalised archetype references, not "
            "forecasts.",
            "Visa, work-right and immigration policies may change before graduation.",
            "The student's confirmed Case Knowledge Asset is accurate and current.",
        ),
        (
            "Verify the exact tuition, living budget and written scholarship or assistantship.",
            "Obtain programme-specific employment distributions—not only the highest salary.",
            "Model debt repayment under overseas-employment and early-India-return scenarios.",
        ),
        (
            "A guaranteed scholarship or assistantship can materially improve the verdict.",
            "A lower-cost destination can improve downside-adjusted ROI.",
            "Verified programme employment and current post-study work rules can change the "
            "ranking.",
        ),
        tuple(dict.fromkeys(evidence for option in ranked for evidence in option.evidence)),
        dict(answers),
        manifest["artifact_id"],
        manifest["effective_date"],
        manifest["content_sha256"],
        policy["policy_version"],
    )

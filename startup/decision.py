"""Deterministic StartupEval Foundation decision engine."""

from __future__ import annotations

from typing import Any

from plugin_sdk.decision import DecisionReport, ScoredOption


def _bounded(value: float) -> float:
    return max(0.0, min(100.0, value))


def _relative(actual: float, reference: float) -> float:
    if reference <= 0:
        return 75.0 if actual <= 0 else 100.0
    return _bounded(actual / reference * 75)


def decide(
    answers: dict[str, Any],
    rows: list[dict[str, str]],
    policy: dict[str, Any],
    manifest: dict[str, Any],
) -> DecisionReport:
    candidates = [
        row
        for row in rows
        if row["sector"] == answers["sector"] and row["stage"] == answers["stage"]
    ]
    if not candidates:
        candidates = [row for row in rows if row["stage"] == answers["stage"]]
    benchmark = candidates[0] if candidates else rows[0]
    evidence_score = {
        "Repeated paid use": 100,
        "Paid pilots": 78,
        "Active usage but little payment": 55,
        "Interviews / assertion only": 28,
    }[answers["customer_evidence"]]
    team_score = {
        "Complete and proven": 95,
        "Strong with one key gap": 76,
        "Several critical gaps": 45,
        "Founder-dependent": 28,
    }[answers["team_strength"]]
    regulatory_score = {
        "Low": 92,
        "Manageable": 72,
        "Material": 38,
        "Unclear": 25,
    }[answers["regulatory_risk"]]
    dimensions = {
        "traction": _relative(
            float(answers["monthly_revenue_inr"]), float(benchmark["revenue_reference_inr"])
        ),
        "growth": _relative(
            float(answers["monthly_growth_pct"]), float(benchmark["growth_reference_pct"])
        ),
        "retention": _relative(
            float(answers["retention_pct"]), float(benchmark["retention_reference_pct"])
        ),
        "margin": _relative(
            float(answers["gross_margin_pct"]), float(benchmark["gross_margin_reference_pct"])
        ),
        "runway": _relative(
            float(answers["runway_months"]), float(benchmark["runway_reference_months"])
        ),
        "customer_evidence": evidence_score,
        "team": team_score,
        "regulatory_resilience": _bounded(
            regulatory_score - float(benchmark["regulatory_complexity"]) * 0.2
        ),
    }
    score = round(
        sum(dimensions[key] * float(weight) for key, weight in policy["weights"].items()), 1
    )
    risks: list[str] = [benchmark["notes"]]
    if float(answers["runway_months"]) < float(policy["minimum_runway_months"]):
        score = round(max(0, score - 12), 1)
        risks.append("Runway is below six months; financing risk can overwhelm product progress.")
    if answers["customer_evidence"] == "Interviews / assertion only":
        risks.append(
            "The problem is asserted but not yet supported by behavioural or paid evidence."
        )
    if answers["regulatory_risk"] in {"Material", "Unclear"}:
        risks.append("Regulatory uncertainty is a decision gate, not a footnote.")
    thresholds = policy["verdict_thresholds"]
    if float(answers["runway_months"]) < 3:
        verdict = "SURVIVAL FIRST — CUT BURN OR SECURE RUNWAY"
        primary = "Stabilise runway"
    elif score >= thresholds["strong"] and evidence_score >= 78:
        verdict = "PROMISING — PROCEED TO DEEP DILIGENCE"
        primary = "Prepare the next evidence-backed growth or funding decision"
    elif score >= thresholds["conditional"]:
        verdict = "CONDITIONAL — RUN THE FALSIFICATION TEST"
        primary = "Resolve the weakest evidence before scaling spend"
    else:
        verdict = "NOT READY — VALIDATE BEFORE COMMITTING MORE CAPITAL"
        primary = "Return to problem and customer validation"
    option_specs = (
        (primary, score, "Best current action"),
        (
            "Bootstrap a narrower proof point",
            _bounded(score + (8 if evidence_score < 78 else -4)),
            "Lower-capital alternative",
        ),
        (
            "Pause scale and investigate the fatal unknown",
            _bounded(100 - min(dimensions.values()) / 2),
            "Information-first alternative",
        ),
    )
    weakest_dimension = min(dimensions, key=lambda name: dimensions[name])
    options = tuple(
        ScoredOption(
            f"startup-action-{index}",
            title,
            round(option_score, 1),
            fit,
            (
                f"Overall evidence score is {score:.1f}/100.",
                f"Weakest dimension is {weakest_dimension.replace('_', ' ')} at "
                f"{dimensions[weakest_dimension]:.0f}/100.",
            ),
            tuple(risks),
            (
                f"{benchmark['source_id']} · observed {benchmark['observed_on']}",
                benchmark["source_url"],
            ),
            {key.replace("_", " "): round(value, 1) for key, value in dimensions.items()},
        )
        for index, (title, option_score, fit) in enumerate(option_specs, start=1)
    )
    confidence = (
        "Medium" if evidence_score >= 78 and answers["regulatory_risk"] != "Unclear" else "Low"
    )
    if answers["role"] == "Investor":
        next_actions = (
            "Verify revenue, cohorts, cash, cap table and customer concentration from primary "
            "evidence.",
            "Interview reference customers and test the weakest dimension independently.",
            "Define diligence conditions before discussing valuation or commitment.",
        )
    else:
        next_actions = (
            "Verify revenue, cohort retention, cash and customer concentration from primary "
            "evidence.",
            "Run one time-boxed experiment against the weakest dimension.",
            "Re-score after the experiment before increasing irreversible spend.",
        )
    return DecisionReport(
        "startup",
        verdict,
        score,
        confidence,
        "Self-reported metrics against a Foundation methodology benchmark",
        "The verdict is a stage-adjusted evidence assessment, not a prediction of company "
        "success or valuation.",
        options,
        tuple(dict.fromkeys(risks)),
        (
            "Metrics use consistent definitions and comparable periods.",
            "Self-reported traction has not been independently audited.",
        ),
        next_actions,
        (
            "Audited retention or paid-use evidence can materially improve authority.",
            "A credible regulatory pathway can remove a decision gate.",
            "Runway below six months can reverse an otherwise positive verdict.",
        ),
        (f"{benchmark['source_id']} · {benchmark['record_id']}", benchmark["source_url"]),
        dict(answers),
        manifest["artifact_id"],
        manifest["effective_date"],
        manifest["content_sha256"],
        policy["policy_version"],
    )

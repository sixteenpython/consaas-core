"""Deterministic Horse/Jockey adjudication for StartupEval."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

from core.optimization import bounded
from plugin_sdk.decision import DecisionReport, ScoredOption

_STOPWORDS = {
    "about",
    "after",
    "also",
    "because",
    "being",
    "from",
    "have",
    "into",
    "more",
    "our",
    "that",
    "their",
    "there",
    "these",
    "they",
    "this",
    "those",
    "through",
    "user",
    "users",
    "very",
    "what",
    "when",
    "where",
    "which",
    "will",
    "with",
}
_EVIDENCE_WORDS = {
    "observed",
    "interviewed",
    "paid",
    "payment",
    "pilot",
    "renewed",
    "retained",
    "used",
    "usage",
    "revenue",
    "customer",
    "customers",
    "tested",
    "measured",
    "transaction",
    "transactions",
    "conversion",
    "cohort",
    "contract",
    "orders",
}
_EXECUTION_WORDS = {
    "built",
    "launched",
    "sold",
    "operated",
    "shipped",
    "managed",
    "changed",
    "learned",
    "failed",
    "improved",
    "delivered",
    "hired",
    "designed",
    "implemented",
    "closed",
}
_UNCERTAINTY = {"unknown", "unsure", "guess", "believe", "hope", "probably", "maybe"}


def _tokens(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[a-z0-9]+", text.casefold())
        if len(token) > 2 and token not in _STOPWORDS
    ]


def _answer_quality(text: str, evidence_terms: set[str] | None = None) -> float:
    """Score specificity and behavioural evidence, not polish or confidence."""
    words = _tokens(text)
    if not words:
        return 0.0
    length = min(35.0, len(set(words)) * 1.25)
    numbers = min(18.0, len(re.findall(r"\b\d+(?:\.\d+)?%?\b", text)) * 6.0)
    evidence = min(35.0, len(set(words) & (evidence_terms or _EVIDENCE_WORDS)) * 7.0)
    structure = 12.0 if len(text.strip()) >= 100 else 6.0 if len(text.strip()) >= 45 else 0.0
    penalty = min(20.0, len(set(words) & _UNCERTAINTY) * 5.0)
    return bounded(length + numbers + evidence + structure - penalty)


def _problem_match(
    answers: dict[str, Any], rows: list[dict[str, str]]
) -> tuple[dict[str, str], float]:
    query = " ".join(
        str(answers[key])
        for key in (
            "problem_customer",
            "problem_evidence",
            "problem_cost",
            "current_alternatives",
            "payer_evidence",
            "solution_outcome",
        )
    )
    query_counts = Counter(_tokens(query))
    ranked: list[tuple[float, dict[str, str]]] = []
    for row in rows:
        reference = " ".join(
            row.get(key, "")
            for key in ("domain", "subdomain", "problem_statement", "keywords", "affected_segment")
        )
        reference_tokens = set(_tokens(reference))
        overlap = sum(min(query_counts[token], 2) for token in reference_tokens)
        coverage = overlap / max(5, min(20, len(reference_tokens)))
        ranked.append((bounded(coverage * 100), row))
    return max(ranked, key=lambda item: item[0])[1], max(ranked, key=lambda item: item[0])[0]


def _weighted(values: dict[str, float], weights: dict[str, float]) -> float:
    return sum(values[key] * weights[key] for key in weights)


def decide(
    answers: dict[str, Any],
    rows: list[dict[str, str]],
    policy: dict[str, Any],
    manifest: dict[str, Any],
    atlas: dict[str, Any] | None = None,
) -> DecisionReport:
    texts = {key: str(value).strip() for key, value in answers.items()}
    problem, match_score = _problem_match(texts, rows)
    atlas_by_id = {item["record_id"]: item for item in (atlas or {}).get("entries", [])}
    problem_atlas = atlas_by_id.get(
        problem["record_id"],
        {"pathway": "Unclassified", "problem_opportunity_score": 0},
    )
    q = {key: _answer_quality(value) for key, value in texts.items()}
    q["solution_outcome"] = _answer_quality(
        texts["solution_outcome"],
        {
            "before",
            "converts",
            "deterministic",
            "evidence",
            "measurable",
            "outcome",
            "produces",
            "reduces",
            "runs",
            "versioned",
        },
    )
    q["business_economics"] = _answer_quality(
        texts["business_economics"],
        {
            "acquire",
            "charge",
            "cost",
            "gross",
            "margin",
            "price",
            "repeat",
            "retain",
            "revenue",
            "serve",
            "subscription",
        },
    )
    match_authority = bounded(match_score * 1.25)
    horse = {
        "problem reality": bounded(
            0.45 * float(problem["problem_reality_score"])
            + 0.35 * q["problem_evidence"]
            + 0.20 * match_authority
        ),
        "pain and frequency": bounded(
            0.55 * float(problem["severity_score"]) + 0.45 * q["problem_cost"]
        ),
        "willing payer": bounded(
            0.45 * float(problem["willingness_to_pay_score"]) + 0.55 * q["payer_evidence"]
        ),
        "remaining white space": bounded(
            0.50 * float(problem["whitespace_score"])
            + 0.30 * q["current_alternatives"]
            + 0.20 * match_authority
        ),
        "solution mechanism": q["solution_outcome"],
        "behavioural traction": q["traction_evidence"],
        "sustainable economics": q["business_economics"],
    }
    horse_score = round(_weighted(horse, policy["horse_dimensions"]), 1)
    jockey = {
        "founder-problem fit": _answer_quality(
            texts["founder_fit"], _EXECUTION_WORDS | _EVIDENCE_WORDS
        ),
        "execution evidence": _answer_quality(texts["execution_learning"], _EXECUTION_WORDS),
        "learning discipline": bounded(
            0.65
            * _answer_quality(
                texts["execution_learning"], {"changed", "learned", "failed", "tested", "evidence"}
            )
            + 0.35
            * _answer_quality(
                texts["risk_milestone"],
                {"test", "measure", "threshold", "fail", "week", "month", "budget"},
            )
        ),
        "capital discipline": _answer_quality(
            texts["risk_milestone"],
            {"budget", "capital", "cost", "week", "month", "threshold", "milestone"},
        ),
    }
    jockey_score = round(_weighted(jockey, policy["jockey_dimensions"]), 1)
    overall = round(0.70 * horse_score + 0.30 * jockey_score, 1)
    evidence_gate = min(
        horse["problem reality"], horse["willing payer"], horse["solution mechanism"]
    )
    thresholds = policy["verdict_thresholds"]
    if (
        overall >= thresholds["strong"]
        and horse_score >= policy["strong_gates"]["horse"]
        and jockey_score >= policy["strong_gates"]["jockey"]
        and evidence_gate >= policy["strong_gates"]["critical_evidence"]
    ):
        verdict = "STRONG"
        summary = (
            "The proposition is close enough to a real, payable Indian problem and the team "
            "has supplied enough execution evidence to justify controlled investment and "
            "deeper diligence."
        )
    elif overall >= thresholds["conditional"] and horse["problem reality"] >= 42:
        verdict = "NOT QUITE THERE"
        summary = (
            "There is a credible proposition, but one or more decisive assumptions still need "
            "behavioural evidence before material capital is committed."
        )
    else:
        verdict = "FORGET IT — IN ITS CURRENT FORM"
        summary = (
            "The present case does not yet establish a sufficiently real, payable problem and "
            "executable business. This rejects the current evidence—not the founder or every "
            "future version of the idea."
        )
    combined = {f"Horse · {key}": value for key, value in horse.items()} | {
        f"Jockey · {key}": value for key, value in jockey.items()
    }
    weakest = min(combined, key=combined.get)
    fatal_unknown = weakest.replace("Horse · ", "").replace("Jockey · ", "")
    risks = (
        f"Fatal unknown: {fatal_unknown} is the weakest supported dimension at "
        f"{combined[weakest]:.0f}/100.",
        f"Problem-observatory match is {match_score:.0f}/100; low semantic overlap limits "
        "external-evidence authority.",
        "All venture answers are self-reported and require primary-evidence diligence before "
        "funding.",
    )
    action_specs = (
        (
            "Proceed to controlled diligence"
            if verdict == "STRONG"
            else "Run the fatal-unknown experiment",
            overall,
            "Best current action",
        ),
        (
            "Narrow the proposition around the strongest proven customer",
            bounded(overall + 6 if horse["problem reality"] >= 60 else overall - 4),
            "Lower-capital alternative",
        ),
        (
            "Pause scale and buy evidence before building more",
            bounded(100 - combined[weakest] / 2),
            "Information-first alternative",
        ),
    )
    metrics = {
        "Horse (business model)": horse_score,
        "Jockey (founder execution)": jockey_score,
        "India problem match": round(match_score, 1),
        "White-space evidence": round(horse["remaining white space"], 1),
        "Precomputed problem pathway": str(problem_atlas["pathway"]),
        "Problem Opportunity Score": float(problem_atlas["problem_opportunity_score"]),
    }
    evidence = (
        f"{problem['source_id']} · {problem['record_id']} · observed {problem['observed_on']}",
        problem["source_url"],
        f"Matched India problem: {problem['problem_statement']}",
        f"Precomputed pathway: {problem_atlas['pathway']}",
    )
    options = tuple(
        ScoredOption(
            f"startup-action-{index}",
            title,
            round(score, 1),
            fit,
            (
                f"Horse score is {horse_score:.1f}/100 and owns 70% of the verdict.",
                f"Jockey score is {jockey_score:.1f}/100 and owns 30% of the verdict.",
            ),
            risks,
            evidence,
            metrics,
        )
        for index, (title, score, fit) in enumerate(action_specs, start=1)
    )
    confidence = "Medium" if match_score >= 35 and min(q.values()) >= 35 else "Low"
    return DecisionReport(
        "startup",
        verdict,
        overall,
        confidence,
        "Eleven founder responses plus a transparent India Problem Observatory match",
        summary,
        options,
        risks,
        (
            "Answer quality measures specificity, behavioural evidence and falsifiability—not "
            "grammar, charisma or verbosity.",
            "White-space evidence can strengthen a real problem; novelty alone cannot make a "
            "weak problem investable.",
            "The assessment is decision support, not a prediction of startup success or valuation.",
        ),
        (
            f"Verify the matched problem evidence: {problem['remaining_gap']}",
            f"Design a time-boxed test for {fatal_unknown} with a pre-committed success threshold.",
            "Re-run the same eleven-question assessment after the test and compare the "
            "versioned scores.",
        ),
        (
            "Verified payment or repeat-use evidence can change the Horse score.",
            "A completed falsification milestone can change both evidence confidence and the "
            "Jockey score.",
            "Contradictory primary evidence can reverse any positive verdict.",
        ),
        evidence,
        dict(answers),
        manifest["artifact_id"],
        manifest["effective_date"],
        manifest["content_sha256"],
        policy["policy_version"],
    )

"""Build the precomputed Decision Atlas consumed by every consultation.

The atlas is the ConSaaS equivalent of Vriddhi's static research release: the
whole covered option universe is classified and scenario-tested before a user
arrives.  Live consultation only applies customer constraints to this release.
"""

from __future__ import annotations

import csv
import io
from typing import Any

from core.artifacts import canonical_json
from core.optimization import bounded, pareto_front

ATLAS_SCHEMA_VERSION = "1.0.0"


def _number(row: dict[str, str], key: str) -> float:
    return float(row[key])


def _career_features(row: dict[str, str]) -> dict[str, Any]:
    cost = _number(row, "total_cost_inr")
    counterfactual = _number(row, "counterfactual_salary_inr")
    duration = _number(row, "duration_years")
    economic_cost = cost + counterfactual * duration
    probability = (
        _number(row, "completion_probability_pct")
        * _number(row, "employment_probability_score")
        / 10_000
    )
    salary_uplift = max(0.0, _number(row, "salary_p50_inr") - counterfactual)
    risk_adjusted_uplift = salary_uplift * probability
    value_ratio = economic_cost / max(risk_adjusted_uplift, 1)
    downside_uplift = _number(row, "salary_p10_inr") - counterfactual
    pathway_score = bounded(
        0.28 * _number(row, "employability_score")
        + 0.18 * _number(row, "quality_score")
        + 0.14 * _number(row, "work_rights_score")
        + 0.14 * _number(row, "evidence_score")
        + 0.16 * bounded(110 - value_ratio * 12)
        + 0.10 * bounded(50 + downside_uplift / max(counterfactual, 1) * 20)
    )
    pathway = "Growth" if pathway_score >= 68 and downside_uplift > 0 else (
        "Stable" if pathway_score >= 52 else "Decline"
    )
    return {
        "record_id": row["record_id"],
        "option_name": row["option_name"],
        "segment": f"{row['degree_level']} · {row['field']} · {row['target_region']}",
        "pathway": pathway,
        "pathway_score": round(pathway_score, 2),
        "economic_cost_inr": round(economic_cost),
        "risk_adjusted_annual_uplift_inr": round(risk_adjusted_uplift),
        "cost_to_risk_adjusted_uplift": round(value_ratio, 2),
        "downside_salary_uplift_inr": round(downside_uplift),
        "authority_score": _number(row, "evidence_score"),
        "affordability_reference": bounded(100 - cost / 200_000),
        "resilience_reference": bounded(
            100 - (_number(row, "risk_score") + _number(row, "visa_uncertainty_score")) / 2
        ),
    }


def _house_features(row: dict[str, str]) -> dict[str, Any]:
    net_yield = (
        _number(row, "rental_yield_pct") * (1 - _number(row, "vacancy_pct") / 100)
        - _number(row, "maintenance_pct")
    )
    base_growth = _number(row, "price_growth_p50_pct")
    downside_growth = _number(row, "price_growth_p10_pct")
    growth_and_yield = base_growth + net_yield
    value_ratio = _number(row, "indicative_price_per_sqft") / max(growth_and_yield, 0.25)
    resilience = bounded(
        100
        - 0.24 * _number(row, "risk_score")
        - 0.22 * _number(row, "climate_risk_score")
        - 0.22 * _number(row, "water_risk_score")
        - 0.16 * _number(row, "supply_risk_score")
    )
    pathway_score = bounded(
        0.24 * _number(row, "growth_score")
        + 0.18 * _number(row, "liquidity_score")
        + 0.13 * _number(row, "liveability_score")
        + 0.10 * _number(row, "transit_score")
        + 0.12 * _number(row, "evidence_score")
        + 0.13 * resilience
        + 0.10 * bounded(45 + growth_and_yield * 5)
    )
    pathway = "Growth" if pathway_score >= 68 and downside_growth >= 0 else (
        "Stable" if pathway_score >= 52 else "Decline"
    )
    return {
        "record_id": row["record_id"],
        "option_name": row["option_name"],
        "segment": f"{row['city']} · {row['micro_market']}",
        "pathway": pathway,
        "pathway_score": round(pathway_score, 2),
        "net_rental_yield_pct": round(net_yield, 2),
        "base_growth_and_yield_pct": round(growth_and_yield, 2),
        "downside_price_growth_pct": downside_growth,
        "cost_to_growth_and_yield": round(value_ratio, 2),
        "authority_score": _number(row, "evidence_score"),
        "affordability_reference": bounded(100 - _number(row, "indicative_price_per_sqft") / 250),
        "resilience_reference": round(resilience, 2),
    }


def _startup_features(row: dict[str, str]) -> dict[str, Any]:
    reality = _number(row, "problem_reality_score")
    severity = _number(row, "severity_score")
    frequency = _number(row, "frequency_score")
    payer = _number(row, "willingness_to_pay_score")
    whitespace = _number(row, "whitespace_score")
    feasibility = _number(row, "regulatory_feasibility_score")
    coverage = _number(row, "solution_coverage_score")
    effectiveness = _number(row, "solution_effectiveness_score")
    opportunity = bounded(
        0.24 * reality
        + 0.17 * severity
        + 0.11 * frequency
        + 0.18 * payer
        + 0.16 * whitespace
        + 0.08 * feasibility
        + 0.06 * bounded(100 - coverage + effectiveness * 0.25)
    )
    saturation = bounded(coverage * 0.65 + effectiveness * 0.35)
    pathway = "Growth" if opportunity >= 70 and whitespace >= 55 else (
        "Persistent" if opportunity >= 52 else "Decline"
    )
    capital_to_evidence = bounded(115 - opportunity) / max(1.0, reality / 25)
    return {
        "record_id": row["record_id"],
        "option_name": row["problem_statement"],
        "segment": f"{row['domain']} · {row['subdomain']}",
        "pathway": pathway,
        "pathway_score": round(opportunity, 2),
        "problem_opportunity_score": round(opportunity, 2),
        "whitespace_score": whitespace,
        "payer_confidence_score": payer,
        "solution_saturation_score": round(saturation, 2),
        "capital_to_evidence_ratio": round(capital_to_evidence, 2),
        "authority_score": 65.0 if row["confidence"] == "medium" else 45.0,
        "affordability_reference": bounded(100 - capital_to_evidence * 3),
        "resilience_reference": feasibility,
    }


def _csv_bytes(rows: list[dict[str, Any]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def build_decision_atlas(
    product_id: str,
    rows: list[dict[str, str]],
    *,
    effective_date: str,
    source_hash: str,
) -> dict[str, bytes]:
    """Return the complete immutable research bundle for a candidate release."""
    builders = {
        "careersim": _career_features,
        "housewise": _house_features,
        "startup": _startup_features,
    }
    features = [builders[product_id](row) for row in rows]
    frontier_indices = pareto_front(
        [
            {
                "pathway": float(item["pathway_score"]),
                "authority": float(item["authority_score"]),
                "affordability": float(item["affordability_reference"]),
                "resilience": float(item["resilience_reference"]),
            }
            for item in features
        ],
        ("pathway", "authority", "affordability", "resilience"),
    )
    frontier_ids = [features[index]["record_id"] for index in frontier_indices]
    scenarios = [
        {
            "record_id": item["record_id"],
            "downside": round(float(item["pathway_score"]) * 0.72, 2),
            "base": item["pathway_score"],
            "upside": round(min(100.0, float(item["pathway_score"]) * 1.16), 2),
        }
        for item in features
    ]
    counts = {label: sum(item["pathway"] == label for item in features) for label in (
        "Growth", "Stable", "Persistent", "Decline"
    )}
    atlas = {
        "schema_version": ATLAS_SCHEMA_VERSION,
        "product_id": product_id,
        "effective_date": effective_date,
        "source_hash": source_hash,
        "universe_size": len(features),
        "pathway_counts": {key: value for key, value in counts.items() if value},
        "frontier_ids": frontier_ids,
        "entries": features,
        "live_contract": (
            "Apply confirmed customer constraints to this precomputed universe; do not train, "
            "research or invent universe facts during consultation."
        ),
    }
    model_card = {
        "model_id": f"{product_id}-transparent-baseline-v1",
        "champion": True,
        "model_family": "deterministic multi-criteria scenario model",
        "learned_model_status": "not promoted",
        "reason": (
            "The current curated release is cross-sectional and does not provide sufficient "
            "out-of-time labelled outcomes. A learned challenger may be promoted only after it "
            "beats this baseline on temporal holdouts and downside calibration."
        ),
        "authoritative_outputs": ["pathway", "pathway_score", "frontier membership"],
        "prohibited_claim": "prediction of guaranteed individual success",
    }
    backtest = {
        "status": "insufficient_longitudinal_outcomes",
        "temporal_split": None,
        "champion_gate": "baseline retained",
        "required_before_ml_promotion": [
            "dated historical vintages",
            "realised outcome labels",
            "out-of-time ranking lift",
            "downside calibration",
            "subgroup stability",
        ],
    }
    classification = [
        {
            "record_id": item["record_id"],
            "pathway": item["pathway"],
            "pathway_score": item["pathway_score"],
            "on_pareto_frontier": item["record_id"] in frontier_ids,
        }
        for item in features
    ]
    return {
        "feature_matrix.csv": _csv_bytes(features),
        "growth_decline_classification.csv": _csv_bytes(classification),
        "scenario_matrix.json": canonical_json(scenarios),
        "pareto_fronts.json": canonical_json({"default_frontier_ids": frontier_ids}),
        "decision_atlas.json": canonical_json(atlas),
        "model_card.json": canonical_json(model_card),
        "backtest_evidence.json": canonical_json(backtest),
    }

"""Product manifests and governed configuration loading."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from plugin_sdk.decision import Question


@dataclass(frozen=True, slots=True)
class ProductCard:
    product_id: str
    name: str
    domain: str
    promise: str
    accent: str
    icon: str


PRODUCTS = {
    "careersim": ProductCard(
        "careersim",
        "CareerSim",
        "Overseas education ROI intelligence",
        "Help Indian students test whether an overseas degree is worth its full cost and risk.",
        "#315b7d",
        "◎",
    ),
    "housewise": ProductCard(
        "housewise",
        "HouseWise",
        "Real estate intelligence",
        "Buy with a clear view of affordability, liveability, liquidity and downside risk.",
        "#8b5e34",
        "⌂",
    ),
    "startup": ProductCard(
        "startup",
        "StartupEval",
        "Venture intelligence",
        "Find the strongest evidence, the fatal unknown and the next decision worth funding.",
        "#516b52",
        "△",
    ),
}


def _json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def load_questions(root: Path, product_id: str) -> tuple[Question, ...]:
    raw = _json(root / product_id / "questions.json")
    return tuple(
        Question(
            question_id=item["id"],
            prompt=item["prompt"],
            answer_type=item["type"],
            options=tuple(item.get("options", [])),
            minimum=item.get("min"),
            maximum=item.get("max"),
            step=item.get("step"),
            default=item.get("default"),
            importance=int(item.get("importance", 50)),
            why_it_matters=str(item.get("why_it_matters", "")),
            expert_context=str(item.get("expert_context", "")),
        )
        for item in raw["questions"]
    )


def load_policy(root: Path, product_id: str) -> dict[str, Any]:
    return _json(root / product_id / "decision_policy.json")


def load_current_gka(root: Path, product_id: str) -> tuple[list[dict[str, str]], dict[str, Any]]:
    pointer = _json(root / "knowledge" / "releases" / product_id / "current.json")
    release = root / pointer["release_path"]
    manifest = _json(release / "manifest.json")
    with (release / "grand_knowledge_asset.csv").open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return rows, manifest


def load_skill(root: Path, product_id: str) -> str:
    return (root / product_id / "SKILL.md").read_text(encoding="utf-8")


def load_metric_catalog(root: Path, product_id: str) -> dict[str, Any]:
    pointer = _json(root / "knowledge" / "releases" / product_id / "current.json")
    return _json(root / pointer["release_path"] / "metric_catalog.json")

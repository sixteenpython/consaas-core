from __future__ import annotations

import json
import shutil
from datetime import date
from pathlib import Path

import pytest

from core.refresh import RefreshError, refresh_all, refresh_product


def _workspace(tmp_path: Path) -> Path:
    root = Path(__file__).parents[2]
    for product in ("careersim", "housewise", "startup"):
        shutil.copytree(root / product, tmp_path / product)
    return tmp_path


def test_monthly_refresh_promotes_all_products_and_is_idempotent(tmp_path: Path) -> None:
    root = _workspace(tmp_path)
    effective = date(2026, 8, 22)

    first = refresh_all(root, effective)
    second = refresh_all(root, effective)

    assert [item.status for item in first] == ["promoted", "promoted", "promoted"]
    assert [item.status for item in second] == ["unchanged", "unchanged", "unchanged"]
    for item in first:
        pointer = json.loads(
            (root / "knowledge" / "releases" / item.product_id / "current.json").read_text()
        )
        assert pointer["content_sha256"] == item.content_sha256
        assert (root / pointer["release_path"] / "quality.json").exists()
        assert (root / pointer["release_path"] / "metric_catalog.json").exists()


def test_invalid_candidate_does_not_replace_current_release(tmp_path: Path) -> None:
    root = _workspace(tmp_path)
    refresh_product(root, "careersim", date(2026, 8, 22))
    pointer_path = root / "knowledge" / "releases" / "careersim" / "current.json"
    before = pointer_path.read_bytes()
    seed = root / "careersim" / "data" / "seed.csv"
    seed.write_text("record_id,option_name\n,broken\n", encoding="utf-8")

    with pytest.raises(RefreshError, match="failed validation"):
        refresh_product(root, "careersim", date(2026, 9, 22))

    assert pointer_path.read_bytes() == before


def test_tagged_methodology_release_preserves_same_day_history(tmp_path: Path) -> None:
    root = _workspace(tmp_path)
    effective = date(2026, 8, 23)
    baseline = refresh_product(root, "careersim", effective)
    tagged = refresh_product(root, "careersim", effective, "decision-intelligence-v1")

    assert baseline.release_dir.exists()
    assert tagged.release_dir.name == "2026-08-23-decision-intelligence-v1"
    assert (tagged.release_dir / "source_catalog.json").exists()
    assert (tagged.release_dir / "validation_report.json").exists()

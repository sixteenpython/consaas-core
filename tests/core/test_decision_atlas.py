from __future__ import annotations

from pathlib import Path

from decision_studio.catalog import load_decision_atlas


def test_current_releases_cover_the_whole_declared_universe() -> None:
    root = Path(__file__).parents[2]
    for product_id, expected in (("careersim", 26), ("housewise", 28), ("startup", 30)):
        atlas = load_decision_atlas(root, product_id)
        assert atlas["universe_size"] == expected
        assert len(atlas["entries"]) == expected
        assert atlas["frontier_ids"]
        assert sum(atlas["pathway_counts"].values()) == expected

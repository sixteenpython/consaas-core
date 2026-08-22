from __future__ import annotations

from decision_studio.case import CaseKnowledgeAsset


def test_case_asset_preserves_confirmed_revision_history() -> None:
    case = CaseKnowledgeAsset("careersim").confirm("degree_level", "Master's")
    revised = case.confirm("degree_level", "PhD", reason="User corrected degree level")

    assert revised.values == {"degree_level": "PhD"}
    assert revised.revisions[0].previous_value == "Master's"
    assert revised.revisions[0].new_value == "PhD"
    assert case.values == {"degree_level": "Master's"}


def test_reconfirming_same_value_does_not_create_revision() -> None:
    case = CaseKnowledgeAsset("housewise").confirm("city", "Pune")
    assert not case.confirm("city", "Pune").revisions


def test_unknown_fact_is_visible_but_not_decision_ready() -> None:
    case = CaseKnowledgeAsset("careersim").mark("budget_inr", "unknown")

    assert case.values == {}
    assert case.fact_map["budget_inr"].status == "unknown"
    assert case.unresolved_ids == frozenset({"budget_inr"})


def test_resolving_unknown_fact_preserves_epistemic_revision() -> None:
    unknown = CaseKnowledgeAsset("careersim").mark("budget_inr", "unknown")
    resolved = unknown.confirm("budget_inr", 6_000_000)

    assert resolved.values == {"budget_inr": 6_000_000}
    assert resolved.revisions[0].previous_status == "unknown"
    assert resolved.revisions[0].new_status == "confirmed"

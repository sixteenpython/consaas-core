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

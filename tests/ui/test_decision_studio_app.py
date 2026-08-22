from __future__ import annotations

from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_landing_and_complete_careersim_journey() -> None:
    app = AppTest.from_file(str(Path(__file__).parents[2] / "streamlit_app.py")).run(timeout=30)
    assert not app.exception
    visible = "\n".join(item.value for item in (*app.markdown, *app.caption, *app.warning))
    assert "ConSaaS Core" in visible
    assert "CareerSim" in visible
    assert "HouseWise" in visible
    assert "StartupEval" in visible

    next(button for button in app.button if button.label == "Start CareerSim").click().run(
        timeout=30
    )
    assert not app.exception
    assert [tab.label for tab in app.tabs] == [
        "Consultant",
        "Decision Brief",
        "Recommendation",
        "Knowledge Asset",
        "Method",
    ]
    for _ in range(14):
        if app.session_state["consultations"]["careersim"]["report"] is not None:
            break
        buttons = [
            button for button in app.button if button.label == "Preserve answer and continue"
        ]
        assert buttons
        buttons[-1].click().run(timeout=30)
        assert not app.exception
    assert app.session_state["consultations"]["careersim"]["report"] is not None
    assert any("decision brief is complete" in item.value.lower() for item in app.success)

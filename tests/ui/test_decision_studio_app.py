from __future__ import annotations

from pathlib import Path

import pytest
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
    assert any("decision position is complete" in item.value.lower() for item in app.success)


def test_consultant_accepts_unknown_in_free_form_conversation() -> None:
    app = AppTest.from_file(str(Path(__file__).parents[2] / "streamlit_app.py")).run(timeout=30)
    next(button for button in app.button if button.label == "Start CareerSim").click().run(
        timeout=30
    )

    app.chat_input[0].set_value("I don't know yet").run(timeout=30)

    case = app.session_state["consultations"]["careersim"]["case"]
    assert case.facts[0].status == "unknown"
    assert case.values == {}
    visible = "\n".join(item.value for item in (*app.markdown, *app.caption))
    assert "will not invent" in visible


@pytest.mark.parametrize(
    ("product_name", "product_id", "maximum_steps"),
    [("HouseWise", "housewise", 12), ("StartupEval", "startup", 15)],
)
def test_every_consultant_completes_without_model_inference(
    product_name: str, product_id: str, maximum_steps: int
) -> None:
    app = AppTest.from_file(str(Path(__file__).parents[2] / "streamlit_app.py")).run(timeout=30)
    next(button for button in app.button if button.label == f"Start {product_name}").click().run(
        timeout=30
    )
    for _ in range(maximum_steps):
        if app.session_state["consultations"][product_id]["report"] is not None:
            break
        buttons = [
            button for button in app.button if button.label == "Preserve answer and continue"
        ]
        assert buttons
        if product_id == "startup":
            next(
                area for area in app.text_area if str(area.key).startswith("answer-startup-")
            ).set_value(
                "We observed 20 customers, tested a paid pilot, measured repeat usage and changed "
                "the product after evidence. The next 8-week milestone has a ₹2 lakh budget and "
                "a defined pass or fail threshold."
            ).run(timeout=30)
            buttons = [
                button for button in app.button if button.label == "Preserve answer and continue"
            ]
        buttons[-1].click().run(timeout=30)
        assert not app.exception
    assert app.session_state["consultations"][product_id]["report"] is not None

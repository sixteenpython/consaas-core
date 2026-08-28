import pytest

AppTest = pytest.importorskip("streamlit.testing.v1").AppTest


def test_screenplay_builder_renders_without_exception() -> None:
    app = AppTest.from_file("narrative/streamlit_app.py")

    app.run(timeout=30)

    assert not app.exception
    assert [tab.label for tab in app.tabs] == [
        "1 · Centre Knot",
        "2 · Characters",
        "3 · Full Plot",
        "4 · Structure",
        "5 · Scene Construction",
        "6 · Build & Score",
    ]
    visible_text = "\n".join(
        item.value for collection in (app.markdown, app.caption, app.warning) for item in collection
    )
    assert "Narrative Architect" in visible_text
    assert "Skill-library intelligence" in visible_text
    assert "Builder v0.3.0" in visible_text
    assert "Hosted construction demo" in visible_text

    next(button for button in app.button if button.label == "Load demo").click().run(timeout=30)

    metric_labels = {metric.label for metric in app.metric}
    assert {"Completion coverage", "Craft quality", "Scenes needing craft pass"}.issubset(
        metric_labels
    )

import pytest

AppTest = pytest.importorskip("streamlit.testing.v1").AppTest


def test_foundation_alpha_renders_without_exception() -> None:
    app = AppTest.from_file("narrative/streamlit_app.py")

    app.run(timeout=30)

    assert not app.exception
    assert [tab.label for tab in app.tabs] == [
        "Create",
        "Knowledge",
        "Characters",
        "Scenes",
        "Compile",
        "Doctor · Roadmap",
    ]
    visible_text = "\n".join(
        item.value for collection in (app.markdown, app.caption, app.warning) for item in collection
    )
    assert "Narrative Architect" in visible_text
    assert "No external LLM" in visible_text
    assert "Hosted demonstration profile" in visible_text

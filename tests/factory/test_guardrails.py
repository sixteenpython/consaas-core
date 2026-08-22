from pathlib import Path

from factory.guardrails import _cycles, inspect_python


def test_cross_product_import_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "narrative" / "service.py"
    path.parent.mkdir()
    path.write_text("from vriddhi.engine import decide\n", encoding="utf-8")

    violations = inspect_python(path, tmp_path)

    assert any("cross-product import" in item.message for item in violations)


def test_provider_import_is_allowed_only_in_adapter(tmp_path: Path) -> None:
    path = tmp_path / "narrative" / "chat.py"
    path.parent.mkdir()
    path.write_text("import ollama\n", encoding="utf-8")

    violations = inspect_python(path, tmp_path)

    assert any("provider SDK" in item.message for item in violations)


def test_module_dependency_cycle_is_reported() -> None:
    graph = {"core": {"factory"}, "factory": {"core"}}

    assert _cycles(graph) == [("core", "factory", "core")]

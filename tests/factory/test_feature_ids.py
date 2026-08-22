import importlib.util
from pathlib import Path
from types import ModuleType


def _module() -> ModuleType:
    path = Path("skills/feature-creator/scripts/next_feature_id.py")
    spec = importlib.util.spec_from_file_location("feature_ids", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_next_id_uses_highest_existing_namespace_number(tmp_path: Path) -> None:
    (tmp_path / "one.md").write_text("NARRATIVE-001", encoding="utf-8")
    (tmp_path / "two.json").write_text('{"id":"NARRATIVE-003"}', encoding="utf-8")

    assert _module().next_id(tmp_path, "narrative") == "NARRATIVE-004"


def test_next_id_does_not_mix_namespaces(tmp_path: Path) -> None:
    (tmp_path / "items.md").write_text("CORE-099 NARRATIVE-002", encoding="utf-8")

    assert _module().next_id(tmp_path, "narrative") == "NARRATIVE-003"

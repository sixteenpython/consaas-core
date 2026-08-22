"""Static architecture checks used locally and in CI."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

PRODUCTS = {"vriddhi", "narrative", "housewise", "careersim", "startup"}
MODULE_ROOTS = PRODUCTS | {"core", "factory"}
FORBIDDEN_PROVIDER_IMPORTS = {"openai", "anthropic", "google.generativeai", "ollama"}
IMPORT_RE = re.compile(r"^\s*(?:from|import)\s+([a-zA-Z_][\w.]*)", re.MULTILINE)


@dataclass(frozen=True, slots=True)
class Violation:
    path: Path
    message: str


def _product_for(path: Path) -> str | None:
    return next((part.lower() for part in path.parts if part.lower() in PRODUCTS), None)


def _module_root(path: Path) -> str | None:
    return next((part.lower() for part in path.parts if part.lower() in MODULE_ROOTS), None)


def inspect_python(path: Path, root: Path) -> list[Violation]:
    relative = path.relative_to(root)
    text = path.read_text(encoding="utf-8")
    owner = _product_for(relative)
    violations: list[Violation] = []
    for imported in IMPORT_RE.findall(text):
        top = imported.split(".")[0].lower()
        if owner and top in PRODUCTS and top != owner:
            violations.append(Violation(relative, f"cross-product import of {top}"))
        if imported in FORBIDDEN_PROVIDER_IMPORTS or top in FORBIDDEN_PROVIDER_IMPORTS:
            allowed = relative.parts[:3] == ("core", "ai", "adapters")
            if not allowed:
                violations.append(
                    Violation(
                        relative, f"provider SDK {imported} must be isolated in core/ai/adapters"
                    )
                )
    if re.search(r"(?i)(api[_-]?key|secret|token)\s*=\s*['\"][^'\"]{8,}['\"]", text):
        violations.append(Violation(relative, "possible hard-coded secret"))
    return violations


def scan(root: Path) -> list[Violation]:
    excluded = {
        ".git",
        ".venv",
        "__pycache__",
        ".pytest_cache",
        ".pytest-tmp",
        ".mypy_cache",
    }
    python_paths = [
        path
        for path in root.rglob("*.py")
        if not excluded.intersection(path.relative_to(root).parts)
    ]
    violations = [violation for path in python_paths for violation in inspect_python(path, root)]
    graph: dict[str, set[str]] = {name: set() for name in MODULE_ROOTS}
    for path in python_paths:
        owner = _module_root(path.relative_to(root))
        if owner is None:
            continue
        for imported in IMPORT_RE.findall(path.read_text(encoding="utf-8")):
            target = imported.split(".")[0].lower()
            if target in MODULE_ROOTS and target != owner:
                graph[owner].add(target)
    cycles = _cycles(graph)
    violations.extend(
        Violation(Path("."), f"module dependency cycle: {' -> '.join(cycle)}") for cycle in cycles
    )
    return violations


def _cycles(graph: dict[str, set[str]]) -> list[tuple[str, ...]]:
    cycles: set[tuple[str, ...]] = set()

    def visit(node: str, path: tuple[str, ...]) -> None:
        if node in path:
            cycle = path[path.index(node) :] + (node,)
            rotations = [cycle[index:-1] + cycle[:index] for index in range(len(cycle) - 1)]
            cycles.add(min(rotations) + (min(rotations)[0],))
            return
        for target in graph[node]:
            visit(target, path + (node,))

    for node in graph:
        visit(node, ())
    return sorted(cycles)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    violations = scan(args.root.resolve())
    for violation in violations:
        print(f"{violation.path}: {violation.message}")
    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())

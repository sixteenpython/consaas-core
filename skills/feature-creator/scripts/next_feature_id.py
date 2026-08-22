#!/usr/bin/env python3
"""Allocate the next unused ConSaaS work-item ID by scanning repository text."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".toml"}
EXCLUDED_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache", ".mypy_cache"}


def existing_numbers(repo: Path, namespace: str) -> set[int]:
    pattern = re.compile(rf"\b{re.escape(namespace.upper())}-(\d{{3,}})\b")
    numbers: set[int] = set()
    for path in repo.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if EXCLUDED_PARTS.intersection(path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        numbers.update(int(match) for match in pattern.findall(text))
    return numbers


def next_id(repo: Path, namespace: str) -> str:
    normalized = namespace.strip().upper()
    if not re.fullmatch(r"[A-Z][A-Z0-9]*", normalized):
        raise ValueError("namespace must contain only uppercase letters and digits")
    used = existing_numbers(repo.resolve(), normalized)
    candidate = max(used, default=0) + 1
    while candidate in used:
        candidate += 1
    return f"{normalized}-{candidate:03d}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--namespace", required=True)
    args = parser.parse_args()
    print(next_id(args.repo, args.namespace))


if __name__ == "__main__":
    main()

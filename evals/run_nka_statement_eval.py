"""Offline contract evaluation for the NARRATIVE-001 boundary."""

from __future__ import annotations

import json
from pathlib import Path

from narrative_architect.knowledge.statements import (
    StatementValidationError,
    validate_model_statement,
)


def main() -> int:
    cases = json.loads(
        Path("evals/narrative/nka_statement_validation_cases.json").read_text(encoding="utf-8")
    )
    failures: list[str] = []
    for case in cases:
        try:
            validate_model_statement(case["input"])
            actual = True
        except StatementValidationError:
            actual = False
        if actual is not case["accepted"]:
            failures.append(case["name"])
    print(f"NKA statement gate: {len(cases) - len(failures)}/{len(cases)} cases passed")
    if failures:
        print("Failed: " + ", ".join(failures))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

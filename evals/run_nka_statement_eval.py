"""Offline contract evaluation for the NARRATIVE-001 boundary."""

from __future__ import annotations

import json
import sys
from pathlib import Path

NARRATIVE_SOURCE = Path(__file__).resolve().parents[1] / "narrative" / "src"
if str(NARRATIVE_SOURCE) not in sys.path:
    sys.path.insert(0, str(NARRATIVE_SOURCE))

from narrative_architect.knowledge.statements import (  # noqa: E402
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

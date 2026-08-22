"""Offline golden evaluation for the governed deterministic dialogue fallback."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from decision_studio.conversation import deterministic_action  # noqa: E402
from plugin_sdk.decision import Question  # noqa: E402


def main() -> int:
    fixture = json.loads(
        (ROOT / "evals" / "core" / "dialogue_action_cases.json").read_text(encoding="utf-8")
    )
    question = Question(
        "career_goal",
        "What is your intended path after graduation?",
        "choice",
        ("Work overseas long term", "Return to India soon after graduation", "Undecided"),
        why_it_matters="The earning market changes the ROI.",
        expert_context="Use the salary market the student is likely to enter.",
    )
    failures: list[str] = []
    for case in fixture["cases"]:
        action = deterministic_action(case["message"], question)
        if action.intent != case["expected_intent"]:
            failures.append(
                f"{case['id']}: expected {case['expected_intent']}, got {action.intent}"
            )
        if "expected_value" in case and action.value != case["expected_value"]:
            failures.append(f"{case['id']}: extracted value mismatch")
        if case.get("prohibited_persistence") and action.value is not None:
            failures.append(f"{case['id']}: non-answer proposed persistence")
    if failures:
        for failure in failures:
            print(failure)
        return 1
    print(f"Dialogue action evaluation passed: {len(fixture['cases'])} cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Evidence-grounded progressive disclosure over a frozen DecisionReport."""

from __future__ import annotations

from plugin_sdk.decision import DecisionReport


def report_to_markdown(report: DecisionReport) -> str:
    """Render a portable human-readable decision report."""
    lines = [
        f"# {report.product_id.title()} Decision Report",
        "",
        f"## Verdict: {report.verdict}",
        "",
        report.summary,
        "",
        "## Three best moves",
        "",
    ]
    for index, option in enumerate(report.options, 1):
        lines.extend(
            [
                f"### {index}. {option.title}",
                "",
                f"**Fit:** {option.fit}",
                "",
                *(f"- {reason}" for reason in option.reasons),
                "",
            ]
        )
    sections = (
        ("Do next", report.next_actions),
        ("Principal risks", report.risks),
        ("What would change the verdict", report.change_conditions),
        ("Assumptions", report.assumptions),
        ("Evidence", report.evidence),
    )
    for title, items in sections:
        lines.extend([f"## {title}", "", *(f"- {item}" for item in items), ""])
    lines.extend(
        [
            "## Provenance",
            "",
            f"- Knowledge asset: `{report.gka_artifact_id}`",
            f"- Effective date: {report.gka_effective_date}",
            f"- Policy: {report.policy_version}",
            f"- SHA-256: `{report.gka_hash}`",
        ]
    )
    return "\n".join(lines)


def answer_report_question(report: DecisionReport, question: str) -> str:
    """Answer common follow-ups without changing or embellishing the report."""
    text = question.casefold()
    top = report.options[0] if report.options else None
    if any(word in text for word in ("why", "reason", "recommend")) and top:
        reasons = "\n".join(f"- {reason}" for reason in top.reasons)
        return f"**Why this is the leading move**\n\n{reasons}"
    if any(word in text for word in ("risk", "downside", "wrong", "fail")):
        risks = "\n".join(f"- {risk}" for risk in report.risks[:5])
        return f"**The risks that matter most**\n\n{risks}"
    if any(word in text for word in ("change", "reverse", "different", "condition")):
        items = "\n".join(f"- {item}" for item in report.change_conditions)
        return f"**What could change the verdict**\n\n{items}"
    if any(word in text for word in ("evidence", "source", "provenance", "data")):
        items = "\n".join(f"- {item}" for item in report.evidence[:8])
        return f"**Evidence behind this decision**\n\n{items}"
    if any(word in text for word in ("next", "do", "action", "start")):
        items = "\n".join(f"{index}. {item}" for index, item in enumerate(report.next_actions, 1))
        return f"**What I would do next**\n\n{items}"
    if any(word in text for word in ("option", "alternative", "second", "third")):
        items = "\n".join(
            f"{index}. **{option.title}** — {option.fit}"
            for index, option in enumerate(report.options, 1)
        )
        return f"**The three best covered moves**\n\n{items}"
    return (
        f"**My decision remains: {report.verdict}.**\n\n{report.summary}\n\n"
        "You can ask me *why this option*, *what could go wrong*, *what would change the "
        "verdict*, *show the evidence*, or *what should I do next*."
    )

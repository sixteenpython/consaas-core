# ruff: noqa: E501
"""Deterministic bounded Fountain compiler for accepted NKA content."""

from __future__ import annotations

from dataclasses import dataclass

from narrative_architect.construction.scoring import assess_screenplay
from narrative_architect.knowledge.nka import NarrativeState, NKARevision

COMPILER_VERSION = "screenplay-fountain/2"


@dataclass(frozen=True, slots=True)
class ReadinessReport:
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]

    @property
    def can_compile(self) -> bool:
        return not self.blockers


def assess_readiness(state: NarrativeState) -> ReadinessReport:
    blockers: list[str] = []
    warnings: list[str] = []
    if not state.centre_knot:
        blockers.append("Lock the one-line centre knot.")
    if not state.characters:
        blockers.append("Add at least one character.")
    if not state.scenes:
        blockers.append("Add at least one scene.")
    if not state.full_plot:
        blockers.append("Lock the full plot.")
    if not state.structure_type or not state.beats:
        blockers.append("Map the screenplay structure.")
    if any("TO BE REFINED" in scene.heading for scene in state.scenes):
        warnings.append(
            "Refine provisional scene headings before treating this as a screenplay draft."
        )
    if not state.ending:
        warnings.append("The ending remains open.")
    if any(not (scene.objective and scene.conflict and scene.outcome) for scene in state.scenes):
        warnings.append("One or more scenes lack objective, conflict or outcome.")
    if 5 not in state.locked_phases:
        warnings.append("Scene construction has not been marked build complete.")
    return ReadinessReport(tuple(blockers), tuple(warnings))


def compile_bounded_fountain(revision: NKARevision) -> str:
    report = assess_readiness(revision.state)
    if not report.can_compile:
        raise ValueError("Compilation blocked: " + " ".join(report.blockers))
    state = revision.state
    lines = [
        f"Title: {state.title}",
        "Credit: Narrative Architect construction draft",
        "Draft date: Canonical revision " + revision.revision_id[:12],
        "Notes: Generated only from the accepted Narrative Knowledge Asset.",
        "",
    ]
    for scene in state.scenes:
        heading = scene.heading.upper()
        if not heading.startswith(("INT.", "EXT.", "INT/EXT.", "I/E.")):
            location = scene.location.upper() or heading
            heading = f"INT. {location} - {scene.time_of_day.upper()}"
        lines.extend([heading, "", scene.summary, ""])
        if scene.blocking:
            lines.extend([scene.blocking, ""])
        if scene.objective:
            lines.extend([f"/* Scene objective: {scene.objective} */", ""])
        if scene.conflict:
            lines.extend([f"/* Conflict: {scene.conflict} */", ""])
        if scene.outcome:
            lines.extend([f"/* Outcome: {scene.outcome} */", ""])
        if scene.dialogue_text:
            character_name = next(
                (
                    character.name
                    for character in state.characters
                    if character.character_id == scene.viewpoint_character_id
                ),
                "CHARACTER",
            )
            lines.extend([character_name.upper(), scene.dialogue_text, ""])
    lines.extend(
        [
            "===",
            f"Compiler: {COMPILER_VERSION}",
            f"Source NKA revision: {revision.revision_id}",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def compile_scorecard_markdown(revision: NKARevision) -> str:
    """Compile an evidence-facing construction scorecard bound to one NKA revision."""
    state = revision.state
    report = assess_screenplay(state)
    lines = [
        f"# {state.title} — First-draft construction scorecard",
        "",
        f"**Source NKA revision:** `{revision.revision_id}`  ",
        f"**Structure:** {state.structure_type or 'Not established'}  ",
        f"**Structural coverage:** {report.coverage_percent}%  ",
        f"**iMaSc construction score:** {report.imasc_construction_score_0_5:.2f}/5",
        "",
        "> This score measures explicit screenplay-construction coverage under the declared rubric. It is not an IMDb score and is not a prediction of audience or commercial success.",
        "",
        "## Scene scorecard",
        "",
        "| # | Scene | Conflict | Character | Plot | Blocking | Placement | Weighted |",
        "|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for index, card in enumerate(report.scenes, 1):
        values = {dimension.name: dimension.score_0_5 for dimension in card.dimensions}
        lines.append(
            f"| {index} | {card.scene_heading} | {values['Conflict']} | "
            f"{values['Character development']} | {values['Plot function']} | "
            f"{values['Blocking & staging']} | {values['Placement']} | {card.weighted_score_0_5:.2f} |"
        )
    if report.strengths:
        lines.extend(["", "## Construction strengths", *[f"- {item}" for item in report.strengths]])
    if report.priorities:
        lines.extend(
            ["", "## Next revision priorities", *[f"- {item}" for item in report.priorities]]
        )
    lines.extend(["", f"Compiler: `{COMPILER_VERSION}`"])
    return "\n".join(lines).strip() + "\n"

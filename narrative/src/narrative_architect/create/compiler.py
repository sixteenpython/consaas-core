"""Deterministic bounded Fountain compiler for accepted NKA content."""

from __future__ import annotations

from dataclasses import dataclass

from narrative_architect.knowledge.nka import NarrativeState, NKARevision

COMPILER_VERSION = "foundation-fountain/1"


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
    if not state.premise:
        blockers.append("Establish the premise.")
    if not state.characters:
        blockers.append("Add at least one character.")
    if not state.scenes:
        blockers.append("Add at least one scene.")
    if len(state.scenes) < 3:
        warnings.append("The Foundation Alpha is strongest with at least three scenes.")
    if any("TO BE REFINED" in scene.heading for scene in state.scenes):
        warnings.append(
            "Refine provisional scene headings before treating this as a screenplay draft."
        )
    if not state.ending:
        warnings.append("The ending remains open.")
    if any(not scene.objective for scene in state.scenes):
        warnings.append("One or more scenes do not yet state a scene objective.")
    return ReadinessReport(tuple(blockers), tuple(warnings))


def compile_bounded_fountain(revision: NKARevision) -> str:
    report = assess_readiness(revision.state)
    if not report.can_compile:
        raise ValueError("Compilation blocked: " + " ".join(report.blockers))
    state = revision.state
    lines = [
        f"Title: {state.title}",
        "Credit: Foundation Alpha bounded draft",
        "Draft date: Canonical revision " + revision.revision_id[:12],
        "Notes: This partial draft contains only author-confirmed NKA content.",
        "",
    ]
    for scene in state.scenes:
        heading = scene.heading.upper()
        if not heading.startswith(("INT.", "EXT.", "INT/EXT.", "I/E.")):
            location = scene.location.upper() or heading
            heading = f"INT. {location} - {scene.time_of_day.upper()}"
        lines.extend([heading, "", scene.summary, ""])
        if scene.objective:
            lines.extend([f"/* Scene objective: {scene.objective} */", ""])
        if scene.conflict:
            lines.extend([f"/* Conflict: {scene.conflict} */", ""])
        if scene.outcome:
            lines.extend([f"/* Outcome: {scene.outcome} */", ""])
    lines.extend(
        [
            "===",
            f"Compiler: {COMPILER_VERSION}",
            f"Source NKA revision: {revision.revision_id}",
        ]
    )
    return "\n".join(lines).strip() + "\n"

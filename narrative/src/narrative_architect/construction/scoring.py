"""Deterministic completion and craft-evidence scoring for screenplay construction."""

from __future__ import annotations

import re
from dataclasses import dataclass

from narrative_architect.knowledge.nka import NarrativeState, Scene

WEIGHTS = {
    "Conflict": 0.20,
    "Character development": 0.25,
    "Plot function": 0.30,
    "Blocking & staging": 0.15,
    "Placement": 0.10,
}

BOILERPLATE_MARKERS = (
    "opening state space",
    "the counterforce makes the approved central conflict immediate",
    "the first tactic fails and forces a more revealing, costly action",
    "a choice changes the meaning or direction",
    "the event is completed and causally launches",
    "the viewpoint character leaves with a changed belief",
    "the character demonstrates the arc through a visible choice",
    "both sides want incompatible outcomes",
    "a short tactical exchange turns",
    "the spoken objective masks the relationship need",
    "movement through the location externalizes",
    "pays or plants a specific story element",
)

SCAFFOLD_MARKERS = (
    "the scene inherits a concrete consequence",
    "the collision makes the central conflict playable",
    "the declared stakes into the room",
    "becomes the point of struggle",
    "the choice cracks",
    "becomes the physical setup for",
)

PLACEHOLDER_CHARACTER_NAMES = {
    "the builder",
    "the counterforce",
    "the truth teller",
    "the living stake",
}

_STOPWORDS = {
    "about",
    "after",
    "again",
    "against",
    "along",
    "also",
    "because",
    "before",
    "being",
    "between",
    "cannot",
    "central",
    "character",
    "choice",
    "conflict",
    "could",
    "event",
    "every",
    "first",
    "from",
    "have",
    "inside",
    "into",
    "makes",
    "must",
    "objective",
    "other",
    "outcome",
    "scene",
    "screenplay",
    "should",
    "story",
    "their",
    "there",
    "these",
    "through",
    "under",
    "until",
    "while",
    "with",
    "would",
}

_COMPLETION_FIELDS = (
    "heading",
    "summary",
    "location",
    "time_of_day",
    "structural_beat_id",
    "viewpoint_character_id",
    "entry_state",
    "objective",
    "conflict",
    "escalation",
    "turning_point",
    "outcome",
    "emotional_change",
    "character_behavior",
    "dialogue_context",
    "dialogue_text",
    "dialogue_subtext",
    "blocking",
    "setup_payoff",
    "character_ids",
)


@dataclass(frozen=True, slots=True)
class DimensionScore:
    name: str
    score_0_5: int
    weight: float
    evidence: str


@dataclass(frozen=True, slots=True)
class SceneScorecard:
    scene_id: str
    scene_heading: str
    dimensions: tuple[DimensionScore, ...]
    completion_score_0_5: float
    weighted_score_0_5: float
    quality_flags: tuple[str, ...]

    @property
    def craft_quality_score_0_5(self) -> float:
        return self.weighted_score_0_5


@dataclass(frozen=True, slots=True)
class ScreenplayScorecard:
    scenes: tuple[SceneScorecard, ...]
    completion_coverage_score_0_5: float
    craft_quality_score_0_5: float
    coverage_percent: int
    template_scene_count: int
    strengths: tuple[str, ...]
    priorities: tuple[str, ...]

    @property
    def imasc_construction_score_0_5(self) -> float:
        """Compatibility alias; the honest product label is craft quality."""

        return self.craft_quality_score_0_5


def _score(checks: tuple[bool, ...]) -> int:
    return round(5 * sum(checks) / len(checks))


def _tokens(value: str) -> set[str]:
    return {
        token for token in re.findall(r"[a-z][a-z'-]{3,}", value.lower()) if token not in _STOPWORDS
    }


def _specific_terms(state: NarrativeState) -> set[str]:
    source = " ".join(
        (
            state.title,
            state.centre_knot,
            state.central_conflict,
            state.stakes,
            state.full_plot,
            state.ending,
            *(character.name for character in state.characters),
            *(character.external_objective for character in state.characters),
            *(beat.event for beat in state.beats),
        )
    )
    return _tokens(source)


def _has_specificity(value: str, terms: set[str], minimum: int = 2) -> bool:
    return len(_tokens(value) & terms) >= minimum


def _scene_text(scene: Scene) -> str:
    return " ".join(
        str(getattr(scene, field)) for field in _COMPLETION_FIELDS if field != "character_ids"
    ).lower()


def _quality_flags(scene: Scene, state: NarrativeState) -> tuple[str, ...]:
    text = _scene_text(scene)
    flags: list[str] = []
    if any(marker in text for marker in BOILERPLATE_MARKERS):
        flags.append("Generic template language is standing in for dramatic action.")
    if any(marker in text for marker in SCAFFOLD_MARKERS):
        flags.append("Architect scaffold remains; complete an author or local-model craft pass.")
    heading_and_location = f"{scene.heading} {scene.location}".lower()
    if " space" in heading_and_location or scene.location.lower().endswith("space"):
        flags.append("The location is a structural placeholder rather than a playable setting.")
    present_names = {
        character.name.lower()
        for character in state.characters
        if character.character_id in scene.character_ids
    }
    if present_names & PLACEHOLDER_CHARACTER_NAMES:
        flags.append("One or more cast names are archetypal placeholders.")
    return tuple(flags)


def _craft_cap(flags: tuple[str, ...]) -> int:
    if any("Generic template" in flag or "structural placeholder" in flag for flag in flags):
        return 2
    if any("cast names" in flag for flag in flags):
        return 2
    if any("Architect scaffold" in flag for flag in flags):
        return 3
    return 5


def _dimension(
    name: str, checks: tuple[bool, ...], evidence: str, craft_cap: int
) -> DimensionScore:
    return DimensionScore(name, min(_score(checks), craft_cap), WEIGHTS[name], evidence)


def assess_scene(scene: Scene, state: NarrativeState) -> SceneScorecard:
    terms = _specific_terms(state)
    flags = _quality_flags(scene, state)
    craft_cap = _craft_cap(flags)
    dimensions = (
        _dimension(
            "Conflict",
            (
                len(scene.objective.split()) >= 8 and _has_specificity(scene.objective, terms),
                len(scene.conflict.split()) >= 10 and _has_specificity(scene.conflict, terms, 3),
                len(scene.escalation.split()) >= 10 and _has_specificity(scene.escalation, terms),
                len(scene.turning_point.split()) >= 8
                and _has_specificity(scene.turning_point, terms),
                len(scene.outcome.split()) >= 8 and _has_specificity(scene.outcome, terms),
            ),
            "Specific objective, active resistance, escalation, visible choice "
            "and changed outcome.",
            craft_cap,
        ),
        _dimension(
            "Character development",
            (
                bool(scene.character_ids),
                bool(scene.viewpoint_character_id),
                len(scene.character_behavior.split()) >= 10
                and _has_specificity(scene.character_behavior, terms),
                len(scene.emotional_change.split()) >= 8
                and _has_specificity(scene.emotional_change, terms),
                len(scene.dialogue_text.split()) >= 8
                and len(scene.dialogue_subtext.split()) >= 8
                and _has_specificity(scene.dialogue_subtext, terms),
            ),
            "Named participants, viewpoint, behavior, emotional movement and playable subtext.",
            craft_cap,
        ),
        _dimension(
            "Plot function",
            (
                len(scene.summary.split()) >= 24 and _has_specificity(scene.summary, terms, 4),
                bool(scene.structural_beat_id),
                len(scene.setup_payoff.split()) >= 8
                and _has_specificity(scene.setup_payoff, terms),
                len(scene.outcome.split()) >= 8 and _has_specificity(scene.outcome, terms),
                _has_specificity(scene.conflict, _tokens(state.central_conflict)),
            ),
            "Story-specific beat service, causal outcome, central conflict "
            "and setup/payoff evidence.",
            craft_cap,
        ),
        _dimension(
            "Blocking & staging",
            (
                bool(scene.location) and "space" not in scene.location.lower(),
                bool(scene.time_of_day),
                len(scene.blocking.split()) >= 18 and _has_specificity(scene.blocking, terms),
                len(scene.entry_state.split()) >= 10 and _has_specificity(scene.entry_state, terms),
                len(scene.turning_point.split()) >= 8
                and _has_specificity(scene.turning_point, terms),
            ),
            "Playable location, physical objects, entry pressure and a staged visible turn.",
            craft_cap,
        ),
        _dimension(
            "Placement",
            (
                bool(scene.structural_beat_id),
                scene.ordinal > 0,
                len(scene.entry_state.split()) >= 10 and _has_specificity(scene.entry_state, terms),
                len(scene.outcome.split()) >= 8 and _has_specificity(scene.outcome, terms),
                len(scene.setup_payoff.split()) >= 8
                and _has_specificity(scene.setup_payoff, terms),
            ),
            "Structural assignment plus explicit consequences connecting "
            "the preceding and next beats.",
            craft_cap,
        ),
    )
    completion_checks = tuple(bool(getattr(scene, field)) for field in _COMPLETION_FIELDS)
    completion = round(5 * sum(completion_checks) / len(completion_checks), 2)
    weighted = sum(item.score_0_5 * item.weight for item in dimensions)
    return SceneScorecard(
        scene.scene_id,
        scene.heading,
        dimensions,
        completion,
        round(weighted, 2),
        flags,
    )


def assess_screenplay(state: NarrativeState) -> ScreenplayScorecard:
    cards = tuple(assess_scene(scene, state) for scene in state.scenes)
    completion = (
        round(sum(card.completion_score_0_5 for card in cards) / len(cards), 2) if cards else 0.0
    )
    craft = (
        round(sum(card.craft_quality_score_0_5 for card in cards) / len(cards), 2) if cards else 0.0
    )
    covered = {scene.structural_beat_id for scene in state.scenes if scene.structural_beat_id}
    coverage = round(100 * len(covered) / len(state.beats)) if state.beats else 0
    averages = {
        name: (
            sum(next(d.score_0_5 for d in card.dimensions if d.name == name) for card in cards)
            / len(cards)
            if cards
            else 0
        )
        for name in WEIGHTS
    }
    strengths = tuple(f"{name}: {value:.1f}/5" for name, value in averages.items() if value >= 4)
    priorities = [
        f"Strengthen {name.lower()} ({value:.1f}/5)."
        for name, value in averages.items()
        if value < 3
    ]
    template_count = sum(bool(card.quality_flags) for card in cards)
    if template_count:
        priorities.insert(
            0,
            f"Replace scaffold or placeholder language in {template_count} "
            "scene(s) before claiming high craft quality.",
        )
    return ScreenplayScorecard(
        cards,
        completion,
        craft,
        coverage,
        template_count,
        strengths,
        tuple(priorities),
    )


def build_complete(state: NarrativeState) -> tuple[bool, tuple[str, ...]]:
    report = assess_screenplay(state)
    blockers: list[str] = []
    if not state.scenes:
        blockers.append("Create at least one engineered scene.")
    if report.coverage_percent < 100:
        blockers.append("Every structural beat needs at least one scene.")
    incomplete = [card.scene_heading for card in report.scenes if card.completion_score_0_5 < 4.5]
    if incomplete:
        blockers.append("Complete the required scene evidence in: " + ", ".join(incomplete))
    weak = [card.scene_heading for card in report.scenes if card.craft_quality_score_0_5 < 3.0]
    if weak:
        blockers.append(
            "Replace generic construction language and bring craft evidence to at least 3.0/5 in: "
            + ", ".join(weak)
        )
    return not blockers, tuple(blockers)

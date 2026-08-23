"""Deterministic iMaSc construction-readiness scoring."""

from __future__ import annotations

from dataclasses import dataclass

from narrative_architect.knowledge.nka import NarrativeState, Scene

WEIGHTS = {
    "Conflict": 0.20,
    "Character development": 0.25,
    "Plot function": 0.30,
    "Blocking & staging": 0.15,
    "Placement": 0.10,
}


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
    weighted_score_0_5: float


@dataclass(frozen=True, slots=True)
class ScreenplayScorecard:
    scenes: tuple[SceneScorecard, ...]
    imasc_construction_score_0_5: float
    coverage_percent: int
    strengths: tuple[str, ...]
    priorities: tuple[str, ...]


def _score(checks: tuple[bool, ...]) -> int:
    return round(5 * sum(checks) / len(checks))


def assess_scene(scene: Scene, state: NarrativeState) -> SceneScorecard:
    dimensions = (
        DimensionScore(
            "Conflict",
            _score(
                (
                    bool(scene.objective),
                    bool(scene.conflict),
                    bool(scene.escalation),
                    bool(scene.turning_point),
                    bool(scene.outcome),
                )
            ),
            WEIGHTS["Conflict"],
            "Objective, resistance, escalation, turn and outcome.",
        ),
        DimensionScore(
            "Character development",
            _score(
                (
                    bool(scene.character_ids),
                    bool(scene.viewpoint_character_id),
                    bool(scene.character_behavior),
                    bool(scene.emotional_change),
                    bool(scene.dialogue_subtext),
                )
            ),
            WEIGHTS["Character development"],
            "Presence, viewpoint, behavior, change and subtext.",
        ),
        DimensionScore(
            "Plot function",
            _score(
                (
                    bool(scene.summary),
                    bool(scene.structural_beat_id),
                    bool(scene.setup_payoff),
                    bool(scene.outcome),
                    bool(state.central_conflict),
                )
            ),
            WEIGHTS["Plot function"],
            "Beat service, causality, setup/payoff and central-conflict connection.",
        ),
        DimensionScore(
            "Blocking & staging",
            _score(
                (
                    bool(scene.location),
                    bool(scene.time_of_day),
                    bool(scene.blocking),
                    bool(scene.entry_state),
                    bool(scene.turning_point),
                )
            ),
            WEIGHTS["Blocking & staging"],
            "Playable space, entry state, physical action and visible turn.",
        ),
        DimensionScore(
            "Placement",
            _score(
                (
                    bool(scene.structural_beat_id),
                    scene.ordinal > 0,
                    bool(scene.entry_state),
                    bool(scene.outcome),
                    bool(scene.setup_payoff),
                )
            ),
            WEIGHTS["Placement"],
            "Structural assignment, sequence state and connective tissue.",
        ),
    )
    weighted = sum(item.score_0_5 * item.weight for item in dimensions)
    return SceneScorecard(scene.scene_id, scene.heading, dimensions, round(weighted, 2))


def assess_screenplay(state: NarrativeState) -> ScreenplayScorecard:
    cards = tuple(assess_scene(scene, state) for scene in state.scenes)
    score = round(sum(card.weighted_score_0_5 for card in cards) / len(cards), 2) if cards else 0.0
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
    priorities = tuple(
        f"Strengthen {name.lower()} ({value:.1f}/5)."
        for name, value in averages.items()
        if value < 3
    )
    return ScreenplayScorecard(cards, score, coverage, strengths, priorities)


def build_complete(state: NarrativeState) -> tuple[bool, tuple[str, ...]]:
    report = assess_screenplay(state)
    blockers: list[str] = []
    if not state.scenes:
        blockers.append("Create at least one engineered scene.")
    if report.coverage_percent < 100:
        blockers.append("Every structural beat needs at least one scene.")
    incomplete = [card.scene_heading for card in report.scenes if card.weighted_score_0_5 < 3.0]
    if incomplete:
        blockers.append(
            "Bring every scene to at least 3.0/5 construction readiness: " + ", ".join(incomplete)
        )
    return not blockers, tuple(blockers)

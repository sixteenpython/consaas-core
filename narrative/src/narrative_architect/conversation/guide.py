"""Deterministic screenplay-development questions for the hosted alpha."""

from __future__ import annotations

from dataclasses import dataclass

from narrative_architect.application.projects import StoryProjectService
from narrative_architect.knowledge.nka import NarrativeState


@dataclass(frozen=True, slots=True)
class GuidanceStep:
    key: str
    label: str
    question: str
    why_it_matters: str


_STORY_STEPS = (
    GuidanceStep(
        "premise",
        "Premise",
        "In one or two sentences, what happens—and why is this story worth following?",
        "A premise anchors every later character and scene decision.",
    ),
    GuidanceStep(
        "protagonist",
        "Protagonist",
        "Who is the central character? Give me their name and the role they occupy in this world.",
        "The audience needs an emotional carrier for the plot.",
    ),
    GuidanceStep(
        "protagonist_objective",
        "Protagonist objective",
        "What concrete result does the protagonist pursue through the story?",
        (
            "A visible objective gives the plot direction and lets scenes create progress "
            "or resistance."
        ),
    ),
    GuidanceStep(
        "central_conflict",
        "Central conflict",
        "Who or what actively prevents the protagonist from achieving that objective?",
        "Conflict is the narrative engine, not merely difficulty in the background.",
    ),
    GuidanceStep(
        "stakes",
        "Stakes",
        "What is irreversibly lost if the protagonist fails—or succeeds in the wrong way?",
        "Stakes make the central decision consequential.",
    ),
    GuidanceStep(
        "theme",
        "Theme",
        "What human question or tension should the story explore without reducing it to a slogan?",
        "Theme helps plot and character choices accumulate meaning.",
    ),
    GuidanceStep(
        "ending",
        "Ending",
        "What decisive change or choice closes the story? It may still be provisional.",
        "Knowing the destination makes setup, escalation and payoff more coherent.",
    ),
)


def next_guidance_step(state: NarrativeState) -> GuidanceStep | None:
    values = {
        "premise": state.premise,
        "protagonist": next(
            (character.name for character in state.characters if character.role == "Protagonist"),
            "",
        ),
        "protagonist_objective": state.protagonist_objective,
        "central_conflict": state.central_conflict,
        "stakes": state.stakes,
        "theme": state.theme,
        "ending": state.ending,
    }
    for step in _STORY_STEPS:
        if not values[step.key].strip():
            return step
    scene_number = len(state.scenes) + 1
    if scene_number <= 3:
        labels = {1: "opening", 2: "escalation", 3: "decisive"}
        return GuidanceStep(
            f"scene_{scene_number}",
            f"Scene {scene_number}",
            (
                f"Describe the {labels[scene_number]} scene: where are we, what does the "
                "protagonist "
                "try to achieve, what resists them, and what changes by the end?"
            ),
            "A scene must create narrative movement, not only communicate information.",
        )
    return None


def apply_guided_answer(service: StoryProjectService, step: GuidanceStep, answer: str) -> str:
    cleaned = answer.strip()
    if not cleaned:
        raise ValueError("Please give the story a little more substance before we preserve it.")
    if step.key == "protagonist":
        service.upsert_character(character_id=None, name=cleaned, role="Protagonist")
    elif step.key.startswith("scene_"):
        number = len(service.head.state.scenes) + 1
        protagonist = next(
            (
                character.character_id
                for character in service.head.state.characters
                if character.role == "Protagonist"
            ),
            None,
        )
        service.upsert_scene(
            scene_id=None,
            heading=f"SCENE {number} - TO BE REFINED",
            summary=cleaned,
            conflict=service.head.state.central_conflict,
            character_ids=(protagonist,) if protagonist else (),
        )
    else:
        service.update_story(f"Establish {step.label.lower()}", **{step.key: cleaned})
    return (
        f"Preserved **{step.label}** in the canonical Narrative Knowledge Asset. "
        f"Revision `{service.head.revision_id[:12]}` is now the project head."
    )

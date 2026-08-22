"""Typed application service for author-approved Narrative Knowledge changes."""

from __future__ import annotations

from dataclasses import replace

from narrative_architect.knowledge.nka import (
    Character,
    InMemoryProjectRepository,
    NKARevision,
    NKAValidationError,
    Scene,
    revise_story,
)


class StoryProjectService:
    def __init__(self, repository: InMemoryProjectRepository):
        self.repository = repository

    @property
    def head(self) -> NKARevision:
        return self.repository.head

    def update_story(self, reason: str, **changes: str) -> NKARevision:
        state = revise_story(self.head.state, **changes)
        return self.repository.commit(self.head.revision_id, state, reason)

    def upsert_character(
        self,
        *,
        character_id: str | None,
        name: str,
        role: str,
        external_objective: str = "",
        internal_need: str = "",
        motivation: str = "",
        ideology: str = "",
        fear: str = "",
        arc: str = "",
    ) -> NKARevision:
        if not name.strip():
            raise NKAValidationError("character name must not be empty")
        clean_name = name.strip()
        clean_role = role.strip() or "Supporting"
        clean_external_objective = external_objective.strip()
        clean_internal_need = internal_need.strip()
        clean_motivation = motivation.strip()
        clean_ideology = ideology.strip()
        clean_fear = fear.strip()
        clean_arc = arc.strip()
        characters = list(self.head.state.characters)
        if character_id is None:
            characters.append(
                Character.create(
                    clean_name,
                    clean_role,
                    external_objective=clean_external_objective,
                    internal_need=clean_internal_need,
                    motivation=clean_motivation,
                    ideology=clean_ideology,
                    fear=clean_fear,
                    arc=clean_arc,
                )
            )
            reason = f"Add character {clean_name}"
        else:
            for index, existing in enumerate(characters):
                if existing.character_id == character_id:
                    characters[index] = replace(
                        existing,
                        name=clean_name,
                        role=clean_role,
                        external_objective=clean_external_objective,
                        internal_need=clean_internal_need,
                        motivation=clean_motivation,
                        ideology=clean_ideology,
                        fear=clean_fear,
                        arc=clean_arc,
                    )
                    reason = f"Revise character {clean_name}"
                    break
            else:
                raise NKAValidationError("unknown character")
        state = replace(self.head.state, characters=tuple(characters))
        return self.repository.commit(self.head.revision_id, state, reason)

    def upsert_scene(
        self,
        *,
        scene_id: str | None,
        heading: str,
        summary: str,
        location: str = "",
        time_of_day: str = "DAY",
        objective: str = "",
        conflict: str = "",
        outcome: str = "",
        emotional_change: str = "",
        character_ids: tuple[str, ...] = (),
    ) -> NKARevision:
        if not heading.strip() or not summary.strip():
            raise NKAValidationError("scene heading and summary are required")
        clean_heading = heading.strip()
        clean_summary = summary.strip()
        clean_location = location.strip()
        clean_time_of_day = time_of_day.strip().upper() or "DAY"
        clean_objective = objective.strip()
        clean_conflict = conflict.strip()
        clean_outcome = outcome.strip()
        clean_emotional_change = emotional_change.strip()
        scenes = list(self.head.state.scenes)
        if scene_id is None:
            scenes.append(
                Scene.create(
                    len(scenes) + 1,
                    clean_heading,
                    clean_summary,
                    location=clean_location,
                    time_of_day=clean_time_of_day,
                    objective=clean_objective,
                    conflict=clean_conflict,
                    outcome=clean_outcome,
                    emotional_change=clean_emotional_change,
                    character_ids=character_ids,
                )
            )
            reason = f"Add scene {clean_heading}"
        else:
            for index, existing in enumerate(scenes):
                if existing.scene_id == scene_id:
                    scenes[index] = replace(
                        existing,
                        heading=clean_heading,
                        summary=clean_summary,
                        location=clean_location,
                        time_of_day=clean_time_of_day,
                        objective=clean_objective,
                        conflict=clean_conflict,
                        outcome=clean_outcome,
                        emotional_change=clean_emotional_change,
                        character_ids=character_ids,
                    )
                    reason = f"Revise scene {clean_heading}"
                    break
            else:
                raise NKAValidationError("unknown scene")
        state = replace(self.head.state, scenes=tuple(scenes))
        return self.repository.commit(self.head.revision_id, state, reason)

    def restore(self, revision_id: str) -> NKARevision:
        return self.repository.undo(revision_id, self.head.revision_id)


def demo_repository() -> InMemoryProjectRepository:
    repository = InMemoryProjectRepository.create("The Last Signal")
    service = StoryProjectService(repository)
    service.update_story(
        "Establish story foundation",
        premise=(
            "A lighthouse keeper receives a radio transmission from her missing brother "
            "on the night a cyclone cuts the island off from the mainland."
        ),
        theme="Hope becomes dangerous when it prevents us from accepting the truth.",
        central_conflict=(
            "Mira must decide whether the signal is a rescue call or a trap created by the storm."
        ),
        stakes=(
            "Following the signal may kill the stranded islanders; ignoring it may abandon "
            "her brother."
        ),
        protagonist_objective="Locate the transmission source before the cyclone makes landfall.",
        ending=(
            "Mira saves the islanders and discovers the signal was her brother's final recording."
        ),
    )
    service.upsert_character(
        character_id=None,
        name="Mira Sen",
        role="Protagonist",
        external_objective="Find the source of the transmission.",
        internal_need="Accept that love cannot reverse loss.",
        motivation="She promised never to abandon her younger brother.",
        ideology="No call for help should go unanswered.",
        fear="Repeating the decision that separated them.",
        arc="From compulsive rescue to courageous acceptance.",
    )
    mira_id = service.head.state.characters[0].character_id
    service.upsert_scene(
        scene_id=None,
        heading="INT. LIGHTHOUSE RADIO ROOM - NIGHT",
        summary="Mira hears her missing brother's call sign beneath the cyclone warning.",
        location="Lighthouse radio room",
        objective="Confirm that the transmission is real.",
        conflict="The signal appears on a frequency disabled years ago.",
        outcome="She answers and receives coordinates inside the storm path.",
        emotional_change="Professional control gives way to private hope.",
        character_ids=(mira_id,),
    )
    service.upsert_scene(
        scene_id=None,
        heading="EXT. ISLAND JETTY - NIGHT",
        summary="Mira prepares the only boat while residents beg her to keep the beacon operating.",
        location="Island jetty",
        objective="Reach the coordinates before landfall.",
        conflict="Leaving will extinguish the navigation beacon protecting the evacuation ferry.",
        outcome="She discovers the signal timing repeats exactly and suspects a recording.",
        emotional_change="Hope becomes doubt and moral responsibility.",
        character_ids=(mira_id,),
    )
    service.upsert_scene(
        scene_id=None,
        heading="INT. LIGHTHOUSE LANTERN ROOM - PRE-DAWN",
        summary=(
            "Mira decodes the recording and uses its coordinates to guide the ferry around a reef."
        ),
        location="Lighthouse lantern room",
        time_of_day="PRE-DAWN",
        objective="Turn her brother's final message into a rescue route.",
        conflict="The failing generator can power either the radio or the beacon, not both.",
        outcome="She keeps the beacon alive and leads the ferry to safety.",
        emotional_change=(
            "She releases the fantasy of rescue while preserving her brother's purpose."
        ),
        character_ids=(mira_id,),
    )
    return repository

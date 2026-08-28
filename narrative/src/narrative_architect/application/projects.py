# ruff: noqa: E501
"""Typed application service for author-approved screenplay construction."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict, replace
from typing import Any

from narrative_architect.construction.blueprints import (
    CharacterOption,
    build_scene_blueprints,
    phase_completion,
    structure_beats,
)
from narrative_architect.construction.scoring import build_complete
from narrative_architect.knowledge.nka import (
    Character,
    InMemoryProjectRepository,
    NKARevision,
    NKAValidationError,
    Scene,
    StructuralBeat,
    revise_story,
)


def _invalidate_from(state: Any, phase: int) -> Any:
    return replace(state, locked_phases=tuple(p for p in state.locked_phases if p < phase))


class StoryProjectService:
    def __init__(self, repository: InMemoryProjectRepository):
        self.repository = repository

    @property
    def head(self) -> NKARevision:
        return self.repository.head

    def _commit(self, state: Any, reason: str) -> NKARevision:
        return self.repository.commit(self.head.revision_id, state, reason)

    def update_story(self, reason: str, **changes: str) -> NKARevision:
        return self._commit(revise_story(self.head.state, **changes), reason)

    def update_blueprint(
        self,
        *,
        title: str,
        centre_knot: str,
        plot_archetype: str,
        genre: str,
        tone: str,
        central_conflict: str,
    ) -> NKARevision:
        if not all(
            value.strip() for value in (centre_knot, plot_archetype, genre, central_conflict)
        ):
            raise NKAValidationError(
                "centre knot, basic plot, genre and central conflict are required"
            )
        state = revise_story(
            self.head.state,
            title=title or "Untitled Screenplay",
            centre_knot=centre_knot,
            premise=centre_knot,
            plot_archetype=plot_archetype,
            genre=genre,
            tone=tone,
            central_conflict=central_conflict,
        )
        return self._commit(_invalidate_from(state, 1), "Establish centre-knot blueprint")

    def update_plot(
        self,
        *,
        full_plot: str,
        protagonist_objective: str,
        stakes: str,
        theme: str,
        ending: str,
    ) -> NKARevision:
        if not all(value.strip() for value in (full_plot, stakes, ending)):
            raise NKAValidationError("full plot, stakes and ending are required")
        state = revise_story(
            self.head.state,
            full_plot=full_plot,
            protagonist_objective=protagonist_objective,
            stakes=stakes,
            theme=theme,
            ending=ending,
        )
        return self._commit(_invalidate_from(state, 3), "Establish full plot")

    def set_structure(
        self, *, structure_type: str, rationale: str, beat_events: Iterable[str]
    ) -> NKARevision:
        specs = structure_beats(structure_type)
        events = tuple(event.strip() for event in beat_events)
        if len(events) != len(specs) or any(not event for event in events):
            raise NKAValidationError("every structural beat requires a story event")
        beats = tuple(
            StructuralBeat.create(index, label, act, purpose, event)
            for index, ((label, act, purpose), event) in enumerate(
                zip(specs, events, strict=True), 1
            )
        )
        state = revise_story(
            self.head.state, structure_type=structure_type, structure_rationale=rationale
        )
        state = replace(
            state,
            beats=beats,
            scenes=(),
            locked_phases=tuple(p for p in state.locked_phases if p < 4),
        )
        return self._commit(state, f"Map {structure_type} structure")

    def lock_phase(self, phase: int) -> NKARevision:
        if phase < 1 or phase > 6:
            raise NKAValidationError("phase number is invalid")
        expected_previous = tuple(range(1, phase))
        if not set(expected_previous).issubset(self.head.state.locked_phases):
            raise NKAValidationError("complete and lock the preceding phase first")
        complete = phase_completion(self.head.state)[phase - 1]
        if phase == 5:
            complete, blockers = build_complete(self.head.state)
            if not complete:
                raise NKAValidationError(" ".join(blockers))
        if not complete:
            raise NKAValidationError(f"phase {phase} is not construction-ready")
        locks = tuple(range(1, phase + 1))
        return self._commit(replace(self.head.state, locked_phases=locks), f"Lock phase {phase}")

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
        contradiction: str = "",
        behavior_signature: str = "",
        voice: str = "",
        arc: str = "",
    ) -> NKARevision:
        if not name.strip():
            raise NKAValidationError("character name must not be empty")
        details: dict[str, Any] = {
            "external_objective": external_objective.strip(),
            "internal_need": internal_need.strip(),
            "motivation": motivation.strip(),
            "ideology": ideology.strip(),
            "fear": fear.strip(),
            "contradiction": contradiction.strip(),
            "behavior_signature": behavior_signature.strip(),
            "voice": voice.strip(),
            "arc": arc.strip(),
        }
        characters = list(self.head.state.characters)
        if character_id is None:
            character = Character.create(name.strip(), role.strip() or "Supporting", **details)
            characters.append(character)
            reason = f"Add character {character.name}"
        else:
            for index, existing in enumerate(characters):
                if existing.character_id == character_id:
                    characters[index] = replace(
                        existing, name=name.strip(), role=role.strip() or "Supporting", **details
                    )
                    reason = f"Revise character {name.strip()}"
                    break
            else:
                raise NKAValidationError("unknown character")
        state = _invalidate_from(replace(self.head.state, characters=tuple(characters)), 2)
        return self._commit(state, reason)

    def add_character_option(self, option: CharacterOption) -> NKARevision:
        return self.upsert_character(
            character_id=None,
            name=option.name,
            role=option.role,
            external_objective=option.external_objective,
            internal_need=option.internal_need,
            contradiction=option.contradiction,
            behavior_signature=option.behavior_signature,
            voice=option.voice,
            arc=option.arc,
        )

    def upsert_scene(
        self,
        *,
        scene_id: str | None,
        heading: str,
        summary: str,
        location: str = "",
        time_of_day: str = "DAY",
        structural_beat_id: str = "",
        viewpoint_character_id: str = "",
        entry_state: str = "",
        objective: str = "",
        conflict: str = "",
        escalation: str = "",
        turning_point: str = "",
        outcome: str = "",
        emotional_change: str = "",
        character_behavior: str = "",
        dialogue_context: str = "",
        dialogue_text: str = "",
        dialogue_subtext: str = "",
        blocking: str = "",
        setup_payoff: str = "",
        character_ids: tuple[str, ...] = (),
    ) -> NKARevision:
        if not heading.strip() or not summary.strip():
            raise NKAValidationError("scene heading and summary are required")
        details: dict[str, Any] = {
            "location": location.strip(),
            "time_of_day": time_of_day.strip().upper() or "DAY",
            "structural_beat_id": structural_beat_id,
            "viewpoint_character_id": viewpoint_character_id,
            "entry_state": entry_state.strip(),
            "objective": objective.strip(),
            "conflict": conflict.strip(),
            "escalation": escalation.strip(),
            "turning_point": turning_point.strip(),
            "outcome": outcome.strip(),
            "emotional_change": emotional_change.strip(),
            "character_behavior": character_behavior.strip(),
            "dialogue_context": dialogue_context.strip(),
            "dialogue_text": dialogue_text.strip(),
            "dialogue_subtext": dialogue_subtext.strip(),
            "blocking": blocking.strip(),
            "setup_payoff": setup_payoff.strip(),
            "character_ids": tuple(character_ids),
        }
        scenes = list(self.head.state.scenes)
        if scene_id is None:
            scene = Scene.create(len(scenes) + 1, heading.strip(), summary.strip(), **details)
            scenes.append(scene)
            reason = f"Add scene {scene.heading}"
        else:
            for index, existing in enumerate(scenes):
                if existing.scene_id == scene_id:
                    scenes[index] = replace(
                        existing, heading=heading.strip(), summary=summary.strip(), **details
                    )
                    reason = f"Revise scene {heading.strip()}"
                    break
            else:
                raise NKAValidationError("unknown scene")
        return self._commit(
            _invalidate_from(replace(self.head.state, scenes=tuple(scenes)), 5), reason
        )

    def generate_scene_plan(self) -> NKARevision:
        state = self.head.state
        if not state.beats:
            raise NKAValidationError("lock a screenplay structure before building scenes")
        scenes = [
            Scene.create(blueprint_index, **asdict(blueprint))
            for blueprint_index, blueprint in enumerate(build_scene_blueprints(state), 1)
        ]
        return self._commit(
            _invalidate_from(replace(state, scenes=tuple(scenes)), 5),
            "Generate story-grounded scene plan",
        )

    def restore(self, revision_id: str) -> NKARevision:
        return self.repository.undo(revision_id, self.head.revision_id)


def demo_repository() -> InMemoryProjectRepository:
    repository = InMemoryProjectRepository.create("The Last Signal")
    service = StoryProjectService(repository)
    service.update_blueprint(
        title="The Last Signal",
        centre_knot="During a cyclone, a lighthouse keeper receives a transmission from the brother she believes is dead and must decide whether following it will doom the islanders depending on her beacon.",
        plot_archetype="Rebirth",
        genre="Contained mystery drama",
        tone="Atmospheric, urgent and humane",
        central_conflict="Mira's need to rescue her brother conflicts with her duty to keep the evacuation beacon alive.",
    )
    service.lock_phase(1)
    service.upsert_character(
        character_id=None,
        name="Mira Sen",
        role="Protagonist",
        external_objective="Locate the transmission source before landfall.",
        internal_need="Accept that love cannot reverse loss.",
        motivation="She promised never to abandon her brother.",
        ideology="Duty is the only dependable form of love.",
        fear="Choosing the island means abandoning him again.",
        contradiction="A guardian who will endanger everyone to undo one private failure.",
        behavior_signature="Repairs machines instead of discussing grief.",
        voice="Controlled, technical, then painfully direct.",
        arc="Turns private grief into a public act of rescue.",
    )
    service.upsert_character(
        character_id=None,
        name="Dev Rao",
        role="Antagonist",
        external_objective="Keep the beacon operating for the evacuation ferry.",
        internal_need="Trust Mira with information he cannot control.",
        contradiction="Opposes Mira because he shares her duty.",
        behavior_signature="Converts fear into procedures and deadlines.",
        voice="Economical and unsentimental.",
        arc="Moves from command to collaboration.",
    )
    service.lock_phase(2)
    service.update_plot(
        full_plot=(
            "Mira hears her missing brother's call sign beneath a cyclone warning. The signal gives coordinates inside the storm path, while Dev insists the lighthouse beacon is the evacuation ferry's only guide. Mira secretly tests the transmission and discovers that it repeats with tiny changes. Her pursuit disables part of the beacon and nearly grounds the ferry. At the midpoint she realizes the voice is a recording, but the coordinates encode a safe passage through the reef. Forced to choose between radio and beacon power, she stops trying to rescue the dead, decodes his final message, and uses it to guide the living home."
        ),
        protagonist_objective="Locate and understand the transmission before the cyclone makes landfall.",
        stakes="Following the signal may kill the islanders; ignoring it may abandon her brother.",
        theme="Love becomes useful when it accepts reality and serves the living.",
        ending="Mira keeps the beacon alive and uses her brother's recorded coordinates to guide the ferry safely through the reef.",
    )
    service.lock_phase(3)
    specs = structure_beats("Three Act")
    events = (
        "Mira maintains the lighthouse and refuses to discuss her missing brother.",
        "His call sign breaks through the cyclone warning on a dead frequency.",
        "Mira answers and conceals the coordinates from Dev.",
        "Testing the signal damages the beacon as the ferry launches.",
        "Mira proves the voice is recorded but discovers coordinates embedded in it.",
        "The generator can power either the radio decoder or the navigation beacon.",
        "Mira lets the voice go, decodes the route, and relays it while keeping the beacon alive.",
        "At dawn the ferry reaches safety and Mira archives the final recording.",
    )
    if len(specs) != len(events):
        raise RuntimeError("demo beat map does not match Three Act structure")
    service.set_structure(
        structure_type="Three Act",
        rationale="The moral choice and external rescue share one clean escalation.",
        beat_events=events,
    )
    service.lock_phase(4)
    service.generate_scene_plan()
    service.lock_phase(5)
    return repository

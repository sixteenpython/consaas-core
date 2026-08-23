"""Versioned canonical Narrative Knowledge Asset for screenplay construction."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

SCHEMA_VERSION = "narrative-nka/alpha-2"
LEGACY_SCHEMA_VERSION = "narrative-nka/alpha-1"
BUNDLE_VERSION = 2


class NKAValidationError(ValueError):
    """Raised when canonical narrative state or a project bundle is invalid."""


class StaleRevisionError(RuntimeError):
    """Raised when a mutation targets a revision that is no longer the head."""


@dataclass(frozen=True, slots=True)
class Character:
    character_id: str
    name: str
    role: str = "Supporting"
    external_objective: str = ""
    internal_need: str = ""
    motivation: str = ""
    ideology: str = ""
    fear: str = ""
    contradiction: str = ""
    behavior_signature: str = ""
    voice: str = ""
    arc: str = ""

    @classmethod
    def create(cls, name: str, role: str = "Supporting", **details: str) -> Character:
        return cls(character_id=f"char-{uuid4()}", name=name.strip(), role=role, **details)


@dataclass(frozen=True, slots=True)
class StructuralBeat:
    beat_id: str
    ordinal: int
    label: str
    act: str
    purpose: str
    event: str

    @classmethod
    def create(
        cls, ordinal: int, label: str, act: str, purpose: str, event: str = ""
    ) -> StructuralBeat:
        return cls(
            f"beat-{uuid4()}", ordinal, label.strip(), act.strip(), purpose.strip(), event.strip()
        )


@dataclass(frozen=True, slots=True)
class Scene:
    scene_id: str
    ordinal: int
    heading: str
    summary: str
    location: str = ""
    time_of_day: str = "DAY"
    structural_beat_id: str = ""
    viewpoint_character_id: str = ""
    entry_state: str = ""
    objective: str = ""
    conflict: str = ""
    escalation: str = ""
    turning_point: str = ""
    outcome: str = ""
    emotional_change: str = ""
    character_behavior: str = ""
    dialogue_context: str = ""
    dialogue_text: str = ""
    dialogue_subtext: str = ""
    blocking: str = ""
    setup_payoff: str = ""
    character_ids: tuple[str, ...] = ()

    @classmethod
    def create(cls, ordinal: int, heading: str, summary: str, **details: Any) -> Scene:
        character_ids = tuple(details.pop("character_ids", ()))
        return cls(
            scene_id=f"scene-{uuid4()}",
            ordinal=ordinal,
            heading=heading.strip(),
            summary=summary.strip(),
            character_ids=character_ids,
            **details,
        )


@dataclass(frozen=True, slots=True)
class NarrativeState:
    title: str
    centre_knot: str = ""
    plot_archetype: str = ""
    genre: str = ""
    tone: str = ""
    premise: str = ""
    theme: str = ""
    central_conflict: str = ""
    stakes: str = ""
    protagonist_objective: str = ""
    ending: str = ""
    full_plot: str = ""
    structure_type: str = ""
    structure_rationale: str = ""
    locked_phases: tuple[int, ...] = ()
    beats: tuple[StructuralBeat, ...] = ()
    characters: tuple[Character, ...] = ()
    scenes: tuple[Scene, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: object) -> NarrativeState:
        if not isinstance(raw, dict):
            raise NKAValidationError("state must be an object")
        legacy_fields = {
            "title",
            "premise",
            "theme",
            "central_conflict",
            "stakes",
            "protagonist_objective",
            "ending",
            "characters",
            "scenes",
        }
        current_fields = set(cls.__dataclass_fields__)
        if set(raw) not in (legacy_fields, current_fields):
            raise NKAValidationError("state contract does not match a supported schema")
        legacy = set(raw) == legacy_fields
        try:
            characters = tuple(_character_from_dict(item, legacy) for item in raw["characters"])
            scenes = tuple(_scene_from_dict(item, legacy) for item in raw["scenes"])
            state = cls(
                title=str(raw["title"]),
                centre_knot=str(raw["premise"] if legacy else raw["centre_knot"]),
                plot_archetype="" if legacy else str(raw["plot_archetype"]),
                genre="" if legacy else str(raw["genre"]),
                tone="" if legacy else str(raw["tone"]),
                premise=str(raw["premise"]),
                theme=str(raw["theme"]),
                central_conflict=str(raw["central_conflict"]),
                stakes=str(raw["stakes"]),
                protagonist_objective=str(raw["protagonist_objective"]),
                ending=str(raw["ending"]),
                full_plot="" if legacy else str(raw["full_plot"]),
                structure_type="" if legacy else str(raw["structure_type"]),
                structure_rationale="" if legacy else str(raw["structure_rationale"]),
                locked_phases=() if legacy else tuple(raw["locked_phases"]),
                beats=() if legacy else tuple(StructuralBeat(**item) for item in raw["beats"]),
                characters=characters,
                scenes=scenes,
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise NKAValidationError("state contains invalid entities") from exc
        validate_state(state)
        return state


def _character_from_dict(item: dict[str, Any], legacy: bool) -> Character:
    raw = dict(item)
    if legacy:
        raw.update(contradiction="", behavior_signature="", voice="")
    return Character(**raw)


def _scene_from_dict(item: dict[str, Any], legacy: bool) -> Scene:
    raw = {**item, "character_ids": tuple(item.get("character_ids", ()))}
    if legacy:
        for field in (
            "structural_beat_id",
            "viewpoint_character_id",
            "entry_state",
            "escalation",
            "turning_point",
            "character_behavior",
            "dialogue_context",
            "dialogue_text",
            "dialogue_subtext",
            "blocking",
            "setup_payoff",
        ):
            raw[field] = ""
    return Scene(**raw)


@dataclass(frozen=True, slots=True)
class NKARevision:
    revision_id: str
    parent_revision_id: str | None
    reason: str
    created_at: str
    state: NarrativeState

    def to_dict(self) -> dict[str, Any]:
        return {
            "revision_id": self.revision_id,
            "parent_revision_id": self.parent_revision_id,
            "reason": self.reason,
            "created_at": self.created_at,
            "state": self.state.to_dict(),
        }


def validate_state(state: NarrativeState) -> None:
    if not state.title.strip():
        raise NKAValidationError("title must not be empty")
    if tuple(sorted(set(state.locked_phases))) != state.locked_phases:
        raise NKAValidationError("locked phases must be unique and ordered")
    if state.locked_phases and state.locked_phases != tuple(range(1, max(state.locked_phases) + 1)):
        raise NKAValidationError("locked phases must form a completed prefix")
    if any(phase < 1 or phase > 6 for phase in state.locked_phases):
        raise NKAValidationError("phase number is invalid")
    character_ids = [character.character_id for character in state.characters]
    if len(character_ids) != len(set(character_ids)):
        raise NKAValidationError("character identifiers must be unique")
    if any(not character.name.strip() for character in state.characters):
        raise NKAValidationError("character names must not be empty")
    beat_ids = [beat.beat_id for beat in state.beats]
    if len(beat_ids) != len(set(beat_ids)):
        raise NKAValidationError("structural beat identifiers must be unique")
    if [beat.ordinal for beat in state.beats] != list(range(1, len(state.beats) + 1)):
        raise NKAValidationError("structural beats must form one ordered sequence")
    if any(not beat.label.strip() or not beat.purpose.strip() for beat in state.beats):
        raise NKAValidationError("every structural beat needs a label and purpose")
    scene_ids = [scene.scene_id for scene in state.scenes]
    if len(scene_ids) != len(set(scene_ids)):
        raise NKAValidationError("scene identifiers must be unique")
    if [scene.ordinal for scene in state.scenes] != list(range(1, len(state.scenes) + 1)):
        raise NKAValidationError("scene ordinals must form one ordered sequence")
    known_characters, known_beats = set(character_ids), set(beat_ids)
    for scene in state.scenes:
        if not scene.heading.strip() or not scene.summary.strip():
            raise NKAValidationError("every scene requires a heading and summary")
        if not set(scene.character_ids).issubset(known_characters):
            raise NKAValidationError("scene character references must resolve")
        if scene.viewpoint_character_id and scene.viewpoint_character_id not in known_characters:
            raise NKAValidationError("scene viewpoint character must resolve")
        if scene.structural_beat_id and scene.structural_beat_id not in known_beats:
            raise NKAValidationError("scene structural beat must resolve")


def _revision_id(parent: str | None, reason: str, state: NarrativeState) -> str:
    return _revision_id_for_payload(parent, reason, state.to_dict())


def _revision_id_for_payload(parent: str | None, reason: str, state: dict[str, Any]) -> str:
    canonical = json.dumps(
        {"parent": parent, "reason": reason, "state": state},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"rev-{hashlib.sha256(canonical).hexdigest()[:24]}"


class InMemoryProjectRepository:
    """One-project immutable revision repository used by the UI and tests."""

    def __init__(self, project_id: str, revisions: list[NKARevision], head_revision_id: str):
        self.project_id = project_id
        self._revisions = {revision.revision_id: revision for revision in revisions}
        self._order = [revision.revision_id for revision in revisions]
        self.head_revision_id = head_revision_id
        self._validate_graph()

    @classmethod
    def create(cls, title: str = "Untitled Screenplay") -> InMemoryProjectRepository:
        state = NarrativeState(title=title.strip() or "Untitled Screenplay")
        revision = _new_revision(None, "Create project", state)
        return cls(f"project-{uuid4()}", [revision], revision.revision_id)

    @property
    def head(self) -> NKARevision:
        return self._revisions[self.head_revision_id]

    @property
    def history(self) -> tuple[NKARevision, ...]:
        return tuple(self._revisions[revision_id] for revision_id in self._order)

    def get(self, revision_id: str) -> NKARevision:
        try:
            return self._revisions[revision_id]
        except KeyError as exc:
            raise NKAValidationError("unknown revision") from exc

    def commit(self, expected_revision_id: str, state: NarrativeState, reason: str) -> NKARevision:
        if expected_revision_id != self.head_revision_id:
            raise StaleRevisionError("project head changed; reload before applying this edit")
        validate_state(state)
        if state == self.head.state:
            return self.head
        revision = _new_revision(self.head_revision_id, reason.strip() or "Revise story", state)
        self._revisions[revision.revision_id] = revision
        self._order.append(revision.revision_id)
        self.head_revision_id = revision.revision_id
        return revision

    def undo(self, target_revision_id: str, expected_revision_id: str) -> NKARevision:
        return self.commit(
            expected_revision_id,
            self.get(target_revision_id).state,
            f"Restore {target_revision_id}",
        )

    def export_json(self) -> str:
        return json.dumps(
            {
                "bundle_version": BUNDLE_VERSION,
                "schema_version": SCHEMA_VERSION,
                "project_id": self.project_id,
                "head_revision_id": self.head_revision_id,
                "revisions": [revision.to_dict() for revision in self.history],
            },
            ensure_ascii=False,
            indent=2,
        )

    @classmethod
    def import_json(cls, text: str) -> InMemoryProjectRepository:
        try:
            raw = json.loads(text)
        except json.JSONDecodeError as exc:
            raise NKAValidationError("project file is not valid JSON") from exc
        fields = {"bundle_version", "schema_version", "project_id", "head_revision_id", "revisions"}
        if not isinstance(raw, dict) or set(raw) != fields:
            raise NKAValidationError("project bundle contract is invalid")
        if not isinstance(raw["project_id"], str) or not raw["project_id"].startswith("project-"):
            raise NKAValidationError("project identifier is invalid")
        if not isinstance(raw["revisions"], list) or not raw["revisions"]:
            raise NKAValidationError("project must contain revisions")
        if raw["bundle_version"] == 1 and raw["schema_version"] == LEGACY_SCHEMA_VERSION:
            return cls._import_legacy(raw)
        if raw["bundle_version"] != BUNDLE_VERSION or raw["schema_version"] != SCHEMA_VERSION:
            raise NKAValidationError("project bundle version is not supported")
        return cls(
            raw["project_id"],
            [_parse_revision(item) for item in raw["revisions"]],
            raw["head_revision_id"],
        )

    @classmethod
    def _import_legacy(cls, raw: dict[str, Any]) -> InMemoryProjectRepository:
        migrated: list[NKARevision] = []
        id_map: dict[str, str] = {}
        for item in raw["revisions"]:
            _validate_revision_contract(item)
            old_parent = item["parent_revision_id"]
            expected_old = _revision_id_for_payload(old_parent, item["reason"], item["state"])
            if item["revision_id"] != expected_old:
                raise NKAValidationError("legacy revision content hash does not match")
            state = NarrativeState.from_dict(item["state"])
            parent = id_map.get(old_parent) if old_parent else None
            revision_id = _revision_id(parent, item["reason"], state)
            migrated.append(
                NKARevision(revision_id, parent, item["reason"], item["created_at"], state)
            )
            id_map[item["revision_id"]] = revision_id
        if raw["head_revision_id"] not in id_map:
            raise NKAValidationError("legacy project head does not resolve")
        return cls(raw["project_id"], migrated, id_map[raw["head_revision_id"]])

    def _validate_graph(self) -> None:
        if self.head_revision_id not in self._revisions:
            raise NKAValidationError("project head does not resolve")
        seen: set[str] = set()
        for revision_id in self._order:
            revision = self._revisions[revision_id]
            if revision.parent_revision_id is not None and revision.parent_revision_id not in seen:
                raise NKAValidationError("revision parent must precede its child")
            if (
                _revision_id(revision.parent_revision_id, revision.reason, revision.state)
                != revision_id
            ):
                raise NKAValidationError("revision content hash does not match")
            seen.add(revision_id)


def _validate_revision_contract(item: object) -> None:
    fields = {"revision_id", "parent_revision_id", "reason", "created_at", "state"}
    if not isinstance(item, dict) or set(item) != fields:
        raise NKAValidationError("revision contract is invalid")
    if not all(isinstance(item[key], str) for key in ("revision_id", "reason", "created_at")):
        raise NKAValidationError("revision metadata is invalid")


def _parse_revision(item: object) -> NKARevision:
    _validate_revision_contract(item)
    if not isinstance(item, dict):
        raise NKAValidationError("revision contract is invalid")
    state = NarrativeState.from_dict(item["state"])
    expected = _revision_id(item["parent_revision_id"], item["reason"], state)
    if item["revision_id"] != expected:
        raise NKAValidationError("revision content hash does not match")
    return NKARevision(
        item["revision_id"], item["parent_revision_id"], item["reason"], item["created_at"], state
    )


def _new_revision(parent: str | None, reason: str, state: NarrativeState) -> NKARevision:
    return NKARevision(
        _revision_id(parent, reason, state), parent, reason, datetime.now(UTC).isoformat(), state
    )


def revise_story(state: NarrativeState, **changes: str) -> NarrativeState:
    allowed = {
        "title",
        "centre_knot",
        "plot_archetype",
        "genre",
        "tone",
        "premise",
        "theme",
        "central_conflict",
        "stakes",
        "protagonist_objective",
        "ending",
        "full_plot",
        "structure_type",
        "structure_rationale",
    }
    if not set(changes).issubset(allowed):
        raise NKAValidationError("unsupported story field")
    return replace(state, **{key: value.strip() for key, value in changes.items()})

"""Versioned canonical Narrative Knowledge Asset for the Foundation Alpha."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

SCHEMA_VERSION = "narrative-nka/alpha-1"
BUNDLE_VERSION = 1


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
    arc: str = ""

    @classmethod
    def create(cls, name: str, role: str = "Supporting", **details: str) -> Character:
        return cls(character_id=f"char-{uuid4()}", name=name.strip(), role=role, **details)


@dataclass(frozen=True, slots=True)
class Scene:
    scene_id: str
    ordinal: int
    heading: str
    summary: str
    location: str = ""
    time_of_day: str = "DAY"
    objective: str = ""
    conflict: str = ""
    outcome: str = ""
    emotional_change: str = ""
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
    premise: str = ""
    theme: str = ""
    central_conflict: str = ""
    stakes: str = ""
    protagonist_objective: str = ""
    ending: str = ""
    characters: tuple[Character, ...] = ()
    scenes: tuple[Scene, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: object) -> NarrativeState:
        if not isinstance(raw, dict):
            raise NKAValidationError("state must be an object")
        required = {
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
        if set(raw) != required:
            raise NKAValidationError("state contract does not match the supported schema")
        try:
            characters = tuple(Character(**item) for item in raw["characters"])
            scenes = tuple(
                Scene(**{**item, "character_ids": tuple(item.get("character_ids", ()))})
                for item in raw["scenes"]
            )
            state = cls(
                title=str(raw["title"]),
                premise=str(raw["premise"]),
                theme=str(raw["theme"]),
                central_conflict=str(raw["central_conflict"]),
                stakes=str(raw["stakes"]),
                protagonist_objective=str(raw["protagonist_objective"]),
                ending=str(raw["ending"]),
                characters=characters,
                scenes=scenes,
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise NKAValidationError("state contains invalid entities") from exc
        validate_state(state)
        return state


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
    character_ids = [character.character_id for character in state.characters]
    if len(character_ids) != len(set(character_ids)):
        raise NKAValidationError("character identifiers must be unique")
    if any(not character.name.strip() for character in state.characters):
        raise NKAValidationError("character names must not be empty")
    scene_ids = [scene.scene_id for scene in state.scenes]
    if len(scene_ids) != len(set(scene_ids)):
        raise NKAValidationError("scene identifiers must be unique")
    if [scene.ordinal for scene in state.scenes] != list(range(1, len(state.scenes) + 1)):
        raise NKAValidationError("scene ordinals must form one ordered sequence")
    known_characters = set(character_ids)
    for scene in state.scenes:
        if not scene.heading.strip() or not scene.summary.strip():
            raise NKAValidationError("every scene requires a heading and summary")
        if not set(scene.character_ids).issubset(known_characters):
            raise NKAValidationError("scene character references must resolve")


def _revision_id(parent_revision_id: str | None, reason: str, state: NarrativeState) -> str:
    canonical = json.dumps(
        {"parent": parent_revision_id, "reason": reason, "state": state.to_dict()},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"rev-{hashlib.sha256(canonical).hexdigest()[:24]}"


class InMemoryProjectRepository:
    """One-project immutable revision repository used by the alpha UI and tests."""

    def __init__(self, project_id: str, revisions: list[NKARevision], head_revision_id: str):
        self.project_id = project_id
        self._revisions = {revision.revision_id: revision for revision in revisions}
        self._order = [revision.revision_id for revision in revisions]
        self.head_revision_id = head_revision_id
        self._validate_graph()

    @classmethod
    def create(cls, title: str = "Untitled Story") -> InMemoryProjectRepository:
        state = NarrativeState(title=title.strip() or "Untitled Story")
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
        target = self.get(target_revision_id)
        return self.commit(
            expected_revision_id,
            target.state,
            f"Restore {target_revision_id}",
        )

    def export_json(self) -> str:
        payload = {
            "bundle_version": BUNDLE_VERSION,
            "schema_version": SCHEMA_VERSION,
            "project_id": self.project_id,
            "head_revision_id": self.head_revision_id,
            "revisions": [revision.to_dict() for revision in self.history],
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)

    @classmethod
    def import_json(cls, text: str) -> InMemoryProjectRepository:
        try:
            raw = json.loads(text)
        except json.JSONDecodeError as exc:
            raise NKAValidationError("project file is not valid JSON") from exc
        required = {
            "bundle_version",
            "schema_version",
            "project_id",
            "head_revision_id",
            "revisions",
        }
        if not isinstance(raw, dict) or set(raw) != required:
            raise NKAValidationError("project bundle contract is invalid")
        if raw["bundle_version"] != BUNDLE_VERSION or raw["schema_version"] != SCHEMA_VERSION:
            raise NKAValidationError("project bundle version is not supported")
        if not isinstance(raw["project_id"], str) or not raw["project_id"].startswith("project-"):
            raise NKAValidationError("project identifier is invalid")
        if not isinstance(raw["revisions"], list) or not raw["revisions"]:
            raise NKAValidationError("project must contain revisions")
        revisions: list[NKARevision] = []
        for item in raw["revisions"]:
            if not isinstance(item, dict) or set(item) != {
                "revision_id",
                "parent_revision_id",
                "reason",
                "created_at",
                "state",
            }:
                raise NKAValidationError("revision contract is invalid")
            state = NarrativeState.from_dict(item["state"])
            expected_id = _revision_id(item["parent_revision_id"], item["reason"], state)
            if item["revision_id"] != expected_id:
                raise NKAValidationError("revision content hash does not match")
            revisions.append(
                NKARevision(
                    revision_id=item["revision_id"],
                    parent_revision_id=item["parent_revision_id"],
                    reason=item["reason"],
                    created_at=item["created_at"],
                    state=state,
                )
            )
        return cls(raw["project_id"], revisions, raw["head_revision_id"])

    def _validate_graph(self) -> None:
        if self.head_revision_id not in self._revisions:
            raise NKAValidationError("project head does not resolve")
        seen: set[str] = set()
        for revision_id in self._order:
            revision = self._revisions[revision_id]
            if revision.parent_revision_id is not None and revision.parent_revision_id not in seen:
                raise NKAValidationError("revision parent must precede its child")
            expected = _revision_id(revision.parent_revision_id, revision.reason, revision.state)
            if expected != revision.revision_id:
                raise NKAValidationError("revision content hash does not match")
            seen.add(revision_id)


def _new_revision(
    parent_revision_id: str | None, reason: str, state: NarrativeState
) -> NKARevision:
    return NKARevision(
        revision_id=_revision_id(parent_revision_id, reason, state),
        parent_revision_id=parent_revision_id,
        reason=reason,
        created_at=datetime.now(UTC).isoformat(),
        state=state,
    )


def revise_story(state: NarrativeState, **changes: str) -> NarrativeState:
    allowed = {
        "title",
        "premise",
        "theme",
        "central_conflict",
        "stakes",
        "protagonist_objective",
        "ending",
    }
    if not set(changes).issubset(allowed):
        raise NKAValidationError("unsupported story field")
    clean = {key: value.strip() for key, value in changes.items()}
    return replace(
        state,
        title=clean.get("title", state.title),
        premise=clean.get("premise", state.premise),
        theme=clean.get("theme", state.theme),
        central_conflict=clean.get("central_conflict", state.central_conflict),
        stakes=clean.get("stakes", state.stakes),
        protagonist_objective=clean.get("protagonist_objective", state.protagonist_objective),
        ending=clean.get("ending", state.ending),
    )

# ruff: noqa: E501
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest
from narrative_architect.application.projects import StoryProjectService, demo_repository
from narrative_architect.construction.blueprints import (
    BOOKER_PLOTS,
    recommend_structure,
    structure_beats,
    suggest_centre_knots,
    suggest_characters,
)
from narrative_architect.construction.scoring import (
    BOILERPLATE_MARKERS,
    assess_scene,
    assess_screenplay,
    build_complete,
)
from narrative_architect.create.compiler import compile_scorecard_markdown
from narrative_architect.inference import LocalModelError, OllamaLocalModel
from narrative_architect.knowledge.nka import InMemoryProjectRepository, NKAValidationError


def test_suggestions_are_bounded_proposals() -> None:
    options = suggest_centre_knots("a shy wedding photographer", "Comedy")

    assert len(options) == 3
    assert options[0].archetype in BOOKER_PLOTS
    assert "wedding photographer" in options[0].centre_knot


def test_phases_must_lock_in_order() -> None:
    service = StoryProjectService(InMemoryProjectRepository.create())

    with pytest.raises(NKAValidationError, match="preceding phase"):
        service.lock_phase(2)

    service.update_blueprint(
        title="Mistaken Expert",
        centre_knot="A timid clerk is mistaken for a crisis negotiator and must keep the lie alive to save a hostage who recognizes him.",
        plot_archetype="Comedy",
        genre="Comedy",
        tone="Escalating and humane",
        central_conflict="Telling the truth may destroy the only trust keeping the hostage alive.",
    )
    service.lock_phase(1)
    assert service.head.state.locked_phases == (1,)


def test_demo_is_a_complete_scene_construction_blueprint() -> None:
    repository = demo_repository()
    state = repository.head.state
    scorecard = assess_screenplay(state)
    complete, blockers = build_complete(state)

    assert state.locked_phases == (1, 2, 3, 4, 5)
    assert len(state.beats) == len(state.scenes) == 8
    assert scorecard.coverage_percent == 100
    assert scorecard.completion_coverage_score_0_5 == 5.0
    assert scorecard.craft_quality_score_0_5 == 3.0
    assert scorecard.template_scene_count == 8
    assert complete and not blockers


def test_scorecard_is_source_bound_and_does_not_claim_success_prediction() -> None:
    repository = demo_repository()
    report = compile_scorecard_markdown(repository.head)

    assert repository.head_revision_id in report
    assert "Completion coverage" in report
    assert "Craft quality" in report
    assert "Craft-evidence flags" in report
    assert "not an IMDb score" in report
    assert "not a prediction" in report


def test_story_grounded_scene_plan_uses_canonical_people_places_and_causality() -> None:
    state = demo_repository().head.state
    opening = state.scenes[0]

    assert opening.heading == "INT. LIGHTHOUSE LANTERN ROOM - DAY"
    assert "Mira Sen" in opening.summary
    assert "Dev Rao" in opening.summary
    assert "beacon switch" in opening.summary
    assert "call sign" in opening.summary
    assert "call sign" in opening.turning_point
    assert "locate the transmission source" in opening.turning_point
    assert not any(marker in opening.summary.lower() for marker in BOILERPLATE_MARKERS)


def test_populated_boilerplate_has_full_completion_but_low_craft_and_blocks_build() -> None:
    repository = demo_repository()
    state = repository.head.state
    opening = replace(
        state.scenes[0],
        heading="INT. OPENING STATE SPACE - DAY",
        location="Opening State space",
        escalation="The first tactic fails and forces a more revealing, costly action.",
        turning_point="A choice changes the meaning or direction of opening state.",
        outcome="The event is completed and causally launches the next structural movement.",
        character_behavior="The character demonstrates the arc through a visible choice under pressure.",
        dialogue_text="A short tactical exchange turns when behavior reveals what the words conceal.",
        blocking="Movement through the location externalizes control, resistance and the turn.",
    )
    degraded = replace(state, scenes=(opening, *state.scenes[1:]))
    card = assess_scene(opening, degraded)
    complete, blockers = build_complete(degraded)

    assert card.completion_score_0_5 == 5.0
    assert card.craft_quality_score_0_5 <= 2.0
    assert any("Generic template" in flag for flag in card.quality_flags)
    assert not complete
    assert any(opening.heading in blocker for blocker in blockers)


def test_structure_and_character_intelligence_reads_canonical_state() -> None:
    state = demo_repository().head.state

    structure, rationale = recommend_structure(state)
    cast = suggest_characters(state)

    assert structure in {
        "Three Act",
        "Non-linear",
        "Freytag's Pyramid",
        "Seven Point Story",
        "Save the Cat",
    }
    assert rationale
    assert len(structure_beats(structure)) >= 6
    assert {item.role for item in cast} >= {"Protagonist", "Antagonist"}


def test_ollama_adapter_rejects_non_loopback_endpoints() -> None:
    with pytest.raises(LocalModelError, match="loopback-only"):
        OllamaLocalModel(base_url="https://example.com")


def test_required_skill_library_is_versioned_with_the_app() -> None:
    skills = Path("narrative/skills")
    required = {
        "plot_builder.md",
        "character_sketch.md",
        "character_builder.md",
        "screenplay_structure.md",
        "scene_builder.md",
        "scene_assessor.md",
        "dialogue_context_text_subtext.md",
    }

    assert required.issubset({path.name for path in skills.glob("*.md")})


def test_foundation_alpha_bundle_migrates_to_builder_schema() -> None:
    legacy_state = {
        "title": "Legacy Story",
        "premise": "A courier must deliver a letter that implicates her family.",
        "theme": "Truth costs belonging.",
        "central_conflict": "Delivery protects the city but destroys her family.",
        "stakes": "The city falls if the evidence disappears.",
        "protagonist_objective": "Deliver the letter.",
        "ending": "She delivers it and accepts exile.",
        "characters": [],
        "scenes": [],
    }
    reason = "Create project"
    canonical = json.dumps(
        {"parent": None, "reason": reason, "state": legacy_state},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    revision_id = f"rev-{hashlib.sha256(canonical).hexdigest()[:24]}"
    bundle = json.dumps(
        {
            "bundle_version": 1,
            "schema_version": "narrative-nka/alpha-1",
            "project_id": "project-legacy",
            "head_revision_id": revision_id,
            "revisions": [
                {
                    "revision_id": revision_id,
                    "parent_revision_id": None,
                    "reason": reason,
                    "created_at": "2026-08-22T00:00:00+00:00",
                    "state": legacy_state,
                }
            ],
        }
    )

    migrated = InMemoryProjectRepository.import_json(bundle)

    assert migrated.head.state.centre_knot == legacy_state["premise"]
    assert migrated.head.state.premise == legacy_state["premise"]
    assert json.loads(migrated.export_json())["schema_version"] == "narrative-nka/alpha-2"

# ruff: noqa: E501
"""Narrative Architect screenplay construction studio."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, cast

import streamlit as st

from narrative_architect.application.projects import StoryProjectService, demo_repository
from narrative_architect.construction.blueprints import (
    BOOKER_PLOTS,
    STRUCTURES,
    draft_full_plot,
    phase_completion,
    recommend_structure,
    structure_beats,
    suggest_centre_knots,
    suggest_characters,
)
from narrative_architect.construction.scoring import assess_screenplay, build_complete
from narrative_architect.create.compiler import (
    assess_readiness,
    compile_bounded_fountain,
    compile_scorecard_markdown,
)
from narrative_architect.inference import LocalModelError, OllamaLocalModel
from narrative_architect.knowledge.nka import InMemoryProjectRepository, NKAValidationError

APP_VERSION = "0.3.0"
PHASES = (
    "Centre Knot",
    "Characters",
    "Full Plot",
    "Structure",
    "Scene Construction",
    "Build & Score",
)


def _set_repository(repository: InMemoryProjectRepository) -> None:
    st.session_state.repository = repository
    for key in tuple(st.session_state):
        if key.startswith("draft_") or key.startswith("suggest_"):
            del st.session_state[key]


def _repository() -> InMemoryProjectRepository:
    if "repository" not in st.session_state:
        _set_repository(InMemoryProjectRepository.create())
    return cast(InMemoryProjectRepository, st.session_state.repository)


def _service() -> StoryProjectService:
    return StoryProjectService(_repository())


def _flash(message: str) -> None:
    st.session_state.flash_success = message


def _consume_flash() -> None:
    if message := st.session_state.pop("flash_success", None):
        st.success(message)


def _profile() -> str:
    return os.getenv("NARRATIVE_PROFILE", "hosted_demo")


def _local_model() -> OllamaLocalModel | None:
    if _profile() != "local_private" or os.getenv("NARRATIVE_ENABLE_OLLAMA") != "1":
        return None
    try:
        return OllamaLocalModel(
            model=os.getenv("NARRATIVE_OLLAMA_MODEL", "qwen2.5:7b-instruct"),
            base_url=os.getenv("NARRATIVE_OLLAMA_URL", "http://127.0.0.1:11434"),
        )
    except LocalModelError:
        return None


def _skill_text(name: str) -> str:
    path = Path(__file__).resolve().parents[3] / "skills" / name
    return path.read_text(encoding="utf-8")


def _skill_generate(skill: str, fallback: str, request: str) -> tuple[str, str]:
    model = _local_model()
    if model and model.available():
        context = json.dumps(_repository().head.state.to_dict(), ensure_ascii=False, indent=2)
        try:
            return model.generate(
                skill_markdown=_skill_text(skill), context=context, request=request
            ), f"Local model · {model.model} · {skill}"
        except (LocalModelError, OSError):
            pass
    return fallback, f"Deterministic skill blueprint · {skill}"


def _render_header() -> None:
    st.markdown(
        """
        <div class="na-hero">
          <div class="na-kicker">SCREENPLAY CONSTRUCTION STUDIO</div>
          <h1>Narrative Architect</h1>
          <p>Build a stronger first draft—centre knot to scene sequence—one approved layer at a time.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(
        f"Builder v{APP_VERSION} · Skill-library intelligence · Immutable story blueprint · Local-model ready"
    )


def _render_sidebar() -> None:
    repository = _repository()
    state = repository.head.state
    completion = phase_completion(state)
    with st.sidebar:
        st.markdown("### Construction blueprint")
        st.markdown(f"**{state.title}**")
        st.caption(f"Project `{repository.project_id[-8:]}` · {len(repository.history)} revisions")
        for index, name in enumerate(PHASES, 1):
            if index in state.locked_phases:
                icon, label = "✓", "Locked"
            elif completion[index - 1]:
                icon, label = "◐", "Ready to lock"
            elif index == max(state.locked_phases, default=0) + 1:
                icon, label = "●", "Building"
            else:
                icon, label = "○", "Waiting"
            st.markdown(
                f"<div class='phase-row'><b>{icon} {index}. {name}</b><span>{label}</span></div>",
                unsafe_allow_html=True,
            )
        st.progress(
            len(state.locked_phases) / 6, text=f"{len(state.locked_phases)}/6 phases locked"
        )

        col1, col2 = st.columns(2)
        if col1.button("New", width="stretch"):
            _set_repository(InMemoryProjectRepository.create())
            st.rerun()
        if col2.button("Load demo", width="stretch"):
            _set_repository(demo_repository())
            _flash("Loaded a fully engineered demonstration screenplay.")
            st.rerun()
        st.download_button(
            "Download construction project",
            repository.export_json(),
            file_name=f"{_safe_name(state.title)}-project.json",
            mime="application/json",
            width="stretch",
        )
        uploaded = st.file_uploader("Reload project JSON", type=["json"])
        if uploaded is not None and st.button("Import project", width="stretch"):
            if uploaded.size > 5_000_000:
                st.error("Project bundles are limited to 5 MB.")
            else:
                try:
                    imported = InMemoryProjectRepository.import_json(
                        uploaded.getvalue().decode("utf-8")
                    )
                except (UnicodeDecodeError, NKAValidationError) as exc:
                    st.error(str(exc))
                else:
                    _set_repository(imported)
                    _flash("Project and immutable revision history restored.")
                    st.rerun()
        if len(repository.history) > 1:
            with st.expander("Revision history"):
                options = list(reversed(repository.history[:-1]))
                selected = st.selectbox(
                    "Restore earlier blueprint",
                    options,
                    format_func=lambda revision: f"{revision.revision_id[:10]} · {revision.reason}",
                )
                if st.button("Restore as new revision", width="stretch"):
                    _service().restore(selected.revision_id)
                    _flash("Earlier blueprint restored without rewriting history.")
                    st.rerun()
        st.divider()
        model = _local_model()
        if model and model.available():
            st.success(f"Local creative model ready · {model.model}")
        elif _profile() == "local_private":
            st.info("Skill engine ready · enable a local Ollama model for generative drafting")
        else:
            st.warning("Hosted construction demo")
            st.caption(
                "Do not enter confidential or unpublished screenplay material. Hosted sessions are temporary."
            )
        st.caption("No screenplay content is sent to an external inference service.")


def _phase_guard(phase: int) -> bool:
    state = _repository().head.state
    missing = [index for index in range(1, phase) if index not in state.locked_phases]
    if missing:
        st.info(f"Complete and lock Phase {missing[0]} before constructing this layer.")
        return False
    return True


def _lock(phase: int, message: str) -> None:
    try:
        _service().lock_phase(phase)
    except NKAValidationError as exc:
        st.error(str(exc))
    else:
        _flash(message)
        st.rerun()


def _render_phase_one() -> None:
    state = _repository().head.state
    st.subheader("Phase 1 · Fix the centre knot")
    st.write("The centre knot is the one-line dramatic problem every later choice must serve.")
    with st.expander(
        "I am unsure—suggest a few one-line plots", expanded=not bool(state.centre_knot)
    ):
        seed = st.text_input(
            "A person, world, image or problem you want to explore", key="suggest_seed"
        )
        suggestion_genre = st.text_input(
            "Preferred genre", value=state.genre or "Comedy", key="suggest_genre"
        )
        for index, option in enumerate(suggest_centre_knots(seed, suggestion_genre)):
            st.markdown(f"**{option.title} · {option.archetype}**")
            st.write(option.centre_knot)
            st.caption(option.dramatic_engine)
            if st.button("Use this blueprint", key=f"use-knot-{index}"):
                st.session_state.draft_blueprint = option
                st.rerun()
    draft = st.session_state.get("draft_blueprint")
    with st.form("centre-knot-form"):
        title = st.text_input("Working title", state.title)
        centre_knot = st.text_area(
            "One-line centre knot", draft.centre_knot if draft else state.centre_knot, height=100
        )
        col1, col2, col3 = st.columns(3)
        default_archetype = draft.archetype if draft else state.plot_archetype
        archetype = col1.selectbox(
            "Booker basic plot",
            BOOKER_PLOTS,
            index=BOOKER_PLOTS.index(default_archetype) if default_archetype in BOOKER_PLOTS else 4,
        )
        genre = col2.text_input("Genre", draft.genre if draft else state.genre or "Comedy")
        tone = col3.text_input("Tone", state.tone or "Warm and escalating")
        central_conflict = st.text_area(
            "Central conflict",
            state.central_conflict,
            placeholder="Who wants what, and what force makes that want costly?",
        )
        submitted = st.form_submit_button("Lock centre-knot blueprint", type="primary")
    if submitted:
        try:
            _service().update_blueprint(
                title=title,
                centre_knot=centre_knot,
                plot_archetype=archetype,
                genre=genre,
                tone=tone,
                central_conflict=central_conflict,
            )
            _service().lock_phase(1)
        except NKAValidationError as exc:
            st.error(str(exc))
        else:
            _flash("Blueprint fixed. Phase 2 is ready for its cast.")
            st.rerun()


def _character_form(defaults: Any = None) -> None:
    with st.form(f"character-form-{defaults.character_id if defaults else 'new'}"):
        col1, col2 = st.columns([2, 1])
        name = col1.text_input("Name", defaults.name if defaults else "")
        roles = ["Protagonist", "Antagonist", "Supporting", "Minor"]
        role = col2.selectbox(
            "Role",
            roles,
            index=roles.index(defaults.role) if defaults and defaults.role in roles else 2,
        )
        external = st.text_area(
            "External objective", defaults.external_objective if defaults else ""
        )
        internal = st.text_area("Internal need", defaults.internal_need if defaults else "")
        col3, col4 = st.columns(2)
        motivation = col3.text_area("Motivation", defaults.motivation if defaults else "")
        fear = col4.text_area("Fear", defaults.fear if defaults else "")
        contradiction = st.text_area(
            "Dramatic contradiction", defaults.contradiction if defaults else ""
        )
        behavior = st.text_area(
            "Behavior signature", defaults.behavior_signature if defaults else ""
        )
        voice = st.text_area("Voice", defaults.voice if defaults else "")
        arc = st.text_area("Arc", defaults.arc if defaults else "")
        submitted = st.form_submit_button("Preserve character")
    if submitted:
        try:
            _service().upsert_character(
                character_id=defaults.character_id if defaults else None,
                name=name,
                role=role,
                external_objective=external,
                internal_need=internal,
                motivation=motivation,
                fear=fear,
                contradiction=contradiction,
                behavior_signature=behavior,
                voice=voice,
                arc=arc,
            )
        except NKAValidationError as exc:
            st.error(str(exc))
        else:
            _flash("Character preserved as a new blueprint revision.")
            st.rerun()


def _render_phase_two() -> None:
    st.subheader("Phase 2 · Assemble the dramatic cast")
    if not _phase_guard(2):
        return
    state = _repository().head.state
    st.write(
        "Choose useful dramatic functions, then make each character specific. Suggestions are proposals, never silent additions."
    )
    with st.expander("Architect's suggested cast", expanded=not bool(state.characters)):
        for index, option in enumerate(suggest_characters(state)):
            st.markdown(f"**{option.name} · {option.role}**")
            st.write(option.contradiction)
            st.caption(f"Arc: {option.arc}")
            if st.button("Add this character", key=f"add-character-option-{index}"):
                _service().add_character_option(option)
                _flash(f"Added {option.name} as an editable proposal.")
                st.rerun()
    if state.characters:
        for character in state.characters:
            with st.expander(f"{character.name} · {character.role}"):
                st.write(character.contradiction or "Contradiction not established.")
                st.caption(character.arc or "Arc not established.")
        selected = st.selectbox(
            "Edit character", state.characters, format_func=lambda item: item.name
        )
        with st.expander("Edit selected character"):
            _character_form(selected)
    with st.expander("Create a character manually"):
        _character_form()
    if st.button("Lock principal cast and continue", type="primary"):
        _lock(2, "Principal cast locked. Phase 3 can now build the complete plot.")


def _render_phase_three() -> None:
    st.subheader("Phase 3 · Build the full plot")
    if not _phase_guard(3):
        return
    state = _repository().head.state
    st.write(
        "Work conversationally by editing the plot, or ask the Architect to produce a complete causal draft from the locked blueprint."
    )
    request = st.text_input(
        "Optional direction for the plot draft",
        placeholder="Make the midpoint a public reversal; keep the ending hopeful.",
    )
    if st.button("Write the full plot for me", type="secondary"):
        generated, source = _skill_generate(
            "plot_builder.md", draft_full_plot(state), request or "Draft the full plot."
        )
        st.session_state.draft_full_plot = generated
        st.session_state.draft_full_plot_source = source
        st.rerun()
    if source := st.session_state.get("draft_full_plot_source"):
        st.caption(source)
    with st.form("full-plot-form"):
        full_plot = st.text_area(
            "Full plot", st.session_state.get("draft_full_plot", state.full_plot), height=330
        )
        objective = st.text_area("Protagonist's screenplay objective", state.protagonist_objective)
        stakes = st.text_area("Stakes", state.stakes)
        theme = st.text_area("Thematic argument", state.theme)
        ending = st.text_area("Ending", state.ending)
        submitted = st.form_submit_button("Lock full plot", type="primary")
    if submitted:
        try:
            _service().update_plot(
                full_plot=full_plot,
                protagonist_objective=objective,
                stakes=stakes,
                theme=theme,
                ending=ending,
            )
            _service().lock_phase(3)
        except NKAValidationError as exc:
            st.error(str(exc))
        else:
            _flash("Full plot locked. The Architect can now freeze its screenplay structure.")
            st.rerun()


def _default_events(state: Any, structure: str) -> list[str]:
    sentences = [
        part.strip() for part in state.full_plot.replace("\n", " ").split(".") if part.strip()
    ]
    specs = structure_beats(structure)
    return [
        f"{sentences[index % len(sentences)]}. ({purpose})" if sentences else purpose
        for index, (_label, _act, purpose) in enumerate(specs)
    ]


def _render_phase_four() -> None:
    st.subheader("Phase 4 · Freeze the screenplay structure")
    if not _phase_guard(4):
        return
    state = _repository().head.state
    recommended, rationale = recommend_structure(state)
    st.info(f"**Architect recommends: {recommended}.** {rationale}")
    structure = st.selectbox(
        "Screenplay structure",
        STRUCTURES,
        index=STRUCTURES.index(state.structure_type or recommended),
    )
    specs = structure_beats(structure)
    defaults = (
        [beat.event for beat in state.beats]
        if state.structure_type == structure and len(state.beats) == len(specs)
        else _default_events(state, structure)
    )
    with st.form("structure-form"):
        structure_rationale = st.text_area(
            "Why this structure serves this plot", state.structure_rationale or rationale
        )
        events = []
        for index, ((label, act, purpose), default) in enumerate(
            zip(specs, defaults, strict=True), 1
        ):
            st.markdown(f"**{index}. {label} · {act}**")
            st.caption(purpose)
            events.append(
                st.text_area("Approved story event", default, key=f"beat-event-{structure}-{index}")
            )
        submitted = st.form_submit_button("Lock structural blueprint", type="primary")
    if submitted:
        try:
            _service().set_structure(
                structure_type=structure, rationale=structure_rationale, beat_events=events
            )
            _service().lock_phase(4)
        except NKAValidationError as exc:
            st.error(str(exc))
        else:
            _flash("Structure locked. Scene construction is ready.")
            st.rerun()


def _scene_form(scene: Any) -> None:
    state = _repository().head.state
    character_map = {character.character_id: character.name for character in state.characters}
    beat_map = {beat.beat_id: f"{beat.ordinal}. {beat.label}" for beat in state.beats}
    with st.form(f"scene-form-{scene.scene_id}"):
        heading = st.text_input("Scene heading", scene.heading)
        col1, col2 = st.columns([2, 1])
        location = col1.text_input("Playable location", scene.location)
        time = col2.text_input("Time", scene.time_of_day)
        beat_ids = list(beat_map)
        beat = st.selectbox(
            "Structural beat served",
            beat_ids,
            index=beat_ids.index(scene.structural_beat_id)
            if scene.structural_beat_id in beat_ids
            else 0,
            format_func=lambda item: beat_map[item],
        )
        character_ids = list(character_map)
        present = st.multiselect(
            "Characters present",
            character_ids,
            default=list(scene.character_ids),
            format_func=lambda item: character_map[item],
        )
        viewpoint = st.selectbox(
            "Viewpoint character",
            ["", *character_ids],
            index=(
                ["", *character_ids].index(scene.viewpoint_character_id)
                if scene.viewpoint_character_id in character_ids
                else 0
            ),
            format_func=lambda item: character_map.get(item, "Not assigned"),
        )
        summary = st.text_area("What happens", scene.summary)
        entry = st.text_area("Entry state", scene.entry_state)
        objective = st.text_area("Immediate objective", scene.objective)
        conflict = st.text_area("Active resistance / mini-conflict", scene.conflict)
        escalation = st.text_area("Escalation", scene.escalation)
        turning = st.text_area("Turning point", scene.turning_point)
        outcome = st.text_area("Resolution / exit state", scene.outcome)
        emotional = st.text_area("Character or emotional change", scene.emotional_change)
        behavior = st.text_area("Character behavior that proves the arc", scene.character_behavior)
        blocking = st.text_area("Blocking and staging", scene.blocking)
        setup = st.text_area("Setup / payoff connection", scene.setup_payoff)
        st.markdown("#### Dialogue · context, text, subtext")
        context = st.text_area("Context", scene.dialogue_context)
        text = st.text_area("Draft dialogue", scene.dialogue_text)
        subtext = st.text_area("Subtext", scene.dialogue_subtext)
        submitted = st.form_submit_button("Preserve engineered scene", type="primary")
    if submitted:
        try:
            _service().upsert_scene(
                scene_id=scene.scene_id,
                heading=heading,
                summary=summary,
                location=location,
                time_of_day=time,
                structural_beat_id=beat,
                viewpoint_character_id=viewpoint,
                entry_state=entry,
                objective=objective,
                conflict=conflict,
                escalation=escalation,
                turning_point=turning,
                outcome=outcome,
                emotional_change=emotional,
                character_behavior=behavior,
                dialogue_context=context,
                dialogue_text=text,
                dialogue_subtext=subtext,
                blocking=blocking,
                setup_payoff=setup,
                character_ids=tuple(present),
            )
        except NKAValidationError as exc:
            st.error(str(exc))
        else:
            _flash("Scene preserved and scorecard recalculated.")
            st.rerun()


def _render_phase_five() -> None:
    st.subheader("Phase 5 · Engineer the scene sequence")
    if not _phase_guard(5):
        return
    state = _repository().head.state
    st.write(
        "This is the construction heart: every scene must operate as a mini-plot and justify its place, conflict, characters, behavior and dialogue."
    )
    if st.button("Generate one editable scene card per structural beat", type="secondary"):
        _service().generate_scene_plan()
        _flash("Generated story-grounded scene drafts from the locked blueprint.")
        st.rerun()
    if not state.scenes:
        st.info(
            "Generate the scene blueprint, then refine each card until the construction gate passes."
        )
        return
    report = assess_screenplay(state)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Completion coverage", f"{report.completion_coverage_score_0_5:.2f}/5")
    col2.metric("Craft quality", f"{report.craft_quality_score_0_5:.2f}/5")
    col3.metric("Structural coverage", f"{report.coverage_percent}%")
    col4.metric("Scenes needing craft pass", report.template_scene_count)
    st.caption(
        "Completion asks whether the construction evidence exists. Craft quality asks whether it is story-specific and playable; scaffold language cannot receive a high score."
    )
    selected = st.selectbox(
        "Open scene card", state.scenes, format_func=lambda item: f"{item.ordinal}. {item.heading}"
    )
    card = next(item for item in report.scenes if item.scene_id == selected.scene_id)
    st.markdown(
        " ".join(f"`{item.name}: {item.score_0_5}/5`" for item in card.dimensions)
        + f" &nbsp; **Completion {card.completion_score_0_5:.2f}/5 · Craft {card.craft_quality_score_0_5:.2f}/5**"
    )
    for flag in card.quality_flags:
        st.warning(flag)
    with st.expander("Edit complete scene card", expanded=True):
        _scene_form(selected)
    complete, blockers = build_complete(state)
    if complete:
        st.success(
            "Every beat is covered, required evidence is complete, and every scene meets the 3.0/5 craft-readiness floor."
        )
        if st.button("Mark build complete · proceed to final phase", type="primary"):
            _lock(5, "Build complete. Proceed to the final compilation and scorecard.")
    else:
        st.warning("Build gate remains open.")
        for blocker in blockers:
            st.markdown(f"- {blocker}")


def _render_phase_six() -> None:
    st.subheader("Phase 6 · Compile the first draft")
    if not _phase_guard(6):
        return
    repository = _repository()
    state = repository.head.state
    readiness = assess_readiness(state)
    report = assess_screenplay(state)
    if readiness.blockers:
        st.error("Compilation is blocked: " + " ".join(readiness.blockers))
        return
    st.success("Build complete · the accepted construction can be compiled.")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Completion coverage", f"{report.completion_coverage_score_0_5:.2f}/5")
    col2.metric("First-draft craft quality", f"{report.craft_quality_score_0_5:.2f}/5")
    col3.metric("Structural coverage", f"{report.coverage_percent}%")
    col4.metric("Canonical revision", repository.head.revision_id[:12])
    st.caption(
        "Completion and deterministic craft evidence are reported separately. Scores are capped while scaffold or placeholder language remains; neither score predicts audience or commercial success."
    )
    fountain = compile_bounded_fountain(repository.head)
    scorecard = compile_scorecard_markdown(repository.head)
    col4, col5, col6 = st.columns(3)
    col4.download_button(
        "Download Fountain draft",
        fountain,
        f"{_safe_name(state.title)}.fountain",
        "text/plain",
        width="stretch",
    )
    col5.download_button(
        "Download scorecard",
        scorecard,
        f"{_safe_name(state.title)}-scorecard.md",
        "text/markdown",
        width="stretch",
    )
    col6.download_button(
        "Download full project",
        repository.export_json(),
        f"{_safe_name(state.title)}-project.json",
        "application/json",
        width="stretch",
    )
    with st.expander("Scene-by-scene scorecard", expanded=True):
        rows = []
        for card in report.scenes:
            row = {
                "Scene": card.scene_heading,
                "Completion /5": card.completion_score_0_5,
                "Craft /5": card.craft_quality_score_0_5,
                "Craft flags": " ".join(card.quality_flags) or "None",
            }
            row.update({dimension.name: dimension.score_0_5 for dimension in card.dimensions})
            rows.append(row)
        st.dataframe(rows, width="stretch", hide_index=True)
    with st.expander("Compiled screenplay draft"):
        st.code(fountain, language=None, line_numbers=True)
    if 6 not in state.locked_phases and st.button("Finalize build revision", type="primary"):
        _lock(6, "Screenplay build finalized and bound to its scorecard revision.")


def _safe_name(title: str) -> str:
    safe = "".join(character.lower() if character.isalnum() else "-" for character in title)
    return "-".join(part for part in safe.split("-") if part) or "untitled-screenplay"


def _install_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp { background: linear-gradient(180deg, #f7f2e8 0%, #fffdf8 28%, #ffffff 100%); }
        .na-hero { padding: 1.35rem 0 .75rem; border-bottom: 1px solid #d8cbb8; }
        .na-hero h1 { margin: .08rem 0; font: 700 3rem Georgia, serif; color: #172a27; }
        .na-hero p { margin: .3rem 0; color: #4f5d58; font-size: 1.08rem; }
        .na-kicker { color: #a4512c; letter-spacing: .16em; font-weight: 800; font-size: .72rem; }
        .phase-row { display:flex; justify-content:space-between; gap:.5rem; padding:.42rem .2rem; border-bottom:1px solid #ece3d5; font-size:.86rem; }
        .phase-row span { color:#7c756b; font-size:.76rem; white-space:nowrap; }
        [data-testid="stMetric"] { background:#fffaf1; border:1px solid #e4d8c6; padding:.75rem; border-radius:.55rem; }
        [data-baseweb="tab-list"] { gap:.15rem; }
        [data-baseweb="tab"] { background:#f5efe5; border-radius:.45rem .45rem 0 0; padding:.55rem .75rem; }
        [aria-selected="true"][data-baseweb="tab"] { background:#173f38; color:#fff; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(
        page_title="Narrative Architect",
        page_icon="✦",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _install_styles()
    _repository()
    _render_sidebar()
    _render_header()
    _consume_flash()
    tabs = st.tabs([f"{index} · {name}" for index, name in enumerate(PHASES, 1)])
    renderers = (
        _render_phase_one,
        _render_phase_two,
        _render_phase_three,
        _render_phase_four,
        _render_phase_five,
        _render_phase_six,
    )
    for tab, renderer in zip(tabs, renderers, strict=True):
        with tab:
            renderer()

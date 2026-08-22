"""Narrative Architect Foundation Alpha Streamlit application."""

from __future__ import annotations

import os
from typing import Any, cast

import streamlit as st

from narrative_architect.application.projects import StoryProjectService, demo_repository
from narrative_architect.conversation.guide import apply_guided_answer, next_guidance_step
from narrative_architect.create.compiler import assess_readiness, compile_bounded_fountain
from narrative_architect.knowledge.nka import (
    InMemoryProjectRepository,
    NKAValidationError,
)

APP_VERSION = "0.1.0"


def _initial_messages() -> list[dict[str, str]]:
    return [
        {
            "role": "assistant",
            "content": (
                "Bring me the story as it exists in your head—even if it is only a fragment. "
                "We will establish one decision at a time, and every accepted answer will become "
                "part of your canonical Narrative Knowledge Asset."
            ),
        }
    ]


def _set_repository(repository: InMemoryProjectRepository) -> None:
    st.session_state.repository = repository
    st.session_state.messages = _initial_messages()


def _repository() -> InMemoryProjectRepository:
    if "repository" not in st.session_state:
        _set_repository(InMemoryProjectRepository.create())
    return cast(InMemoryProjectRepository, st.session_state.repository)


def _service() -> StoryProjectService:
    return StoryProjectService(_repository())


def _flash_success(message: str) -> None:
    st.session_state.flash_success = message


def _consume_flash() -> None:
    message = st.session_state.pop("flash_success", None)
    if message:
        st.success(message)


def _render_header() -> None:
    st.markdown(
        """
        <div class="na-hero">
          <div class="na-kicker">CONSAAS · NARRATIVE INTELLIGENCE</div>
          <h1>Narrative Architect</h1>
          <p>Your story is not the chat. The canonical Narrative Knowledge Asset is the story.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(
        f"Foundation Alpha v{APP_VERSION} · Create-first · Deterministic guidance · No external LLM"
    )


def _render_sidebar() -> None:
    repository = _repository()
    state = repository.head.state
    with st.sidebar:
        st.markdown("### Story workspace")
        st.caption(f"Project `{repository.project_id[-8:]}`")
        st.markdown(f"**{state.title}**")
        st.caption(
            f"Head `{repository.head_revision_id[:12]}` · {len(repository.history)} revisions"
        )

        col1, col2 = st.columns(2)
        if col1.button("New", use_container_width=True):
            _set_repository(InMemoryProjectRepository.create())
            st.rerun()
        if col2.button("Load demo", use_container_width=True):
            _set_repository(demo_repository())
            _flash_success("Loaded the synthetic demonstration project.")
            st.rerun()

        st.download_button(
            "Download project JSON",
            data=repository.export_json(),
            file_name=f"{_safe_name(state.title)}-project.json",
            mime="application/json",
            use_container_width=True,
        )
        uploaded = st.file_uploader("Reload project JSON", type=["json"])
        if uploaded is not None and st.button("Import project", use_container_width=True):
            try:
                imported = InMemoryProjectRepository.import_json(
                    uploaded.getvalue().decode("utf-8")
                )
            except (UnicodeDecodeError, NKAValidationError) as exc:
                st.error(str(exc))
            else:
                _set_repository(imported)
                _flash_success("Project and revision history restored.")
                st.rerun()

        if len(repository.history) > 1:
            st.markdown("#### Revision history")
            options = list(reversed(repository.history[:-1]))
            selected = st.selectbox(
                "Restore an earlier version",
                options,
                format_func=lambda revision: f"{revision.revision_id[:10]} · {revision.reason}",
            )
            if st.button("Restore as new revision", use_container_width=True):
                _service().restore(selected.revision_id)
                _flash_success("Earlier story state restored without deleting history.")
                st.rerun()

        st.divider()
        profile = os.getenv("NARRATIVE_PROFILE", "hosted_demo")
        if profile == "local_private":
            st.success("Local-private profile")
            st.caption("Project content is processed in this local application process.")
        else:
            st.warning("Hosted demonstration profile")
            st.caption(
                "Do not enter confidential or unpublished screenplay material. Hosted sessions are "
                "temporary; download the project before leaving."
            )
        st.caption("Doctor mode and local model intelligence arrive through curated increments.")


def _render_create() -> None:
    service = _service()
    state = service.head.state
    left, right = st.columns([1.65, 1], gap="large")
    with left:
        st.subheader("Conversation workspace")
        st.caption("The guide reads the current NKA—not the transcript—to decide what to ask next.")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        step = next_guidance_step(state)
        if step is None:
            with st.chat_message("assistant"):
                st.markdown(
                    "Your foundation now has the minimum structural spine. Refine the "
                    "characters and "
                    "scenes in their dedicated views, then compile the bounded draft."
                )
            st.success("Foundation spine established")
        else:
            with st.chat_message("assistant"):
                st.markdown(f"**{step.question}**")
                st.caption(step.why_it_matters)
            answer = st.chat_input(f"Establish {step.label.lower()}…")
            if answer:
                st.session_state.messages.append({"role": "user", "content": answer})
                try:
                    response = apply_guided_answer(service, step, answer)
                except (ValueError, NKAValidationError) as exc:
                    response = f"I could not preserve that yet: {exc}"
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

    with right:
        st.subheader("Canonical story at a glance")
        completed = sum(
            bool(value)
            for value in (
                state.premise,
                state.protagonist_objective,
                state.central_conflict,
                state.stakes,
                state.theme,
                state.ending,
            )
        )
        st.progress(completed / 6, text=f"Story decisions established: {completed}/6")
        _knowledge_card("Premise", state.premise)
        _knowledge_card("Central conflict", state.central_conflict)
        _knowledge_card("Stakes", state.stakes)
        col1, col2 = st.columns(2)
        col1.metric("Characters", len(state.characters))
        col2.metric("Scenes", len(state.scenes))
        st.info(
            "Chat is the experience; the NKA is memory. Deleting the presentation transcript would "
            "not erase the story decisions already preserved here."
        )


def _knowledge_card(label: str, value: str) -> None:
    st.markdown(f"**{label}**")
    st.write(value or "_Not established yet._")


def _render_knowledge() -> None:
    service = _service()
    state = service.head.state
    st.subheader("Narrative Knowledge Asset")
    st.caption("These author-confirmed fields—not conversational wording—are canonical.")
    with st.form("story-knowledge-form"):
        title = st.text_input("Title", state.title)
        premise = st.text_area("Premise", state.premise, height=100)
        protagonist_objective = st.text_area(
            "Protagonist objective", state.protagonist_objective, height=80
        )
        central_conflict = st.text_area("Central conflict", state.central_conflict, height=80)
        stakes = st.text_area("Stakes", state.stakes, height=80)
        theme = st.text_area("Theme", state.theme, height=80)
        ending = st.text_area("Ending", state.ending, height=80)
        submitted = st.form_submit_button("Preserve story revision", type="primary")
    if submitted:
        try:
            service.update_story(
                "Revise story knowledge",
                title=title,
                premise=premise,
                protagonist_objective=protagonist_objective,
                central_conflict=central_conflict,
                stakes=stakes,
                theme=theme,
                ending=ending,
            )
        except NKAValidationError as exc:
            st.error(str(exc))
        else:
            _flash_success("Canonical story knowledge revised.")
            st.rerun()


def _render_characters() -> None:
    service = _service()
    characters = service.head.state.characters
    st.subheader("Characters")
    st.caption(
        "Character choices should serve the plot while retaining emotional and ideological depth."
    )
    options: list[Any] = [None, *characters]
    selected = st.selectbox(
        "Edit or add",
        options,
        format_func=lambda character: "＋ Add character" if character is None else character.name,
    )
    defaults = selected
    with st.form("character-form"):
        col1, col2 = st.columns([2, 1])
        name = col1.text_input("Name", defaults.name if defaults else "")
        role = col2.selectbox(
            "Role",
            ["Protagonist", "Antagonist", "Supporting", "Minor"],
            index=(
                ["Protagonist", "Antagonist", "Supporting", "Minor"].index(defaults.role)
                if defaults
                and defaults.role in {"Protagonist", "Antagonist", "Supporting", "Minor"}
                else 2
            ),
        )
        external_objective = st.text_area(
            "External objective", defaults.external_objective if defaults else ""
        )
        internal_need = st.text_area("Internal need", defaults.internal_need if defaults else "")
        motivation = st.text_area("Motivation", defaults.motivation if defaults else "")
        ideology = st.text_area("Ideology", defaults.ideology if defaults else "")
        fear = st.text_area("Fear", defaults.fear if defaults else "")
        arc = st.text_area("Arc", defaults.arc if defaults else "")
        submitted = st.form_submit_button("Preserve character", type="primary")
    if submitted:
        try:
            service.upsert_character(
                character_id=defaults.character_id if defaults else None,
                name=name,
                role=role,
                external_objective=external_objective,
                internal_need=internal_need,
                motivation=motivation,
                ideology=ideology,
                fear=fear,
                arc=arc,
            )
        except NKAValidationError as exc:
            st.error(str(exc))
        else:
            _flash_success("Character preserved in a new NKA revision.")
            st.rerun()

    if characters:
        st.markdown("### Character map")
        for character in characters:
            with st.expander(f"{character.name} · {character.role}"):
                _labelled_text("Objective", character.external_objective)
                _labelled_text("Internal need", character.internal_need)
                _labelled_text("Motivation", character.motivation)
                _labelled_text("Ideology", character.ideology)
                _labelled_text("Fear", character.fear)
                _labelled_text("Arc", character.arc)


def _render_scenes() -> None:
    service = _service()
    state = service.head.state
    options: list[Any] = [None, *state.scenes]
    st.subheader("Scene board")
    st.caption(
        "Each scene should pursue an objective, encounter resistance, and finish somewhere new."
    )
    selected = st.selectbox(
        "Edit or add",
        options,
        format_func=lambda scene: (
            "＋ Add scene" if scene is None else f"{scene.ordinal}. {scene.heading}"
        ),
    )
    defaults = selected
    character_map = {character.character_id: character.name for character in state.characters}
    with st.form("scene-form"):
        heading = st.text_input("Scene heading", defaults.heading if defaults else "")
        col1, col2 = st.columns([2, 1])
        location = col1.text_input("Location", defaults.location if defaults else "")
        time_of_day = col2.text_input("Time of day", defaults.time_of_day if defaults else "DAY")
        selected_characters = st.multiselect(
            "Characters present",
            list(character_map),
            default=list(defaults.character_ids) if defaults else [],
            format_func=lambda character_id: character_map[character_id],
        )
        summary = st.text_area("What happens?", defaults.summary if defaults else "", height=100)
        objective = st.text_area("Scene objective", defaults.objective if defaults else "")
        conflict = st.text_area("Conflict / obstacle", defaults.conflict if defaults else "")
        outcome = st.text_area("Outcome", defaults.outcome if defaults else "")
        emotional_change = st.text_area(
            "Emotional change", defaults.emotional_change if defaults else ""
        )
        submitted = st.form_submit_button("Preserve scene", type="primary")
    if submitted:
        try:
            service.upsert_scene(
                scene_id=defaults.scene_id if defaults else None,
                heading=heading,
                summary=summary,
                location=location,
                time_of_day=time_of_day,
                objective=objective,
                conflict=conflict,
                outcome=outcome,
                emotional_change=emotional_change,
                character_ids=tuple(selected_characters),
            )
        except NKAValidationError as exc:
            st.error(str(exc))
        else:
            _flash_success("Scene preserved in a new NKA revision.")
            st.rerun()

    if state.scenes:
        st.markdown("### Ordered screenplay foundation")
        for scene in state.scenes:
            with st.expander(f"{scene.ordinal}. {scene.heading}", expanded=True):
                st.write(scene.summary)
                col1, col2, col3 = st.columns(3)
                col1.markdown(f"**Objective**\n\n{scene.objective or 'Open'}")
                col2.markdown(f"**Conflict**\n\n{scene.conflict or 'Open'}")
                col3.markdown(f"**Outcome**\n\n{scene.outcome or 'Open'}")


def _render_compile() -> None:
    repository = _repository()
    state = repository.head.state
    report = assess_readiness(state)
    st.subheader("Compile the accepted foundation")
    st.caption(
        "The compiler translates established NKA content. It does not invent missing action "
        "or dialogue."
    )
    if report.blockers:
        st.error("Compilation is blocked.")
        for blocker in report.blockers:
            st.markdown(f"- {blocker}")
    else:
        st.success("The bounded foundation can be compiled.")
    if report.warnings:
        with st.expander("Readiness warnings", expanded=True):
            for warning in report.warnings:
                st.markdown(f"- {warning}")
    if report.can_compile:
        compiled = compile_bounded_fountain(repository.head)
        st.download_button(
            "Download bounded Fountain draft",
            data=compiled,
            file_name=f"{_safe_name(state.title)}-foundation.fountain",
            mime="text/plain",
            type="primary",
        )
        st.code(compiled, language=None, line_numbers=True)


def _render_doctor_roadmap() -> None:
    st.subheader("Doctor mode · Curated backlog")
    st.info("Not enabled in the Foundation Alpha. No screenplay upload is accepted yet.")
    st.markdown(
        """
        Doctor mode will arrive through independently testable increments:

        1. deterministic PDF block and atomic-scene parsing;
        2. reviewed mapping from atomic scenes to analyst-defined macro-scenes;
        3. Four-Pillar diagnosis and reconciled iMaSc scorecard;
        4. deterministic weighted scoring and Narrative Momentum;
        5. evidence drill-down and conversational Script Doctor.

        The product diagnoses screenplay construction. It will not claim to predict film success.
        """
    )


def _labelled_text(label: str, value: str) -> None:
    st.markdown(f"**{label}:** {value or 'Not established'}")


def _safe_name(title: str) -> str:
    safe = "".join(character.lower() if character.isalnum() else "-" for character in title)
    return "-".join(part for part in safe.split("-") if part) or "untitled-story"


def _install_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp { background: linear-gradient(180deg, #fbfaf7 0%, #ffffff 38%); }
        .na-hero { padding: 1.2rem 0 .55rem 0; border-bottom: 1px solid #e5dfd3; }
        .na-hero h1 { margin: .1rem 0; font-family: Georgia, serif; color: #182421; }
        .na-hero p { margin: .25rem 0; color: #53605b; font-size: 1.04rem; }
        .na-kicker { color: #9a5b36; letter-spacing: .14em; font-weight: 700; font-size: .72rem; }
        [data-testid="stMetric"] { background: #f4f0e8; border: 1px solid #e6ddcf; padding: .7rem; }
        [data-testid="stChatMessage"] { border: 1px solid #ece6dc; background: #fff; }
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
    create_tab, knowledge_tab, character_tab, scene_tab, compile_tab, doctor_tab = st.tabs(
        ["Create", "Knowledge", "Characters", "Scenes", "Compile", "Doctor · Roadmap"]
    )
    with create_tab:
        _render_create()
    with knowledge_tab:
        _render_knowledge()
    with character_tab:
        _render_characters()
    with scene_tab:
        _render_scenes()
    with compile_tab:
        _render_compile()
    with doctor_tab:
        _render_doctor_roadmap()

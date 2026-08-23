"""Streamlit experience for the ConSaaS Decision Studio Foundation MVP."""

from __future__ import annotations

import html
import json
import os
from pathlib import Path
from typing import Any, cast

import streamlit as st

from core.ai.adapters.groq import GroqProvider
from core.ai.registry import ModelRegistry
from decision_studio.browser_expert import browser_expert
from decision_studio.case import CaseKnowledgeAsset
from decision_studio.catalog import (
    PRODUCTS,
    load_current_gka,
    load_decision_atlas,
    load_metric_catalog,
    load_skill,
)
from decision_studio.conversation import (
    DialogueAction,
    apply_action,
    browser_prompt,
    deterministic_action,
    deterministic_actions,
    guard_repeated_narrative,
    validate_model_action,
)
from decision_studio.narrator import ConsultantNarrative, narrate
from decision_studio.report_qa import answer_report_question, report_to_markdown
from decision_studio.service import DecisionStudio
from plugin_sdk.decision import DecisionReport, Question

APP_VERSION = "0.5.2"
ROOT = Path(__file__).resolve().parents[1]


def _install_theme() -> None:
    st.markdown(
        """
        <style>
        .stApp { background:#fff; }
        .block-container { max-width: 1280px; padding-top: 2rem; padding-bottom: 4rem; }
        .cs-hero { background:#f8f6f0; padding:1rem 1.25rem 1.4rem;
                   border:1px solid #e5ded2; border-radius:16px; }
        .cs-kicker { color:#8b5a2b; letter-spacing:.14em; font-weight:800; font-size:.72rem;
                     line-height:1.5; padding:.08rem 0; }
        .cs-hero h1 { font-family:Georgia,serif; font-size:3.2rem; letter-spacing:-.045em;
                      color:#19231f; margin:.2rem 0; }
        .cs-hero p { color:#56605b; font-size:1.13rem; max-width:850px; margin:.25rem 0; }
        .cs-promise { font-family:Georgia,serif; font-size:1.45rem; color:#26342e;
                      padding:1.1rem 0 .35rem; }
        .cs-product { min-height:270px; }
        .cs-icon { font-family:Georgia,serif; font-size:2.2rem; color:#8b5a2b; }
        .cs-domain { text-transform:uppercase; letter-spacing:.09em; font-size:.68rem;
                     color:#8a7764; font-weight:800; }
        .cs-product h3 { font-family:Georgia,serif; margin:.3rem 0; color:#24312c; }
        .cs-foundation { background:#f2eee5; border:1px solid #e1d8c9;
                         border-radius:999px; padding:.22rem .65rem; font-size:.72rem;
                         color:#6b5a47; display:inline-block; }
        .cs-verdict { border-left:5px solid #8b5a2b; background:#fffaf1; padding:1rem 1.2rem;
                      border-radius:0 12px 12px 0; margin:.6rem 0 1rem; }
        .cs-verdict h2 { font-family:Georgia,serif; color:#26352e; margin:.15rem 0; }
        .cs-section { color:#855527; letter-spacing:.1em; text-transform:uppercase;
                      font-size:.72rem; font-weight:800; }
        [data-testid="stChatMessage"] { border:1px solid #e4ded3; background:#fff;
                                         border-radius:12px; }
        [data-testid="stMetric"] { background:#f6f2ea; border:1px solid #e4ddcf; padding:.75rem; }
        div[data-testid="stVerticalBlockBorderWrapper"] { border-color:#e1dacf !important;
                                                            border-radius:14px !important; }
        .stTabs [data-baseweb="tab-list"] { gap:1.2rem; border-bottom:1px solid #ded7ca; }
        [data-testid="stBaseButton-primary"] { background:#315b4b; border-color:#315b4b; }
        [data-testid="stBaseButton-primary"]:hover { background:#27493d; border-color:#27493d; }
        @media(max-width:768px) { .cs-hero h1 { font-size:2.25rem; } }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _init() -> None:
    defaults: dict[str, Any] = {
        "selected_product": None,
        "consultations": {},
        "narratives": {},
        "browser_expert_enabled": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _header() -> None:
    st.markdown(
        """
        <div class="cs-hero">
          <div class="cs-kicker">CONSAAS · DECISION INTELLIGENCE</div>
          <h1>ConSaaS Core</h1>
          <p>We de-risk high-stakes decisions in real estate, higher education
          and startup evaluation.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(
        f"Decision Studio Consulting v{APP_VERSION} · Explainable by design · No paid AI required"
    )


def _landing() -> None:
    st.markdown(
        '<div class="cs-promise">Choose the decision you need to make—not the tool '
        "you want to use.</div>",
        unsafe_allow_html=True,
    )
    st.write(
        "Each consultant asks the questions with the greatest decision value, preserves confirmed "
        "facts in a Case Knowledge Asset, then evaluates them against governed knowledge and a "
        "versioned methodology."
    )
    columns = st.columns(3, gap="large")
    for column, product in zip(columns, PRODUCTS.values(), strict=True):
        with column, st.container(border=True):
            st.markdown(
                f"""
                <div class="cs-product">
                  <div class="cs-icon">{html.escape(product.icon)}</div>
                  <div class="cs-domain">{html.escape(product.domain)}</div>
                  <h3>{html.escape(product.name)}</h3>
                  <p>{html.escape(product.promise)}</p>
                  <span class="cs-foundation">GKA v1.0 Decision Coverage</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(
                f"Start {product.name}",
                key=f"start-{product.product_id}",
                width="stretch",
                type="primary",
            ):
                st.session_state.selected_product = product.product_id
                st.rerun()
    st.divider()
    st.subheader("One operating system. Three kinds of judgment.")
    pillars = st.columns(4)
    for column, title, body in zip(
        pillars,
        (
            "Canonical memory",
            "Deterministic verdict",
            "Provider-free conversation",
            "Evidence trail",
        ),
        (
            "The structured brief—not chat history—is the source of truth.",
            "Rules, constraints and scores are replayable and versioned.",
            "An optional browser model makes dialogue natural without owning the decision.",
            "Every result identifies asset, policy, assumptions and limitations.",
        ),
        strict=True,
    ):
        with column:
            st.markdown(f"**{title}**")
            st.caption(body)
    st.warning(
        "Metric coverage is comprehensive for the current v1 decision contract; observations "
        "remain curated and bounded. Verify exact programme, property and venture evidence before "
        "a consequential commitment."
    )


def _consultation(product_id: str) -> dict[str, Any]:
    consultations = st.session_state.consultations
    if product_id not in consultations:
        consultations[product_id] = {
            "case": CaseKnowledgeAsset(product_id),
            "messages": [],
            "report": None,
            "pending_turn": None,
            "report_messages": [],
        }
    state = cast(dict[str, Any], consultations[product_id])
    state.setdefault("report_messages", [])
    return state


def _answer_widget(
    question: Question, *, key_prefix: str = "answer", initial_value: Any = None
) -> Any:
    key = f"{key_prefix}-{st.session_state.selected_product}-{question.question_id}"
    if question.answer_type == "choice":
        index = question.options.index(initial_value) if initial_value in question.options else 0
        return st.selectbox(
            "Your answer",
            question.options,
            index=index,
            key=key,
            label_visibility="collapsed",
        )
    if question.answer_type == "text":
        return st.text_area(
            "Your answer",
            value=str(initial_value or question.default or ""),
            height=130,
            max_chars=1600,
            placeholder=question.expert_context,
            key=key,
            label_visibility="collapsed",
        )
    return st.number_input(
        "Your answer",
        min_value=question.minimum,
        max_value=question.maximum,
        value=initial_value if initial_value is not None else question.default,
        step=question.step,
        key=key,
        label_visibility="collapsed",
    )


def _format_inr(value: float) -> str:
    """Format a numeric amount with Indian digit grouping."""
    rounded = round(value)
    sign = "-" if rounded < 0 else ""
    digits = str(abs(rounded))
    if len(digits) <= 3:
        grouped = digits
    else:
        tail = digits[-3:]
        head = digits[:-3]
        groups: list[str] = []
        while head:
            groups.append(head[-2:])
            head = head[:-2]
        grouped = f"{','.join(reversed(groups))},{tail}"
    return f"{sign}₹{grouped}"


def _display_label(key: str) -> str:
    """Turn an internal metric key into a concise UI label."""
    return key.replace("_", " ").replace("₹", "").replace("%", "").strip().capitalize()


def _display_value(key: str, value: Any) -> str:
    """Format structured values without leaking JSON notation into the UI."""
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (int, float)):
        if "₹" in key:
            return _format_inr(float(value))
        if "%" in key:
            return f"{float(value):,.1f}%"
        return f"{float(value):,.0f}" if float(value).is_integer() else f"{float(value):,.1f}"
    if isinstance(value, (list, tuple)):
        return " · ".join(str(item) for item in value)
    return str(value)


def _display_rows(values: dict[str, Any]) -> list[dict[str, str]]:
    """Create two-column presentation rows for a structured mapping."""
    return [
        {"Metric": _display_label(key), "Value": _display_value(key, value)}
        for key, value in values.items()
    ]


def _complete_dialogue_action(
    product_id: str,
    service: DecisionStudio,
    state: dict[str, Any],
    action: DialogueAction,
) -> None:
    state["case"] = apply_action(state["case"], action)
    state["messages"].append(
        {
            "role": "assistant",
            "content": f"{action.acknowledgement}\n\n{action.guidance}",
            "model_id": action.model_id,
        }
    )
    state["report"] = service.decide_if_ready(product_id, state["case"].values)
    state["pending_turn"] = None


def _complete_dialogue_actions(
    product_id: str,
    service: DecisionStudio,
    state: dict[str, Any],
    actions: tuple[DialogueAction, ...],
) -> None:
    for action in actions:
        state["case"] = apply_action(state["case"], action)
    captured = [action for action in actions if action.intent == "answer"]
    primary = actions[0]
    extra = (
        f" I also preserved {len(captured) - 1} other explicit decision fact(s) from that answer."
        if len(captured) > 1
        else ""
    )
    state["messages"].append(
        {
            "role": "assistant",
            "content": f"{primary.acknowledgement}{extra}\n\n{primary.guidance}",
            "model_id": primary.model_id,
        }
    )
    state["report"] = service.decide_if_ready(product_id, state["case"].values)
    state["pending_turn"] = None


def _render_decision_position(
    case: CaseKnowledgeAsset,
    questions: tuple[Question, ...],
    next_question: Question | None,
) -> None:
    question_map = {question.question_id: question for question in questions}
    st.markdown('<div class="cs-section">Live decision position</div>', unsafe_allow_html=True)
    established = len(case.values)
    st.metric("Analysis depth", f"{established}/{len(questions)}")
    if next_question:
        st.markdown("**Next analytical issue**")
        st.write(next_question.prompt)
    if case.facts:
        st.markdown("**What I understand**")
        for fact in case.facts:
            label = _display_label(fact.question_id)
            if fact.status in {"confirmed", "estimated"}:
                value = _display_value(fact.question_id, fact.value)
                st.caption(f"✓ {label}: {value} · {fact.status}")
            else:
                st.caption(f"○ {label}: {fact.status}")
    else:
        st.caption("No canonical facts yet. Start by describing the decision in your own words.")
    if case.unresolved_ids:
        st.markdown("**Visible uncertainty**")
        for question_id in case.unresolved_ids:
            st.caption(f"• {question_map[question_id].prompt}")
    st.markdown("**Authority boundary**")
    st.caption(
        "Conversation may interpret and challenge. Only validated facts enter the case; the "
        "versioned product engine owns every score and verdict."
    )


def _render_consultant(product_id: str, service: DecisionStudio) -> None:
    state = _consultation(product_id)
    case: CaseKnowledgeAsset = state["case"]
    answers = case.values
    questions = service.questions(product_id)
    answered = len(answers)
    next_question = (
        None
        if state["report"] is not None
        else service.next_question(product_id, answers, case.unresolved_ids)
    )
    use_browser = st.toggle(
        "Private browser conversation",
        value=st.session_state.browser_expert_enabled.get(product_id, False),
        key=f"browser-model-{product_id}",
        help=(
            "Optional Apache-2.0 open-weight model inference runs on this device through WebGPU. "
            "No provider key is used and every proposed action is validated by the application."
        ),
    )
    st.session_state.browser_expert_enabled[product_id] = use_browser
    st.progress(
        answered / len(questions), text=f"Decision brief: {answered}/{len(questions)} established"
    )
    conversation, position = st.columns([1.8, 1], gap="large")
    with position, st.container(border=True):
        _render_decision_position(case, questions, next_question)
    with conversation:
        if not state["messages"]:
            with st.chat_message("assistant"):
                st.write(
                    "Tell me what decision you are facing in your own words. You do not need to "
                    "have every answer: you can say ‘I don’t know’, ask why something matters, or "
                    "change your mind. I’ll build the decision position with you without inventing "
                    "missing facts."
                )
        for message in state["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message.get("model_id"):
                    st.caption(f"Private browser wording · {message['model_id']}")

        pending = state.get("pending_turn")
        if use_browser:
            registry = ModelRegistry.from_file(ROOT / "factory" / "model_registry.json")
            model = registry.resolve_browser("conversation")
            request = None
            if pending:
                request = {
                    "request_id": pending["request_id"],
                    "payload": pending["payload"],
                }
            component = browser_expert(
                model_id=model.runtime_name,
                request=request,
                key=f"browser-expert-{product_id}",
            )
            returned = getattr(component, "turn", None)
            if pending and returned and returned.get("request_id") == pending["request_id"]:
                try:
                    raw = json.loads(returned["raw"])
                    action = validate_model_action(raw, pending["question"], returned["model_id"])
                except (KeyError, TypeError, ValueError, json.JSONDecodeError):
                    action = deterministic_action(pending["text"], pending["question"])
                action = guard_repeated_narrative(case, action, pending["question"])
                _complete_dialogue_action(product_id, service, state, action)
                st.rerun()
            if pending and st.button(
                "Continue now with governed fallback",
                key=f"fallback-{product_id}-{pending['request_id']}",
                width="stretch",
            ):
                action = deterministic_action(pending["text"], pending["question"])
                action = guard_repeated_narrative(case, action, pending["question"])
                _complete_dialogue_action(product_id, service, state, action)
                st.rerun()
        elif pending:
            actions = deterministic_actions(pending["text"], pending["question"], questions)
            _complete_dialogue_actions(product_id, service, state, actions)
            st.rerun()

        if next_question:
            with st.chat_message("assistant"):
                st.markdown(f"**{next_question.prompt}**")
                st.caption(f"How to think about it: {next_question.expert_context}")
                if next_question.options:
                    st.caption(
                        "You can answer conversationally. Useful reference points: "
                        + " · ".join(next_question.options)
                    )
            user_text = st.chat_input(
                "Answer naturally, ask why, or say ‘I don’t know’…",
                key=f"consultant-chat-{product_id}",
            )
            if user_text:
                state["messages"].append({"role": "user", "content": user_text})
                if next_question.answer_type == "text":
                    actions = deterministic_actions(user_text, next_question, questions)
                    actions = (
                        guard_repeated_narrative(case, actions[0], next_question),
                        *actions[1:],
                    )
                    _complete_dialogue_actions(product_id, service, state, actions)
                    st.rerun()
                request_id = f"{product_id}-{len(state['messages'])}"
                state["pending_turn"] = {
                    "request_id": request_id,
                    "text": user_text,
                    "question": next_question,
                    "payload": browser_prompt(user_text, next_question, case),
                }
                st.rerun()
        elif state["report"] is not None:
            st.success(
                "I have your verdict ready. The leading move is stable under the remaining "
                "bounded uncertainty."
            )
            if st.button("Rebuild assessment", width="stretch"):
                state["report"] = service.decide_if_ready(product_id, answers)
                st.rerun()
        else:
            st.warning(
                "We have covered every issue, but some material facts remain unknown or deferred. "
                "The application will not manufacture a verdict. Resolve them in the Decision "
                "Brief when evidence becomes available."
            )


def _render_brief(product_id: str, service: DecisionStudio) -> None:
    state = _consultation(product_id)
    case: CaseKnowledgeAsset = state["case"]
    questions = {question.question_id: question for question in service.questions(product_id)}
    st.subheader("Canonical Case Knowledge Asset")
    st.caption(
        "Confirmed facts—not the conversational transcript—are evaluated. Every revision is "
        "preserved for this anonymous session."
    )
    if not case.facts:
        st.info("Begin the consultant conversation to create the brief.")
        return
    for fact in case.facts:
        key = fact.question_id
        value = fact.value
        with st.container(border=True):
            st.markdown(
                f'<div class="cs-section">{questions[key].prompt}</div>', unsafe_allow_html=True
            )
            if fact.status not in {"confirmed", "estimated"}:
                st.markdown(f"**{fact.status.replace('_', ' ').title()}**")
                st.caption("No value is assumed by the Decision Engine.")
            elif key.endswith("_inr"):
                st.markdown(f"**{_format_inr(float(value))}**")
                st.caption(f"{fact.status.title()} · source: {fact.source}")
            else:
                st.markdown(f"**{value}**")
                st.caption(f"{fact.status.title()} · source: {fact.source}")
    with st.expander("Resolve or revise a case fact"):
        revision_key = st.selectbox(
            "Fact to revise",
            tuple(case.fact_map),
            format_func=lambda key: questions[key].prompt,
            key=f"revision-field-{product_id}",
        )
        existing = case.fact_map[revision_key]
        revised_value = _answer_widget(
            questions[revision_key],
            key_prefix=f"revision-{len(case.revisions)}",
            initial_value=existing.value,
        )
        if st.button("Preserve revision and reassess", key=f"revise-{product_id}"):
            state["case"] = case.confirm(
                revision_key, revised_value, reason="User revised a confirmed fact"
            )
            state["report"] = service.decide_if_ready(product_id, state["case"].values)
            st.rerun()
    if case.revisions:
        with st.expander(f"Revision history · {len(case.revisions)}"):
            st.dataframe(
                [
                    {
                        "Revision": item.revision,
                        "Fact": _display_label(item.question_id),
                        "Previous": _display_value(item.question_id, item.previous_value),
                        "Current": _display_value(item.question_id, item.new_value),
                        "Status": f"{item.previous_status} → {item.new_status}",
                    }
                    for item in case.revisions
                ],
                width="stretch",
                hide_index=True,
            )
    if st.button("Start this consultation again", type="secondary"):
        st.session_state.consultations[product_id] = {
            "case": case.reset(),
            "messages": [],
            "report": None,
            "pending_turn": None,
            "report_messages": [],
        }
        st.session_state.narratives.pop(product_id, None)
        st.rerun()


def _render_option(option: Any, rank: int) -> None:
    with st.container(border=True):
        st.markdown(f"### {rank}. {option.title}")
        st.caption(option.fit)
        for reason in option.reasons:
            st.markdown(f"- {reason}")
        if option.metrics:
            with st.expander("Numbers behind this option"):
                st.dataframe(
                    _display_rows({"decision fit score": option.score} | option.metrics),
                    width="stretch",
                    hide_index=True,
                )
        with st.expander("Risks and evidence"):
            st.markdown("**Risks**")
            for risk in option.risks:
                st.markdown(f"- {risk}")
            st.markdown("**Evidence**")
            for evidence in option.evidence:
                st.markdown(f"- {evidence}")


def _secret(name: str) -> str | None:
    configured = os.getenv(name)
    if configured:
        return configured
    try:
        return str(st.secrets[name]) if name in st.secrets else None
    except Exception:
        return None


def _render_narrative(product_id: str, report: DecisionReport) -> None:
    st.markdown("### Ask the open-model consultant to challenge the result")
    st.caption(
        "Optional: this sends the structured brief and deterministic report to a hosted "
        "open-weight "
        "model. It cannot change the verdict or scores."
    )
    key = _secret("GROQ_API_KEY")
    if not key:
        st.info(
            "Hosted explanation is not configured. The complete deterministic report "
            "remains available."
        )
        return
    consent = st.checkbox(
        "I consent to send this consultation and result for one hosted inference call"
    )
    if consent and st.button("Generate consultant challenge", width="stretch"):
        registry = ModelRegistry.from_file(ROOT / "factory" / "model_registry.json")
        model = registry.resolve_hosted("recommendation")
        try:
            generated_narrative = narrate(
                report, load_skill(ROOT, product_id), GroqProvider(key), model.runtime_name
            )
        except (ValueError, RuntimeError, json.JSONDecodeError) as exc:
            st.warning(
                "The optional narrator is resting. Your deterministic result is unaffected. "
                f"({exc})"
            )
        else:
            st.session_state.narratives[product_id] = generated_narrative
            st.rerun()
    narrative: ConsultantNarrative | None = st.session_state.narratives.get(product_id)
    if narrative:
        st.success(narrative.executive_summary)
        st.markdown(f"**The consultant's challenge:** {narrative.challenge}")
        for question in narrative.questions:
            st.markdown(f"- {question}")
        st.caption(f"Model {narrative.model_id} · prompt {narrative.prompt_hash[:12]}")


def _render_result(product_id: str) -> None:
    report: DecisionReport | None = _consultation(product_id)["report"]
    if report is None:
        st.info("Complete the consultation to unlock the assessment.")
        return
    st.markdown(
        f'<div class="cs-verdict"><div class="cs-section">Verdict</div><h2>{report.verdict}</h2>'
        f"<p>{report.summary}</p></div>",
        unsafe_allow_html=True,
    )
    st.subheader("So what should you do?")
    st.success(report.next_actions[0])
    st.subheader("Your three best moves")
    for rank, option in enumerate(report.options, start=1):
        _render_option(option, rank)
    left, right = st.columns(2, gap="large")
    with left:
        st.subheader("Do next")
        for action in report.next_actions:
            st.markdown(f"- {action}")
        st.subheader("Principal risks")
        for risk in report.risks:
            st.markdown(f"- {risk}")
    with right:
        st.subheader("What would change this verdict?")
        for condition in report.change_conditions:
            st.markdown(f"- {condition}")
        st.subheader("Assumptions")
        for assumption in report.assumptions:
            st.markdown(f"- {assumption}")
    with st.expander("Decision provenance and evidence", expanded=False):
        st.code(report.gka_artifact_id)
        st.caption(f"GKA SHA-256 `{report.gka_hash}`")
        for evidence in report.evidence:
            st.markdown(f"- {evidence}")
    st.download_button(
        "Download complete decision report",
        json.dumps(report.to_dict(), ensure_ascii=False, indent=2),
        file_name=f"{product_id}-decision-report.json",
        mime="application/json",
        width="stretch",
    )
    st.download_button(
        "Download plain-English decision report",
        report_to_markdown(report),
        file_name=f"{product_id}-decision-report.md",
        mime="text/markdown",
        width="stretch",
    )
    with st.expander("Technical decision identity", expanded=False):
        metrics = st.columns(4)
        metrics[0].metric("Decision score", f"{report.score:.1f}/100")
        metrics[1].metric("Confidence", report.confidence)
        metrics[2].metric("GKA effective", report.gka_effective_date)
        metrics[3].metric("Policy", report.policy_version)
        st.caption(report.data_sufficiency)
    st.subheader("Ask your consultant about this decision")
    st.caption(
        "Unpack the frozen report gradually. Follow-up answers retrieve only evidence already "
        "inside this decision; they cannot silently change the verdict."
    )
    state = _consultation(product_id)
    for message in state["report_messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    follow_up = st.chat_input(
        "Ask why, explore a risk, compare alternatives or request evidence…",
        key=f"report-chat-{product_id}",
    )
    if follow_up:
        state["report_messages"].append({"role": "user", "content": follow_up})
        state["report_messages"].append(
            {"role": "assistant", "content": answer_report_question(report, follow_up)}
        )
        st.rerun()
    _render_narrative(product_id, report)


def _render_knowledge(product_id: str) -> None:
    rows, manifest = load_current_gka(ROOT, product_id)
    atlas = load_decision_atlas(ROOT, product_id)
    catalog = load_metric_catalog(ROOT, product_id)
    metrics_catalog = catalog["metrics"]
    available = sum(item["coverage"] == "available" for item in metrics_catalog)
    st.subheader("Grand Knowledge Asset · Decision coverage")
    st.warning(
        "The asset distinguishes available evidence from required-but-missing evidence. Coverage "
        "is expanded only through governed sources; unavailable facts are never invented."
    )
    cols = st.columns(4)
    cols[0].metric("Decision metrics", len(metrics_catalog))
    cols[1].metric("Currently available", available)
    cols[2].metric("Evidence coverage", f"{available / len(metrics_catalog):.0%}")
    cols[3].metric("GKA effective", manifest["effective_date"])
    st.subheader("Precomputed Decision Universe")
    st.write(
        "Before any customer conversation begins, every covered option is feature-engineered, "
        "scenario-tested, pathway-classified and checked for robust frontier membership. The "
        "consultation retrieves from this frozen universe; it does not invent research live."
    )
    atlas_cols = st.columns(3)
    atlas_cols[0].metric("Options processed upfront", atlas["universe_size"])
    atlas_cols[1].metric("Robust frontier", len(atlas["frontier_ids"]))
    atlas_cols[2].metric("Atlas schema", atlas["schema_version"])
    with st.expander("Growth / stable / decline pathway atlas", expanded=True):
        st.dataframe(
            [
                {
                    "Option": item["option_name"],
                    "Decision segment": item["segment"],
                    "Pathway": item["pathway"],
                    "Pathway score": item["pathway_score"],
                    "Robust frontier": item["record_id"] in atlas["frontier_ids"],
                }
                for item in atlas["entries"]
            ],
            width="stretch",
            hide_index=True,
        )
    with st.expander("Decision metric catalog", expanded=True):
        st.dataframe(
            [
                {
                    "Metric": item["label"],
                    "Decision use": item["decision_use"],
                    "Coverage": item["coverage"].replace("_", " ").title(),
                    "Freshness": item["freshness"],
                    "Preferred source": item["preferred_source"],
                }
                for item in metrics_catalog
            ],
            width="stretch",
            hide_index=True,
        )
    st.subheader("Current governed observations")
    st.dataframe(rows, width="stretch", hide_index=True)
    with st.expander("Artifact identity"):
        st.dataframe(_display_rows(manifest), width="stretch", hide_index=True)


def _workspace(product_id: str) -> None:
    product = PRODUCTS[product_id]
    service = DecisionStudio(ROOT)
    top_left, top_right = st.columns([5, 1])
    top_left.markdown(f"## {product.icon} {product.name}")
    top_left.caption(product.promise)
    if top_right.button("All services", width="stretch"):
        st.session_state.selected_product = None
        st.rerun()
    consult_tab, brief_tab, result_tab, knowledge_tab, method_tab = st.tabs(
        ["Consultant", "Decision Brief", "Recommendation", "Knowledge Asset", "Method"]
    )
    with consult_tab:
        _render_consultant(product_id, service)
    with brief_tab:
        _render_brief(product_id, service)
    with result_tab:
        _render_result(product_id)
    with knowledge_tab:
        _render_knowledge(product_id)
    with method_tab:
        st.subheader("Governed decision skill")
        st.markdown(load_skill(ROOT, product_id))
        st.info(
            "Deterministic code owns the verdict. Optional model intelligence can explain and "
            "challenge only after the result is frozen."
        )


def main() -> None:
    st.set_page_config(page_title="ConSaaS Core", page_icon="◇", layout="wide")
    _install_theme()
    _init()
    _header()
    if st.session_state.selected_product is None:
        _landing()
    else:
        _workspace(st.session_state.selected_product)
    st.divider()
    st.caption(
        "Decision support only—not financial, legal, admission, property-valuation or investment "
        "advice. Anonymous session; no durable personal-data storage in this release."
    )

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
from decision_studio.catalog import PRODUCTS, load_current_gka, load_skill
from decision_studio.narrator import ConsultantNarrative, narrate
from decision_studio.service import DecisionStudio
from plugin_sdk.decision import DecisionReport, Question

APP_VERSION = "0.1.1"
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
        f"Decision Studio Foundation v{APP_VERSION} · Explainable by design · No paid AI required"
    )


def _landing() -> None:
    st.markdown(
        '<div class="cs-promise">Choose the decision you need to make—not the tool '
        "you want to use.</div>",
        unsafe_allow_html=True,
    )
    st.write(
        "Each consultant asks only the questions needed to construct a canonical decision brief, "
        "then evaluates it against governed knowledge and a versioned methodology."
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
                  <span class="cs-foundation">GKA v0.1 Foundation</span>
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
            "Model-assisted explanation",
            "Evidence trail",
        ),
        (
            "The structured brief—not chat history—is the source of truth.",
            "Rules, constraints and scores are replayable and versioned.",
            "An open-weight model may explain; it cannot rewrite the decision.",
            "Every result identifies asset, policy, assumptions and limitations.",
        ),
        strict=True,
    ):
        with column:
            st.markdown(f"**{title}**")
            st.caption(body)
    st.warning(
        "Foundation coverage is intentionally small and illustrative. Verify current programme, "
        "property and venture evidence before making a consequential commitment."
    )


def _consultation(product_id: str) -> dict[str, Any]:
    consultations = st.session_state.consultations
    if product_id not in consultations:
        consultations[product_id] = {"answers": {}, "messages": [], "report": None}
    return cast(dict[str, Any], consultations[product_id])


def _answer_widget(question: Question) -> Any:
    key = f"answer-{st.session_state.selected_product}-{question.question_id}"
    if question.answer_type == "choice":
        return st.selectbox("Your answer", question.options, key=key, label_visibility="collapsed")
    return st.number_input(
        "Your answer",
        min_value=question.minimum,
        max_value=question.maximum,
        value=question.default,
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


def _render_consultant(product_id: str, service: DecisionStudio) -> None:
    state = _consultation(product_id)
    questions = service.questions(product_id)
    answered = len(state["answers"])
    st.progress(
        answered / len(questions), text=f"Decision brief: {answered}/{len(questions)} established"
    )
    if not state["messages"]:
        with st.chat_message("assistant"):
            st.write(
                "I will build this decision one constraint at a time. I will not force a verdict "
                "when the evidence is too thin."
            )
    for message in state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if answered < len(questions):
        question = questions[answered]
        with st.chat_message("assistant"):
            st.markdown(f"**{question.prompt}**")
            st.caption("This answer becomes part of your canonical decision brief.")
        with st.form(f"question-{product_id}-{question.question_id}"):
            answer = _answer_widget(question)
            submitted = st.form_submit_button(
                "Preserve answer and continue", type="primary", width="stretch"
            )
        if submitted:
            state["answers"][question.question_id] = answer
            shown = (
                f"₹{float(answer):,.0f}" if question.question_id.endswith("_inr") else str(answer)
            )
            state["messages"].extend(
                [
                    {"role": "user", "content": shown},
                    {
                        "role": "assistant",
                        "content": "Understood. I have preserved that constraint.",
                    },
                ]
            )
            if len(state["answers"]) == len(questions):
                state["report"] = service.decide(product_id, state["answers"])
            st.rerun()
    else:
        st.success("Your decision brief is complete. The deterministic assessment is ready.")
        if st.button("Rebuild assessment", width="stretch"):
            state["report"] = service.decide(product_id, state["answers"])
            st.rerun()


def _render_brief(product_id: str, service: DecisionStudio) -> None:
    state = _consultation(product_id)
    questions = {question.question_id: question for question in service.questions(product_id)}
    st.subheader("Canonical decision brief")
    st.caption("This structured asset—not the conversational transcript—is evaluated.")
    if not state["answers"]:
        st.info("Answer the first consultant question to begin the brief.")
        return
    for key, value in state["answers"].items():
        with st.container(border=True):
            st.markdown(
                f'<div class="cs-section">{questions[key].prompt}</div>', unsafe_allow_html=True
            )
            if key.endswith("_inr"):
                st.markdown(f"**₹{float(value):,.0f}**")
            else:
                st.markdown(f"**{value}**")
    if st.button("Start this consultation again", type="secondary"):
        st.session_state.consultations[product_id] = {"answers": {}, "messages": [], "report": None}
        st.session_state.narratives.pop(product_id, None)
        st.rerun()


def _render_option(option: Any, rank: int) -> None:
    with st.container(border=True):
        top, metric = st.columns([4, 1])
        top.markdown(f"### {rank}. {option.title}")
        top.caption(option.fit)
        metric.metric("Fit score", f"{option.score:.1f}")
        for reason in option.reasons:
            st.markdown(f"- {reason}")
        if option.metrics:
            with st.expander("Numbers behind this option"):
                st.dataframe(
                    _display_rows(option.metrics), width="stretch", hide_index=True
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
    metrics = st.columns(4)
    metrics[0].metric("Decision score", f"{report.score:.1f}/100")
    metrics[1].metric("Confidence", report.confidence)
    metrics[2].metric("GKA effective", report.gka_effective_date)
    metrics[3].metric("Policy", report.policy_version)
    st.caption(report.data_sufficiency)
    st.subheader("Ranked options")
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
    _render_narrative(product_id, report)


def _render_knowledge(product_id: str) -> None:
    rows, manifest = load_current_gka(ROOT, product_id)
    st.subheader("Grand Knowledge Asset · Foundation")
    st.warning(
        "This is a small governed seed asset, not exhaustive market coverage. Use it to structure "
        "a decision and identify diligence—not as current transactional truth."
    )
    cols = st.columns(4)
    cols[0].metric("Records", manifest["row_count"])
    cols[1].metric("Effective", manifest["effective_date"])
    cols[2].metric("Quality", manifest["quality_state"].title())
    cols[3].metric("Schema", manifest["schema_version"])
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
        "advice. Anonymous session; no durable personal-data storage in this Foundation release."
    )

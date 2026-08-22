"""Opt-in provider-free browser inference component for governed dialogue actions."""

from __future__ import annotations

from typing import Any

import streamlit as st

_COMPONENT_HTML = """
<div class="browser-card">
  <div class="browser-row">
    <div>
      <strong>Private browser expert</strong>
      <div id="status">Checking this device…</div>
    </div>
    <button id="enable" type="button">Enable on this device</button>
  </div>
  <div class="progress"><span id="bar"></span></div>
  <small id="detail">No model is downloaded until you choose Enable.</small>
</div>
"""

_COMPONENT_CSS = """
.browser-card { border:1px solid var(--st-border-color); border-radius:12px; padding:.8rem 1rem;
  background:color-mix(in srgb, var(--st-secondary-background-color) 70%, white); }
.browser-row { display:flex; align-items:center; justify-content:space-between; gap:1rem; }
#status, #detail { color:var(--st-text-color); opacity:.72; font-size:.82rem; margin-top:.15rem; }
#enable { border:0; border-radius:8px; padding:.45rem .75rem; color:white;
  background:var(--st-primary-color); cursor:pointer; font-weight:650; white-space:nowrap; }
#enable:disabled { cursor:not-allowed; opacity:.55; }
.progress { height:4px; background:var(--st-secondary-background-color); border-radius:999px;
  overflow:hidden; margin:.65rem 0 .4rem; }
#bar { display:block; height:100%; width:0; background:var(--st-primary-color);
  transition:width .2s; }
"""

_COMPONENT_JS = r"""
const CDN = "https://cdn.jsdelivr.net/npm/@mlc-ai/web-llm@0.2.84/+esm";

export default function(component) {
  const {data, key, parentElement, setStateValue, setTriggerValue} = component;
  const status = parentElement.querySelector("#status");
  const detail = parentElement.querySelector("#detail");
  const button = parentElement.querySelector("#enable");
  const bar = parentElement.querySelector("#bar");
  globalThis.__consaasBrowserExperts ??= {};
  const runtime = globalThis.__consaasBrowserExperts[key] ??= {
    engine: null, loading: false, processed: null, model: null
  };

  function show(message, extra="", progress=null) {
    status.textContent = message;
    detail.textContent = extra;
    if (progress !== null) bar.style.width = `${Math.max(0, Math.min(1, progress)) * 100}%`;
  }

  async function processRequest() {
    const request = data?.request;
    if (!runtime.engine || !request || runtime.processed === request.request_id) return;
    runtime.processed = request.request_id;
    button.disabled = true;
    show(
      "Thinking privately in your browser…",
      "No provider token or application secret is used.", 1
    );
    try {
      const system = `You are the conversational interpretation layer of a high-stakes advisory
system. The deterministic application owns facts and decisions. Interpret only the current user
message against the supplied current question. Never invent a number, option, fact, score, verdict,
evidence or recommendation. Return one JSON object with exactly intent, question_id, value,
acknowledgement and guidance. intent must be answer, unknown, uncertain, defer, confused, explain or
discuss. For answer, value must exactly satisfy the supplied type/options/bounds. For all other
intents value must be null. Keep acknowledgement and guidance warm, concise and grounded only in the
payload.`;
      const completion = await runtime.engine.chat.completions.create({
        messages: [
          {role: "system", content: system},
          {role: "user", content: JSON.stringify(request.payload)}
        ],
        temperature: 0.15,
        max_tokens: 260,
        response_format: {type: "json_object"}
      });
      const raw = completion?.choices?.[0]?.message?.content;
      if (!raw) throw new Error("The browser model returned no dialogue action.");
      setTriggerValue("turn", {
        request_id: request.request_id,
        model_id: runtime.model,
        raw: raw
      });
      show("Private browser expert is ready", "The proposed action is being validated.", 1);
    } catch (error) {
      runtime.processed = null;
      setTriggerValue("failure", {
        request_id: request.request_id,
        message: String(error?.message ?? error)
      });
      show("Browser inference could not complete", "Use the governed fallback below.", 0);
    } finally {
      button.disabled = false;
    }
  }

  async function enable() {
    if (runtime.engine || runtime.loading) {
      await processRequest();
      return;
    }
    if (!navigator.gpu) {
      show("WebGPU is unavailable", "The governed conversation remains fully usable.", 0);
      setStateValue("capability", "unsupported");
      button.disabled = true;
      return;
    }
    runtime.loading = true;
    button.disabled = true;
    try {
      const webllm = await import(CDN);
      runtime.model = data.model_id;
      runtime.engine = await webllm.CreateMLCEngine(runtime.model, {
        initProgressCallback: report => show(
          "Preparing the private browser expert…", report.text ?? "Downloading model assets",
          report.progress ?? 0
        )
      });
      setStateValue("capability", "ready");
      show("Private browser expert is ready", "Model assets are cached by this browser.", 1);
      button.textContent = "Enabled";
      await processRequest();
    } catch (error) {
      runtime.engine = null;
      setStateValue("capability", "failed");
      show("This device could not load the model", String(error?.message ?? error), 0);
      button.textContent = "Try again";
    } finally {
      runtime.loading = false;
      button.disabled = false;
    }
  }

  button.onclick = enable;
  if (!navigator.gpu) {
    show("WebGPU is unavailable", "The governed conversation remains fully usable.", 0);
    button.disabled = true;
  } else if (runtime.engine) {
    button.textContent = "Enabled";
    show("Private browser expert is ready", "Inference stays on this device.", 1);
    void processRequest();
  } else {
    show("Compatible browser detected", "Enable once to download and cache the model.", 0);
  }
}
"""

_browser_expert = st.components.v2.component(
    "consaas_browser_expert",
    html=_COMPONENT_HTML,
    css=_COMPONENT_CSS,
    js=_COMPONENT_JS,
)


def _noop() -> None:
    """Allow the component to declare governed state and trigger names."""


def browser_expert(*, model_id: str, request: dict[str, Any] | None, key: str) -> Any:
    """Mount the browser runtime; returned model text remains untrusted."""
    return _browser_expert(
        key=key,
        default={"capability": "unknown"},
        data={"model_id": model_id, "request": request},
        on_capability_change=_noop,
        on_turn_change=_noop,
        on_failure_change=_noop,
    )

# Conversational Decision Intelligence v0.3

Status: Implemented for review
Effective: 2026-08-23

## Outcome

Decision Studio now treats conversation as the primary way to build a case. Users may narrate a
problem, answer in ordinary language, ask why, express confusion, defer an issue or explicitly say
that they do not know. Guided controls remain available as an accessibility and deterministic
fallback path.

The release establishes a governed collaboration:

`Conversation -> typed action -> validation -> Case Knowledge Asset -> product engine -> result`

The model does not become the decision engine.

## Decision Position

The Consultant tab shows a live Decision Position containing established facts, unresolved
uncertainty, analysis depth and the next analytical issue. Facts carry an epistemic status:

- `confirmed`: supplied or explicitly selected by the user;
- `estimated`: an explicit working estimate accepted by the user;
- `inferred`: a model or rule hypothesis, not decision-ready in this release;
- `unknown`: the user does not currently know;
- `uncertain`: the user is not confident enough to confirm;
- `deferred`: intentionally postponed.

Only confirmed and estimated values may enter a deterministic product engine.

## Browser intelligence profile

The optional private browser profile uses WebLLM 0.2.84 and the prebuilt
`SmolLM2-1.7B-Instruct-q4f16_1-MLC` profile. The upstream model is Apache-2.0 licensed. A compatible
WebGPU browser is required. No model is downloaded until the user explicitly enables it; model
assets are then cached by the browser where supported.

The browser model receives only the current user message, current governed question and compact
case values. It proposes exactly one typed dialogue action. Python validates the action name,
question identity, answer type, permitted choices, numeric bounds and required wording before any
state change. Invalid, unavailable or failed inference falls back to the deterministic interpreter.

## Privacy boundary

The public release stores the case only in the anonymous Streamlit session. Browser inference does
not send consultation content to an LLM provider. Enabling it downloads public runtime/model assets
from the pinned jsDelivr package URL and the WebLLM-configured model host, which necessarily exposes
ordinary network metadata to those asset hosts. It must not be represented as offline before assets
are cached or as universally compatible.

## Known limitations

- Browser inference quality and speed depend on the user's device and browser.
- The approximately 1.7B-parameter profile is a conversational interpreter, not the source of
  international-advisory expertise.
- The deterministic fallback recognises governed options and common uncertainty language; it does
  not claim general natural-language understanding.
- This release does not implement CareerSim cash-flow simulation, Pareto search, calibrated outcome
  probabilities or the full value-of-information engine proposed for later increments.
- The WebLLM JavaScript runtime is pinned but loaded from a third-party CDN in this bounded release;
  self-hosting the reviewed bundle is a production-hardening candidate.

## Rollback

Revert the v0.3 release commit. No promoted GKA pointer, policy or product-engine artifact is
rewritten, so the v0.2 application path remains compatible.

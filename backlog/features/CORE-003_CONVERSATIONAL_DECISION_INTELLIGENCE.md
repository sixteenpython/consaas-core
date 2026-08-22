---
id: CORE-003
mode: RELEASE
status: REVIEW
product: core
type: vertical-slice feature
owner: product-owner
created: 2026-08-23
dependencies: [CORE-002]
---

# Conversational Decision Intelligence

## User outcome

A user can describe a high-stakes decision in ordinary language, answer or revise questions without
being forced into a form, say that they do not know or are confused, and watch a governed Decision
Position develop. An optional Apache-2.0 browser model makes the dialogue more natural without
owning canonical facts, calculations, rankings or verdicts.

## Bounded release scope

CareerSim is the reference journey. The shared conversational and epistemic-state contracts remain
usable by HouseWise and StartupEval, but this release does not replace their domain engines or claim
that a small browser model is a consulting authority.

## Acceptance criteria

1. Free-form conversation is the primary consultant input; guided choices remain optional.
2. `unknown`, `uncertain`, `estimated` and `deferred` are valid case states and are visible.
3. “I don't know”, “I am confused”, “why are you asking?” and supported natural answers have safe,
   useful deterministic behavior.
4. Model-proposed dialogue actions are typed, schema/domain validated and cannot silently persist.
5. An opt-in browser WebGPU profile can interpret and word a turn without a provider key.
6. The Decision Position shows established facts, unresolved uncertainty and the next analytical
   issue throughout the conversation.
7. The same report is produced with browser inference enabled or disabled.
8. Unsupported devices and model failures retain the complete deterministic journey.
9. Unit, integration, UI, evaluation, architecture, privacy and production smoke gates pass.

## Explicit exclusions

- No claim of universally unlimited inference or universal browser compatibility.
- No server-side GPU, local Ollama requirement, paid inference dependency or autonomous agent.
- No new CareerSim cash-flow simulator, calibrated probability or outcome-learning engine.
- No durable personal-data persistence in this anonymous public release.

## Rollback

Revert the CORE-003 release commit. Existing v0.2 question, case, policy and GKA artifacts remain
compatible and are not rewritten.

# ADR-CORE-003: Govern free-form browser conversation around deterministic authority

Status: Accepted
Date: 2026-08-23

## Decision

Make free-form chat the primary Decision Studio consultation interface. Introduce epistemic case
states and a typed `DialogueAction` validation boundary. Permit an explicitly enabled,
Apache-2.0-licensed WebLLM model to run inside a compatible user's browser for turn interpretation
and wording. Browser output is untrusted, cannot call domain engines directly and cannot persist a
fact until schema and domain validation succeed.

The deterministic consultation remains a first-class path. Product decision engines retain sole
authority over calculations, scores, rankings and verdicts. The browser model is downloaded only
after consent, remains device-dependent and is never described as universally available or as the
source of the recommendation.

## Why

The v0.2 consultation established safe authority boundaries but exposed them as a questionnaire.
High-stakes advisory requires natural problem narration, uncertainty handling and explanation.
Provider-free browser inference can improve that experience without requiring ConSaaS or its
customer to operate GPU infrastructure, while the deterministic path preserves accessibility and
reliability.

## Alternatives rejected

- LLM-owned case memory or verdicts: weakens replay, evidence and safety.
- Mandatory paid/free-hosted API: introduces quota, privacy and availability dependencies.
- Mandatory Ollama or customer inference hardware: conflicts with the approved hardware boundary.
- Browser model as the only interface: excludes unsupported and resource-constrained devices.
- Immediate frontend rewrite: unnecessary before the vertical slice validates demand.

## Privacy and security

Browser-model payloads remain in the browser except for the validated typed action returned to the
existing anonymous Streamlit session. Component source is trusted repository code; untrusted user or
model content is passed as serialised data and is not interpolated into executable code. The model
runtime downloads public weights from the documented upstream host after user consent.

## Consequences

The model registry gains a browser provider profile. Case facts gain explicit epistemic status.
Model and deterministic turns share one validation and application boundary. Streamlit remains the
serving shell for this release; a separate frontend is deferred until measured product needs justify
it.

## Rollback

Revert the release commit. The v0.2 artifacts, product engines and GKA pointers are unchanged.

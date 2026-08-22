---
id: NARRATIVE-004
mode: RELEASE
status: REVIEW
product: narrative
type: vertical-slice feature
owner: product-owner
created: 2026-08-22
dependencies: [NARRATIVE-001-T01]
---

# Narrative Architect Foundation Alpha

## User outcome

An author can turn an idea into a structured three-scene screenplay foundation through guided
conversation, inspect the canonical Narrative Knowledge Asset, revise it, undo changes, compile a
bounded Fountain draft, and export/reload the complete project.

## Included

- minimum versioned NKA domain spine;
- deterministic NKA-gap conversation guide;
- premise/theme/conflict/stakes/ending knowledge view;
- character and scene editors;
- immutable revision history and undo-as-new-revision;
- deterministic bounded Fountain compilation and readiness report;
- lossless JSON project export/import;
- Streamlit Create workspace, demonstration project, privacy/release disclosures;
- hosted-demo and local-private profiles from ADR-NA-011.

## Excluded

LLM inference, Ollama, screenplay PDF upload, Doctor mode, SDI/iMaSc scoring, durable hosted storage,
authentication, collaboration, PDF compilation, and claims of screenplay quality or film success.

## Acceptance criteria

1. Conversation guidance is derived from the NKA head, never from chat history.
2. Every accepted mutation produces a new immutable revision and rejects stale writes.
3. Undo creates a descendant revision without deleting history.
4. Export/import preserves the project head and every revision.
5. Identical NKA revisions compile to identical bounded Fountain text.
6. The Streamlit workflow supports idea -> NKA -> characters/scenes -> compile/download.
7. Hosted mode uses no secret, external LLM, durable content store, or screenplay upload.
8. Unit, integration, UI smoke, guardrail, lint, type, and security gates pass as applicable.

# Narrative Architect Changelog

## 0.2.0 — Screenplay Construction Studio

- Rebuilt the product around six author-approved construction phases.
- Added centre-knot suggestions, Booker basic-plot selection, and separate genre/tone controls.
- Added proposed character ensembles with playable objectives, contradictions, behavior, voice, and arcs.
- Added full-plot drafting through a governed skill with a deterministic hosted fallback.
- Added five screenplay structures, recommendations, and explicit story-event beat mapping.
- Added rich scene cards covering mini-conflict, change, behavior, blocking, and context/text/subtext.
- Added deterministic iMaSc construction-readiness scoring, structural coverage, and a build-complete gate.
- Added Fountain and evidence-facing Markdown scorecard compilation bound to one NKA revision.
- Added a loopback-only optional Ollama adapter; no screenplay content is sent to external inference.
- Migrated the canonical NKA to `alpha-2` while retaining import support for `alpha-1` project bundles.

## 0.1.0 — Foundation Alpha

- Added a guided Create workspace whose questions follow gaps in canonical narrative state.
- Added minimum story, character, and ordered-scene knowledge views.
- Added immutable in-session revision history, stale-write rejection, and restore-as-new-revision.
- Added tamper-checked project JSON export/import.
- Added deterministic readiness assessment and bounded Fountain compilation.
- Added hosted-demo privacy disclosure and a local-private runtime profile.
- Added domain, application, compiler, import/export, and Streamlit smoke tests.

Known limits: no LLM, durable database, PDF screenplay output/import, SDI/iMaSc analysis, Doctor mode,
authentication, or collaboration. Hosted-demo content is processed by the Streamlit host and must not
be confidential.

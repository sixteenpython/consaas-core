# MVP Scope

## Product promise

A single-user local application can develop a screenplay through expert conversation, maintain a coherent canonical NKA, compile a standard/bounded screenplay, import a born-digital PDF, diagnose it under SDI, and converse with evidence-linked findings.

## Foundation Alpha release boundary

The first public deployment is an architectural proving slice, not the full MVP described below. It
supports deterministic guided story development, a minimum NKA, character and scene editing,
immutable in-session revisions, portable JSON, and bounded Fountain compilation. It intentionally
excludes local LLM inference, durable server storage, PDF parsing, SDI/iMaSc diagnosis, and Doctor
mode. Hosted users are warned not to enter confidential screenplay material; the local profile is the
privacy-preserving path.

## Vertical Slice 1 — Create

**End-to-end:** create local project -> narrate idea -> expert asks/proposes -> structured NKA revisions -> inspect scenes/characters/plot -> revise/undo -> compiler readiness -> compile/download screenplay.

Included:

- one active project head with immutable history;
- premise/theme/plot/conflicts/stakes/characters/relationships/arcs/ordered scenes/dialogue/subtext;
- structured expert turn plans and NKA patches;
- confirmation for material generated content;
- deterministic standard and bounded-script compilation;
- local model health/profile selection;
- restart/reload continuity and project-local storage.

Not required: full SDI scoring, PDF import, collaborative branches/merge, FDX, OCR, autonomous full-script generation, embeddings if deterministic retrieval suffices.

## Vertical Slice 2 — Doctor

**End-to-end:** upload born-digital screenplay PDF -> parse/review -> candidate NKA -> confirm import -> SDI four-pillar scoring -> SIS/momentum -> findings/recommendations -> evidence drill-down -> grounded doctor conversation -> accepted revision -> recompile/reanalyze.

Included:

- deterministic page/block provenance and parse uncertainty;
- per-scene four-pillar `0–5`, total `/20`, mean `0–5`;
- named SDI momentum observations and graph;
- finding taxonomy and source navigation;
- stale-analysis detection and before/after comparison;
- no film-success prediction.

Not required: scanned/OCR PDFs, every screenplay format, biometric/drop-off prediction, learned audience model, genre-specific non-SDI scoring, automatic rewrite.

## Definition of done

- Runnable locally through documented one-command setup after models are installed.
- No screenplay content leaves the machine.
- Every mutation is revisioned and undoable.
- Every authoritative diagnostic claim has evidence.
- Deterministic computations are tested and reproducible.
- Local model entry and license are recorded.
- Both slices pass integration and headless UI smoke tests.
- Documentation reflects actual behavior and limitations.

## Product metrics

NKA correction rate, accepted/rejected proposal rate, continuity defects, compiler blockers, parse coverage, evidence coverage, SIS reviewer agreement, unsupported-claim rate, task completion, inference latency/memory, and percentage of recommendations that users can trace to source.

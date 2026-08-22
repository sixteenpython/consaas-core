# Narrative Architect Implementation Roadmap

Each increment begins by rereading its architecture documents and ends with implementation, tests, validation, diff review, documentation update, and a runnable application.

## Current proving release

Foundation Alpha v0.1.0 combines a deliberately narrow subset of Increments 1, 3, and 4 to validate
the user loop on a public Streamlit deployment without a model or secret. It does not mark those
increments complete. The production roadmap below remains authoritative.

## Increment 0 — Architecture approval

Approve Phase-1 documents, resolve open SDI scale/cadence labels, accept/revise ADRs, select supported MVP hardware profiles, and approve local-model/license candidates. No code.

## Increment 1 — Domain spine

Implement NKA v1 models, statement taxonomy, IDs/references, invariants, change sets, immutable revisions, SQLite/filesystem ports, and project commands/queries. Provide CLI/domain tests before UI.

**Exit:** create/revise/reload/undo a small story deterministically.

## Increment 2 — Local model and expert turn

Implement `LocalLLM`, Ollama adapter, registry, capability probe, structured-output validation, expert turn plan, context builder, and fake-model contract tests.

**Exit:** a conversation proposes validated changes without direct persistence access.

## Increment 3 — Create UI vertical slice

Add Streamlit shell, Create conversation, knowledge/scene/character inspectors, proposal diff/approval, open-question/gap view, and restart-safe state.

**Exit:** a user develops an ordered multi-scene bounded story through conversation.

## Increment 4 — Compiler

Implement readiness, standard/bounded profiles, deterministic document model, PDF/download rendering adapter, source map, and render/golden tests.

**Exit:** Vertical Slice 1 passes end-to-end and remains runnable without Doctor features.

## Increment 5 — PDF source and deterministic parser

Add secure local upload, immutable artifacts, layout blocks, grammar/state machine, source spans, review queue, correction workflow, and parser fixtures.

**Exit:** born-digital reference scripts parse with disclosed coverage and evidence navigation.

## Increment 6 — NKA import enrichment

Add local model ambiguity classification and narrative inference, confidence/evidence, alias resolution, candidate import diff, and confirmation.

**Exit:** parsed screenplay becomes a reviewed canonical NKA without source mutation.

## Increment 7 — SDI/SIS/momentum

Implement evidence packets, four-pillar assessments, deterministic SIS scales, momentum rules/graph, uncertainty, manifests, and expert-reviewed golden cases.

**Exit:** scores and observations are reproducible, labelled, and drillable.

## Increment 8 — Script Doctor and continuous loop

Implement findings, recommendation validator/prioritizer, doctor conversation tools, evidence drawer, recommendation-to-proposal, stale invalidation, recompile/reanalyze, and revision comparison.

**Exit:** Vertical Slice 2 and Create->Doctor->Revise loop pass end-to-end.

## Increment 9 — Hardening and MVP release

Privacy/security audit, failure injection, model/hardware benchmark, packaging, backups/deletion, accessibility, performance budgets, operator/user docs, and release evidence.

## Stop/go gates

Do not advance if canonical truth leaks into chat state, the model can write persistence, deterministic arithmetic differs across runs, source evidence cannot be resolved, unpublished text leaves local boundaries, or a model lacks documented distribution/use rights.

## Post-MVP candidates

FDX/Fountain, OCR, multilingual grammar, collaborative branching, embeddings/reranking, genre extensions, model fine-tuning, and advanced report exports. Each is beyond MVP; non-SDI narrative theories require explicit extension governance.

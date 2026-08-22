---
id: NARRATIVE-003
mode: BACKLOG
status: BACKLOG
product: narrative
type: feature
owner: unassigned
created: 2026-08-22
dependencies: [NARRATIVE-002-T01]
readiness: blocked-by-dependency
---

# Feature ID

NARRATIVE-003

# Title

Compare two immutable scene versions with grounded change analysis

# Product

Narrative Architect

# Feature Type

Feature enhancement

# User Story

As a screenwriter, I want to compare two versions of the same scene so I can understand what changed and decide which version better serves my narrative intent.

# User Problem

Revision currently lacks a trustworthy view connecting textual changes to scene purpose while preserving both originals.

# Business / Product Objective

Make iterative creation visibly more useful than generic chat while retaining author control.

# Context

Narrative architecture already defines immutable revisions, evidence spans, NKA canonical truth, and SDI-grounded interpretation.

# Existing Capability

The architecture supports version identity and provenance; NARRATIVE-002 will supply the first NKA aggregate. No comparison implementation exists.

# Proposed Capability

Select two versions of one scene, show a deterministic structural/text diff, then provide an optional SDI-grounded qualitative comparison with evidence drill-down.

# Knowledge Asset Impact

Read scene versions and their objectives/outcomes. Store comparison as a derived artifact; never overwrite either scene version.

# Decision Intelligence Impact

SDI interpretation may identify changed dramatic function or momentum. It diagnoses; it does not predict film success or choose a winner.

# Deterministic Components

Version validation, scene identity, textual/structural diff, source-span mapping, artifact creation, and serialization.

# LLM / AI Components

Qualitative comparison of dramatic effect using SDI terminology. Output remains inferred, schema-validated, and non-canonical unless the author accepts a separate revision.

# Inputs

Two version IDs for the same scene, their NKA context, source spans, and optional author comparison question.

# Outputs

Deterministic diff artifact, grounded qualitative findings, provenance manifest, and evidence links.

# Provenance Requirements

Record both version IDs, span IDs, code version, model/runtime/digest, prompt version, configuration, timestamp, and comparison artifact ID.

# Versioning Requirements

Versions are immutable. Re-running creates a new comparison artifact. No silent merge or mutation.

# Dependencies

NARRATIVE-002-T01 plus an approved SDI scene-comparison prompt and evaluation set.

# Architecture Impact

Fits existing Narrative versioning and local-model ports; no ADR or new Core abstraction is currently required.

# Core Reuse Candidates

Generic artifact comparison presentation may become a candidate only after a second product demonstrates the same need.

# Acceptance Criteria

1. The system rejects versions from different scene identities.
2. Both original versions remain independently retrievable.
3. Repeated structural diff of identical inputs is byte-stable.
4. Every qualitative finding links to at least one version/source span and records model/prompt metadata.
5. The UI labels deterministic changes separately from inferred interpretation.
6. The system never selects, merges, or persists a preferred scene without explicit author action.

# Test Requirements

Unit tests for identity/version/diff rules; integration tests for artifact-to-evidence drill-down; regression fixtures for screenplay formatting edge cases.

# AI Evaluation Requirements

Golden scene pairs must test grounding, SDI terminology, contradiction detection, unsupported claims, and version attribution. Evaluation runs locally.

# Security / Privacy Considerations

Scene text remains local, is absent from content logs, and is sent only to a loopback-approved runtime.

# Observability Requirements

Record execution/artifact IDs, latency, accepted/rejected finding counts, model metadata, and validation failures without screenplay content.

# Explicitly Out of Scope

Automatic winner selection, commercial-success prediction, silent rewrite/merge, cross-scene rewrite, and screenplay-wide diagnosis.

# Definition of Done

All acceptance criteria, deterministic tests, AI evaluations, privacy checks, guardrails, documentation, CI, review, and rollback evidence pass.

# Implementation Notes

Begin behind ports for version retrieval, deterministic diffing, local structured generation, validation, and derived-artifact persistence.

# Suggested Task Breakdown

1. Define comparison and diff contracts.
2. Implement deterministic diff and provenance tests.
3. Define SDI comparison schema/prompt and golden cases.
4. Integrate local generation and validation.
5. Add comparison/evidence UI after intelligence passes.

# Dependency Graph

`NARRATIVE-002-T01 → comparison contracts/diff → SDI evaluation → local AI integration → UI`

# Risks / Open Questions

The definition of “better” must remain the author's intent plus SDI diagnosis, not a universal score. Prompt/evaluation approval is the remaining readiness blocker.

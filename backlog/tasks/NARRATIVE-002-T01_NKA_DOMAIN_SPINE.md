---
task_id: NARRATIVE-002-T01
feature_id: NARRATIVE-002
status: READY
assignee: unassigned
---

# TASK-ID

NARRATIVE-002-T01

# TITLE

Narrative Knowledge Asset domain spine

# OBJECTIVE

Implement the first versioned Narrative Knowledge Asset aggregate containing premise, theme, characters, relationships, acts, sequences, scenes, and references to validated statements.

# PRODUCT CONTEXT

The NKA is canonical memory for CREATE and DOCTOR modes; the author remains authoritative.

# ARCHITECTURAL CONTEXT

Root and Narrative `AGENTS.md`, Constitution, `NARRATIVE_KNOWLEDGE_ASSET.md`, `PROVENANCE_MODEL.md`, and `VERSIONING_MODEL.md`.

# SCOPE

Versioned aggregate, domain entities, statement references, repository port, in-memory adapter, and tests.

# OUT OF SCOPE

Chat, screenplay compiler/parser, SDI scoring, model calls, persistence database, and Streamlit.

# DEPENDENCIES

NARRATIVE-001-T01; relevant Narrative architecture and accepted ADRs.

# INPUTS

Validated statements and explicit revision commands with expected version.

# OUTPUTS

Immutable NKA versions retrievable through a repository protocol.

# IMPLEMENTATION GUIDANCE

- Use immutable version identifiers and optimistic revision checks.
- Preserve epistemic status and evidence on every knowledge-bearing field.
- Keep persistence behind a repository protocol; begin with an in-memory adapter.
- Do not add chat, screenplay compilation, SDI scoring, or Streamlit.

# ACCEPTANCE CRITERIA

- Aggregate schema round-trips without provenance loss.
- A revision produces a new version and leaves the prior version readable.
- Stale revision attempts fail explicitly.
- Unit tests cover creation, revision, historical retrieval, and invalid references.
- Architecture documents are updated if implementation reveals a concrete mismatch.

# TESTS

Run format, lint, types, tests, guardrails, and relevant offline evaluations.

# AI EVALUATIONS

Not applicable: this slice introduces no probabilistic behaviour; existing boundary evaluations must continue to pass.

# DEFINITION OF DONE

All criteria, tests, quality gates, documentation, CI, review, and status updates pass.

# ROLLBACK / SAFETY

The new aggregate is not connected to production. Revert the isolated module and fixtures if contracts are rejected.

# DOCUMENTATION REQUIREMENTS

Update NKA, provenance, and versioning documents only for concrete implementation discoveries; create an ADR for conflicts.

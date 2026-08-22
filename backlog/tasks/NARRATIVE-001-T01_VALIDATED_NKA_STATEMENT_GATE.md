---
task_id: NARRATIVE-001-T01
feature_id: NARRATIVE-001
status: REVIEW
assignee: architecture
---

# TASK-ID

NARRATIVE-001-T01

# TITLE

Validated NKA statement gate

# OBJECTIVE

Implement and verify the smallest complete AI-to-canonical-NKA validation boundary.

# PRODUCT CONTEXT

Narrative Architect uses the Narrative Knowledge Asset—not chat history—as canonical memory.

# ARCHITECTURAL CONTEXT

- `AGENTS.md`
- `narrative/AGENTS.md`
- `docs/CONSAAS_CONSTITUTION.md`
- `docs/NARRATIVE_KNOWLEDGE_ASSET.md`
- `docs/PROVENANCE_MODEL.md`
- feature `NARRATIVE-001`

# SCOPE

Narrative knowledge statement module/tests, the corresponding offline eval, and linked documentation/status.

# OUT OF SCOPE

Chat, storage, complete NKA, compiler, parser, SDI scoring, and UI.

# DEPENDENCIES

Core AI contracts and Narrative provenance architecture.

# INPUTS

Untrusted structured model statement or explicit author assertion.

# OUTPUTS

Validated typed statement or explicit validation failure.

# IMPLEMENTATION GUIDANCE

Assign canonical IDs in code; fail closed; keep user and model epistemic paths separate.

# ACCEPTANCE CRITERIA

All feature criteria pass; the repository remains runnable; no provider SDK enters domain code.

# TESTS

- `pytest -q narrative/tests/test_narrative_statements.py`
- `python evals/run_nka_statement_eval.py`
- `python -m factory.guardrails .`

# AI EVALUATIONS

Run the three versioned offline statement-gate cases without invoking a model.

# DEFINITION OF DONE

Code, tests, evaluation, lint, types, guardrails, security scan, documentation, CI, and human review pass.

# ROLLBACK / SAFETY

Remove the unintegrated module; no production state or migration exists in this slice.

# DOCUMENTATION REQUIREMENTS

Update the feature, task, end-to-end demonstration, factory status, and any architecture mismatch.

# Review checklist

- [x] Scope implemented
- [x] Tests and offline evaluation added
- [x] Deterministic/AI boundary preserved
- [x] No screenplay content sent externally
- [ ] Human review and GitLab pipeline evidence

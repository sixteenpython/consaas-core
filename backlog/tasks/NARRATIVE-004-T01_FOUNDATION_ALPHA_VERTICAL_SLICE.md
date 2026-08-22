---
task_id: NARRATIVE-004-T01
feature_id: NARRATIVE-004
status: REVIEW
assignee: codex
---

# Foundation Alpha vertical slice

## Objective

Implement the complete bounded user outcome in `NARRATIVE-004` while keeping the application runnable
without a model or secret.

## Architecture context

Root and Narrative `AGENTS.md`, Constitution, NKA, versioning, conversational architecture, compiler,
UI architecture, ADR-NA-011, and feature NARRATIVE-004.

## Inputs and outputs

Input is explicit author text entered into the guided flow or editors. Output is a versioned NKA,
portable project JSON, readiness report, and deterministic bounded Fountain draft.

## Tests

- NKA creation, revision, stale-write failure, history, and undo;
- project export/import validation and round-trip;
- guidance sequence and canonical mutation;
- compiler readiness and deterministic output;
- end-to-end service workflow;
- Streamlit headless smoke test;
- full repository quality gates.

## Privacy and rollback

No external inference or durable hosted content storage. Reverting this isolated product slice leaves
the existing statement gate intact and requires no data migration.

## Verification evidence

- 15 Narrative tests pass, including the Streamlit headless smoke test.
- Full repository tests, format, lint, strict typing, guardrails, offline evaluation, Bandit, and
  dependency audit are required before release promotion.
- Human acceptance and post-deployment verification remain release gates.

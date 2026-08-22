---
task_id: CORE-003-T01
feature_id: CORE-003
status: REVIEW
assignee: codex
---

# Governed free-form consulting vertical slice

Implement the CORE-003 free-form consultation, epistemic Case Knowledge Asset, typed dialogue
actions, Decision Position, optional browser WebLLM component, deterministic fallback, tests,
evaluation fixtures, documentation and deployment according to ADR-CORE-003.

## Definition of done additions

- Browser output is untrusted and validated before any case update.
- The component receives data as a mount payload; user/model text is never interpolated into its
  executable HTML or JavaScript.
- No model download occurs until explicit user action.
- The untracked `narrative/Screenplay Course/` material is not modified or committed.

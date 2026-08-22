# End-to-end factory demonstration — NARRATIVE-001

## Flow

1. **Idea:** prevent local-model output from silently becoming canonical story truth.
2. **Feature specification:** `NARRATIVE-001` defines the user trust outcome, boundary, acceptance criteria, risks, and non-goals.
3. **Backlog:** the feature and `NARRATIVE-001-T01` are indexed with dependencies and lifecycle status.
4. **Task contract:** permitted files, required context, verification, and review conditions are explicit.
5. **Implementation:** a typed epistemic statement and deterministic validation gate were added to Narrative domain code.
6. **Tests:** unit tests cover accepted inference, missing fields, ungrounded inference, model-authored user claims, and real user assertions.
7. **Evaluation:** versioned fixtures exercise the AI/canonical boundary offline without calling a model.
8. **CI:** format, lint, types, guardrails, unit tests, offline evaluation, Bandit, and dependency audit are encoded in `.gitlab-ci.yml`.
9. **MR-ready:** the task is REVIEW, not DONE, because no authoritative GitLab remote/runner is configured and no merge request has run.

This demonstrates the operating system without pretending to build Narrative Architect itself.


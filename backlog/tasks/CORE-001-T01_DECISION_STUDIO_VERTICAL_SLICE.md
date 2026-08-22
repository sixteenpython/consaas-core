---
task_id: CORE-001-T01
feature_id: CORE-001
status: REVIEW
assignee: codex
---

# Decision Studio Foundation vertical slice

## Objective

Implement `CORE-001` end to end while preserving the modular-monolith and product-ownership
boundaries in ADR-CORE-001.

## Architecture context

Root `AGENTS.md`, Constitution, Architecture, Pipeline, Golden Knowledge Asset, Decision Engine,
Data Connector Framework, Definition of Done, Decision Studio Foundation and ADR-CORE-001.

## Inputs and outputs

Inputs are governed seed/source rows and explicit anonymous user answers. Outputs are immutable GKA
releases, quality/manifests, a session-only Consultation Asset and deterministic Recommendation Set.

## Tests

- artifact identity, validation, idempotent refresh and failed-candidate rollback;
- three product policy/engine unit suites;
- three end-to-end consultation-to-recommendation integrations;
- optional narrator validation/fallback;
- headless Streamlit smoke for landing and each completed journey;
- full repository factory gates.

## Privacy and rollback

No durable user storage and no secret in source control. Hosted narration is optional and disclosed.
Rollback follows the feature specification and never rewrites retained releases.

## Definition of done

All acceptance criteria in `CORE-001`, repository gates, diff review, documentation, push, deployment
and public smoke verification pass. Human product acceptance remains required.

## Verification evidence

- all three promoted GKA Foundation assets build through one monthly command;
- invalid-candidate rollback and idempotency are covered by tests;
- three consultation-to-recommendation integration paths are covered;
- hosted narrator overwrite attempts are rejected by contract tests;
- Streamlit landing and complete CareerSim journey have a headless smoke test;
- final quality-gate and public deployment evidence are recorded at release handoff.

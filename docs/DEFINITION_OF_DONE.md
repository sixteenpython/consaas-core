# Factory Definition of Done

All items also require scope compliance, clean diff review, no secrets, relevant documentation, and truthful reporting of limitations.

## Architecture task

- Decision/problem, constraints, alternatives, boundaries, data/provenance, security/privacy, failure behavior, migration, and validation are documented.
- Conflicts are resolved through an ADR.
- Links and terminology are consistent; stakeholders have an explicit approval point.

## Code task

- Acceptance criteria pass.
- Formatting, lint, type, unit, integration, architecture, dependency/security, and regression gates pass as applicable.
- Error/failure and rollback paths are tested.
- No unrelated changes, hidden provider coupling, sensitive logging, or unversioned contract break.
- Product remains runnable and task/status docs are current.

## AI task

- Model/provider is behind approved interfaces and registry entry with accurate license/digest.
- Raw output is schema- and domain-validated before canonical use.
- Golden task evaluations, groundedness, failure cases, latency/memory profile, and regression comparison pass.
- Model/prompt/runtime/configuration provenance and local/external boundary are recorded.

## Product feature

- End-to-end user outcome works through the intended UX/API.
- All constituent tasks are DONE; feature-level acceptance, tests, AI evaluations, privacy/security, observability, accessibility, and rollback pass.
- Product Owner accepts usefulness and limitations.

## Migration

- Source/target contracts, compatibility window, data verification, dual-run/backfill where required, rollback, and operator runbook are proven.
- Production remains available; no historical artifact is silently rewritten.

## Release

- Release manifest identifies code/configuration/schemas/models/prompts/artifacts.
- CI/evaluations and manual approvals pass; deployment/rollback and monitoring are ready.
- Changelog, known limitations, security/privacy review, and factory status are updated.
- Post-deployment verification succeeds.

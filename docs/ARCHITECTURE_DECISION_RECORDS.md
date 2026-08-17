# Architecture Decision Records

ADRs are immutable once accepted; later decisions supersede rather than edit history. Each record includes status, context, decision, alternatives, consequences, migration, and validation evidence.

## Initial decision register

| ID | Decision | Status | Rationale |
|---|---|---|---|
| ADR-001 | Modular monolith before microservices | Proposed | Preserves velocity; ports keep later distribution possible. |
| ADR-002 | Hexagonal plugin architecture | Proposed | Keeps runtime independent of domains and infrastructure. |
| ADR-003 | Stable artifact envelope plus domain payload schemas | Proposed | Common governance without a false universal ontology. |
| ADR-004 | Immutable, content-addressed artifacts and append-only releases | Proposed | Enables audit, replay, rollback, and safe publication. |
| ADR-005 | Separate GKA from Decision Views | Proposed | Prevents decision-specific features from corrupting canonical knowledge. |
| ADR-006 | Separate decision, recommendation, report, and UI | Proposed | Each has distinct ownership, testing, and change cadence. |
| ADR-007 | Transactional candidate promotion | Proposed | A failed run cannot partially change production. |
| ADR-008 | SDK contracts use typed payloads and schema IDs | Proposed | Supports compatibility across processes and languages. |
| ADR-009 | Product assembly is declarative | Proposed | Enables generator, validation, and reproducible composition. |
| ADR-010 | LLM output is constrained and non-authoritative by default | Proposed | Controls hallucination and preserves evidence integrity. |
| ADR-011 | Filesystem/SQLite local adapters; object/relational production ports | Proposed | Low-friction development without binding the architecture. |
| ADR-012 | Strangler migration with dual-run parity | Proposed | Protects Vriddhi production while extracting the platform. |
| ADR-013 | Outcomes/evaluation are separate from released recommendations | Proposed | Historical claims remain immutable. |
| ADR-014 | Shared abstractions require two-domain evidence | Proposed | Prevents Vriddhi-shaped Core APIs. |
| ADR-015 | UI consumes ReportBundle/view models only | Proposed | Serving stays deterministic and independent of research execution. |

## ADR template

```text
# ADR-NNN: Title
Status: proposed | accepted | deprecated | superseded
Date / owners
Context and forces
Decision
Alternatives considered
Positive and negative consequences
Security, privacy, data, and operational impact
Compatibility and migration
Validation evidence
Supersedes / superseded by
```

Before implementation, ADR-001 through ADR-009 should be accepted or revised by platform and Vriddhi owners. ADR-010 additionally requires security/model-risk review.

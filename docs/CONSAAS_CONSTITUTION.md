# ConSaaS Constitution

Status: Governing baseline  
Effective: 2026-08-22

## Purpose

ConSaaS exists to **de-risk high-stakes decisions**. It builds systems and services that transform governed evidence into explainable findings or recommendations while preserving human judgment and accountability.

`Data / Artifact -> Ingestion -> Knowledge -> Distillation -> Decision Intelligence -> Recommendation / Finding -> Human Decision`

A ConSaaS product is a domain-specific decision-intelligence system that owns its domain knowledge, intelligence, limitations, and user experience while using proven shared infrastructure. ConSaaS Core is the reusable operating system for artifact lifecycle, provenance, versioning, validation, model access, evaluation, reporting, configuration, security, observability, and delivery. Core is not a universal data model or universal AI engine.

## Product philosophy

1. Start from a consequential user decision, not a technology.
2. Improve decision quality; do not optimize for engagement or automation theatre.
3. Distinguish evidence, inference, calculation, observation, recommendation, and human decision.
4. State uncertainty, assumptions, limitations, and invalid-use boundaries.
5. Keep the human accountable for product judgment, prioritization, acceptance, exceptions, security/business decisions, and real-world usefulness.
6. The factory supplies disciplined execution, not autonomous product judgment.

## Architecture philosophy

Use **common infrastructure + domain-specific intelligence**. Never force one universal knowledge schema or one universal decision engine across products. Keep a capability product-specific when reuse is uncertain.

A capability normally enters Core only after at least two products demonstrate the same semantics, failure modes, and lifecycle. Promotion requires evidence, tests, ownership, compatibility policy, and an ADR. Similar names or duplicate-looking code are insufficient evidence.

Prefer a modular monolith. Introduce a service boundary only for measured security isolation, independent scaling, reliability, deployment, or ownership needs. Directory structure is not justification for microservices.

## Deterministic and probabilistic systems

Deterministic code owns mechanics where practical: identifiers, parsing rules, arithmetic, constraints, thresholds, ordering, persistence, versioning, provenance, release gates, and report assembly. Probabilistic models may interpret, extract, classify, summarize, or formulate recommendations. Raw model output is untrusted input:

`Raw model output -> schema validation -> domain validation -> canonical result`

An LLM may never silently alter deterministic values or directly persist canonical knowledge. Applications use provider-neutral interfaces and model registries; they never hard-code a provider or model into business logic.

Local inference is the default. ConSaaS must not require OpenAI, Anthropic, Gemini, paid inference, or proprietary hosted APIs. Model licensing must be recorded accurately; “open source” is used only when the license supports that description.

## Evidence and provenance

Every important output must identify applicable input artifact/version, knowledge revision, code/configuration, model artifact and runtime, prompt/template, deterministic parameters, timestamp, validation results, and output version. Users must be able to traverse recommendation/finding to its evidence. Missing provenance reduces authority; it is not reconstructed by assertion.

## Human accountability

Systems assist, challenge, explain, and recommend. Humans approve consequential actions and creative or business decisions. Material model-proposed changes require explicit authority. Overrides are recorded with actor, reason, scope, and expiry where applicable.

## Security and privacy

Use least privilege, local-first processing where appropriate, environment/secret-store configuration, dependency and secret scanning, safe logging, input isolation, and explicit external-data boundaries. Sensitive content, unpublished intellectual property, credentials, and PII must not enter logs or external model calls by default. Security controls cannot be bypassed to make a demo pass.

## Versioning and change

Canonical artifacts and important decisions are immutable or versioned with explicit lineage. Schema, methodology, model, prompt, configuration, code, and policy versions are independent identities. No silent migration, model substitution, or methodology fallback is permitted.

Architectural changes require an ADR when they alter boundaries, canonical data, public contracts, provenance, security/privacy posture, model policy, or product methodology. When requirements conflict with architecture, stop and escalate; do not silently redesign.

## Testing and AI evaluation

Every change receives proportionate unit, integration, contract, security, architecture, and regression tests. AI behavior uses versioned golden cases based on real ConSaaS tasks, including groundedness and failure behavior—not generic benchmarks alone. A model upgrade is a behavior change and requires evaluation.

Quality gates must be reproducible locally and in CI. Tests are not bypassed, weakened, or rewritten merely to accept a defective implementation.

## Product lifecycle

`Idea -> Feature Creator -> reviewed feature -> backlog -> READY task -> branch -> implementation -> tests/evals -> CI -> merge request -> review -> deploy -> product feedback -> new backlog item`

Each task leaves the product runnable. Production changes use rollback plans and safe migration. Vriddhi follows a strangler extraction path; production is never broken to satisfy Core reuse.

## Documentation authority

1. Constitution
2. Architecture
3. ADR
4. Product specification
5. Feature specification
6. Implementation task
7. Code, tests, and evaluations

Lower levels implement higher levels. When authorities conflict, stop and resolve through an ADR or explicit correction; never silently choose.

## Portfolio boundary

The current portfolio is Vriddhi (live), Narrative Architect (architecture complete/implementation starting), HouseWise (planned), and CareerSim (planned). Additional products require an explicit portfolio decision.

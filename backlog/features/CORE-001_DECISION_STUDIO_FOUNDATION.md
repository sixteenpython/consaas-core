---
id: CORE-001
mode: RELEASE
status: REVIEW
product: core
type: vertical-slice feature
owner: product-owner
created: 2026-08-22
dependencies: []
readiness: ready
---

# ConSaaS Decision Studio Foundation

## User outcome

A user selects CareerSim, HouseWise or StartupEval, completes a pointed structured consultation and
receives an explainable verdict, ranked options, risks, assumptions, evidence and next actions.

## Included

- three versioned GKA Foundation schemas and seed datasets;
- source catalogs, provenance, quality results and promoted manifests;
- one idempotent monthly refresh command with candidate isolation and atomic promotion;
- canonical session-only consultation assets;
- domain-owned question sequences, policies and deterministic decision engines;
- optional validated open-model narration through Core AI contracts;
- one Streamlit landing page and three complete journeys;
- downloads, limitations, privacy and evidence drill-down;
- tests, documentation, release manifest and deployment.

## Excluded

Exhaustive market coverage, accounts, durable user storage, paid data/API dependencies, transactional
execution, legal/financial/admission advice, real property valuation, startup success prediction,
microservices and changes to Vriddhi or Narrative Architect runtimes.

## Acceptance criteria

1. Every journey completes without an LLM or network call.
2. Each verdict is reproducible from consultation, GKA and policy versions.
3. Every ranked option and risk links to evidence or an explicit user assertion.
4. Failed refresh validation leaves the promoted release unchanged.
5. All three GKAs expose schema, cutoff, content hash, source provenance and quality state.
6. Optional model prose cannot change deterministic verdicts or numbers.
7. No user answer is durably stored or logged.
8. The public UI states scope, limitations and Foundation data coverage clearly.
9. Unit, integration, UI, guardrail, type, lint and security gates pass.
10. All three live journeys pass post-deployment smoke verification.

## Rollback

Revert the isolated feature commit or repoint Streamlit. GKA rollback moves only a validated promoted
pointer; retained releases are immutable.

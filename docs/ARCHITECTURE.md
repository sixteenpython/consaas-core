# Architecture

## Style

ConSaaS Core uses a hexagonal, plugin-oriented architecture around an artifact pipeline. The runtime depends only on SDK contracts. Product plugins depend on the SDK, never on Core internals. Adapters connect providers, storage, models, renderers, and deployment systems.

## Planes

**Control plane:** product registry, manifests, plugin catalog, scheduling, policy, run state, approvals, release registry, secrets references, compatibility, and observability.

**Execution plane:** acquisition, normalization, knowledge construction, distillation, decision execution, recommendation generation, report composition, validation, and isolated candidate storage.

**Serving plane:** immutable release resolution, query APIs, cached report/view-model delivery, and dashboard shells. Serving never triggers research or authoritative decision computation.

## Dependency direction

`product plugins -> plugin_sdk <- core runtime`

`connectors/renderers/storage adapters -> plugin_sdk`

Core has no import dependency on Vriddhi, HouseWise, or any domain package. Products are assembled by a declarative `product.yaml` manifest and plugin entry points.

## Artifact progression

1. `SourceSnapshot`: retained raw or source-addressable inputs.
2. `GoldenAsset`: complete canonical domain knowledge.
3. `DecisionView`: purpose-specific, decision-relevant features and constraints.
4. `DecisionResult`: ranked/scored/optimized/modelled result plus diagnostics.
5. `RecommendationSet`: actionable recommendations with evidence links.
6. `ReportBundle`: channel-neutral sections, tables, charts, narratives, and disclosures.
7. `Release`: signed manifest linking all artifacts, validations, and approvals.

Every artifact uses a standard envelope containing artifact ID, product and tenant scope, schema and methodology versions, effective time and observed time, run ID, parent artifact IDs, producer plugin/version, content hash, code/config identity, quality state, and payload reference.

## Run state machine

`requested -> acquiring -> building_knowledge -> distilling -> deciding -> recommending -> reporting -> validating -> needs_review|approved -> promoted`

Any stage may become `failed` or `quarantined`. Promotion uses compare-and-swap against the current release pointer. Retries use idempotency keys. Supersession is explicit; history is append-only.

## Extensibility

Plugins are discovered through manifests/entry points, instantiated through dependency injection, and invoked in isolated run contexts. Contracts are transport-neutral so the first implementation can be an in-process modular monolith and later move expensive or untrusted stages to workers without changing product code.

## Deployment strategy

Begin as a modular monolith with filesystem/object-store artifacts and a relational control store. Do not start with microservices. Split a component only for independent scaling, security isolation, reliability, or ownership—not directory aesthetics.

## Non-functional targets

- Atomic promotion and one-command rollback.
- Full lineage for every published claim.
- Deterministic replay where dependencies permit; otherwise declared reproducibility class.
- Contract compatibility checks before a run.
- Tenant isolation, scoped secrets, encrypted storage, and audit events.
- Stage metrics, structured logs, traces, data-quality results, and cost records.

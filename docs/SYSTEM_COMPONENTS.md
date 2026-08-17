# System Components

## Platform modules

| Component | Responsibility | Must not own |
|---|---|---|
| Runtime kernel | run context, DAG execution, lifecycle, cancellation, idempotency | domain rules |
| Artifact store | immutable blobs, hashes, candidate/release namespaces | payload meaning |
| Metadata and release registry | lineage, schemas, runs, approvals, promoted pointers | raw large payloads |
| Connector runtime | retries, rate limits, cursors, caching, secret handles | provider-specific mapping |
| Knowledge runtime | schema registry, quality suites, temporal and lineage services | domain schema |
| Decision runtime | engine invocation, reproducibility, diagnostics, evaluation hooks | decision formula |
| Recommendation runtime | common action/evidence structures, policy gates, explanation assembly | domain action taxonomy |
| Reporting runtime | channel-neutral document/view models and renderer registry | authoritative decisions |
| UI shell | navigation, release context, accessibility, standard evidence/disclosure components | acquisition or inference |
| Plugin manager | discovery, compatibility, capabilities, configuration validation | business workflow |
| Policy/approval service | gate evaluation, review workflow, audit | hidden manual mutation |
| Observability | structured logs, metrics, traces, data quality, cost, audit events | sensitive payload leakage |
| Product generator | deterministic scaffolding and conformance fixtures | runtime code generation |

## Storage model

Use object storage for immutable artifact payloads; a relational store for products, plugin versions, runs, lineage edges, policies, approvals, and release pointers; a secrets manager for credentials; and optional product-selected indexes for serving. Local development may implement these ports with filesystem and SQLite.

## Security and tenancy

Run context carries tenant, product, actor, purpose, and correlation IDs. Plugins receive capability-scoped services rather than ambient filesystem/network access. Secrets are references, never serialized artifacts. Logs redact configured fields. Promotion and approval actions are audit events. Tenant and product namespaces are enforced at storage ports.

## Operational ownership

Platform engineering owns contracts, runtime, compatibility, release safety, and shared UX. Product teams own plugins, schemas, domain policies, fixtures, and outcome definitions. A platform council approves contract changes and cross-domain promotion of abstractions.

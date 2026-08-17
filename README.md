# ConSaaS Core

ConSaaS Core is the operating system for explainable Decision Intelligence products. It extracts the reusable architecture proven by Vriddhi so that new products are assembled from domain plugins instead of rebuilt as independent applications.

## Product contract

A product supplies only:

1. data-source connector configuration or connector plugins;
2. a versioned Golden Knowledge Asset schema and builder;
3. domain distillation and decision logic;
4. optional recommendation wording and page extensions.

The platform supplies run orchestration, immutable artifacts, provenance, schema validation, policy gates, release promotion and rollback, recommendation and evidence contracts, report composition, dashboard shells, observability, testing harnesses, CI templates, and product scaffolding.

## Universal pipeline

`Sources -> Golden Knowledge Asset -> Decision View -> Decision Engine -> Recommendations -> Reports/View Models -> UX`

Every stage consumes and emits a versioned artifact envelope. A release is promoted only when all required contracts, quality gates, policy checks, and product smoke tests pass.

## Architecture status

This repository is currently an architecture blueprint, not an implementation. The documents in [docs](./docs) define the intended boundaries and migration path. Vriddhi remains the production system and first reference product while capabilities are extracted incrementally through compatibility adapters.

## Design goals

- At least 80% platform reuse for HouseWise.
- A new product is primarily schemas, plugins, decision logic, fixtures, and configuration.
- Deterministic replay and complete evidence for every published recommendation.
- No UI, report renderer, or LLM owns authoritative decision logic.
- No failed candidate can partially replace a published release.
- Domain independence without reducing every domain to an artificial common data model.

## Reading order

Start with [VISION.md](./docs/VISION.md), [FIRST_PRINCIPLES.md](./docs/FIRST_PRINCIPLES.md), [ARCHITECTURE.md](./docs/ARCHITECTURE.md), and [PLUGIN_SDK.md](./docs/PLUGIN_SDK.md). The migration sequence is in [ROADMAP.md](./docs/ROADMAP.md).

## Document map

- Direction: [Vision](./docs/VISION.md), [Manifesto](./docs/MANIFESTO.md), [First Principles](./docs/FIRST_PRINCIPLES.md)
- Platform: [Architecture](./docs/ARCHITECTURE.md), [Pipeline](./docs/CONSAAS_PIPELINE.md), [Components](./docs/SYSTEM_COMPONENTS.md), [Repository](./docs/REPOSITORY_STRUCTURE.md)
- Contracts: [Plugin SDK](./docs/PLUGIN_SDK.md), [Golden Knowledge Asset](./docs/GOLDEN_KNOWLEDGE_ASSET.md), [Decision Engine](./docs/DECISION_ENGINE.md), [Data Connectors](./docs/DATA_CONNECTOR_FRAMEWORK.md), [Report Engine](./docs/REPORT_ENGINE.md)
- Delivery: [Product Generator](./docs/PRODUCT_GENERATOR.md), [Roadmap](./docs/ROADMAP.md), [Coding Standards](./docs/CODING_STANDARDS.md), [ADR Register](./docs/ARCHITECTURE_DECISION_RECORDS.md)
- Extraction: [Vriddhi Module Inventory](./docs/VRIDDHI_MODULE_INVENTORY.md)

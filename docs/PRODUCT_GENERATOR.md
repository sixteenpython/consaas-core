# Product Generator

## Goal

`consaas new product-spec.yaml` creates a deployable, contract-conformant product skeleton. It generates structure and adapters, not domain judgment.

## Input specification

```yaml
product:
  name: HouseWise
  id: housewise
  domain: real-estate
sources: [property_registry, listings, locality_signals]
golden_asset:
  schema: schemas/property_knowledge.v1.json
decision:
  engine: housewise.decision:PropertyDecisionEngine
ui:
  pages: [overview, shortlist, property, risk, evidence]
```

The full spec also declares product version, schedules, decision requests, connector configuration schemas, distiller, recommendation taxonomy, policies, reports, themes, deployment target, tenancy, data classification, and outcome metrics.

## Generated output

- product manifest and validated configuration;
- plugin package stubs for connectors, GKA builder, distiller, engine, recommender, reporter, and optional page extensions;
- JSON/Pydantic schema locations and migration skeletons;
- fixtures, contract tests, golden tests, smoke tests, and sample offline data;
- local run configuration, CLI commands, CI/release workflow, deployment adapter;
- ADR, methodology, data-source, privacy, operations, and runbook templates;
- dependency lock and compatibility declaration.

## Generator qualities

Generation is deterministic, template-versioned, dry-run capable, idempotent, and merge-aware. Generated files carry ownership markers only where regeneration is safe. Product-owned code is never overwritten. `consaas doctor` checks SDK compatibility, missing contracts, schema registrations, provenance coverage, and deployment readiness.

## Workflow

1. Validate spec and resolve plugins.
2. Show the planned file graph and unresolved domain decisions.
3. Scaffold to a new directory.
4. Run offline conformance tests against fixtures.
5. Produce a “first candidate” checklist, never an automatic production release.

Success is measured by time to first validated candidate and percentage of generated/shared code, not line count.

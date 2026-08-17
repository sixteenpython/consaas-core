# Repository Structure

```text
consaas-core/
├── README.md
├── docs/                    # Architecture, contracts, ADRs, roadmap
├── core/                    # Runtime, policies, artifacts, releases, observability
├── connectors/              # Connector runtime and shared provider adapters
├── knowledge/               # GKA envelope, registry, lineage, quality, migrations
├── decision_engine/         # Engine runtime, evaluation, composition, adapters
├── recommendation_engine/   # Action/evidence model and explanation assembly
├── reporting/               # Report model, components, renderers, exports
├── ui/                      # Dashboard shell, design system, block renderers
├── plugin_sdk/              # Stable public contracts and conformance kit
├── templates/               # Product Generator templates
├── examples/                # Minimal reference products and tutorials
├── plugins/                 # Optional shared/provider plugin packages
├── vriddhi/                 # Vriddhi manifest and domain plugins
├── housewise/               # Reserved product package
├── careersim/               # Reserved product package
├── startup/                 # Reserved product package
└── narrative/               # Reserved product package
```

The repository begins as a monorepo, but packages have explicit APIs. `plugin_sdk` has the strongest stability promise. Core depends on SDK abstractions; products depend on the SDK and shared plugins, never another product. UI depends on report/view models, not engines.

Tests live beside packages plus top-level contract and end-to-end suites. Architecture checks reject reverse dependencies and imports from internal modules.

Generated data, candidates, releases, caches, secrets, and logs are not source packages. Local implementations use ignored `.consaas/`; production uses configured stores. Product directories contain manifests, schemas, migrations, policies, plugins, tests, fixtures, and domain docs—not published user data.

Core, SDK, templates, and product plugins version independently. A compatibility matrix records supported SDK, artifact-schema, and template versions; a monorepo does not imply lockstep deployment.

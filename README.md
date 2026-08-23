# ConSaaS Core

ConSaaS Core is the operating system for explainable Decision Intelligence products. It extracts the reusable architecture proven by Vriddhi so that new products are assembled from domain plugins instead of rebuilt as independent applications.

## Decision Studio Foundation

The root Streamlit application now contains three bounded, runnable Decision Intelligence journeys:

- **CareerSim** for Indian students evaluating overseas undergraduate, master's and PhD ROI;
- **HouseWise** for Indian residential purchase decisions;
- **StartupEval** for founder and investor venture assessment.

Decision Studio v0.4 adds scenario/Pareto intelligence for education and property plus an
eleven-question India Problem Observatory and Horse/Jockey engine for startup assessment. Each
journey uses a free-form adaptive expert conversation, an epistemic and revision-aware
session-only Case Knowledge Asset, a live Decision Position, a promoted GKA with explicit
decision-metric coverage, a versioned deterministic policy, explainable recommendations and an
optional provider-free browser model behind a typed validation gate. Run it with
`streamlit run streamlit_app.py`.

Refresh all three promoted knowledge assets with:

```powershell
python refresh_monthly.py --effective-date YYYY-MM-DD
# For a corrected same-day methodology release:
python refresh_monthly.py --effective-date YYYY-MM-DD --release-tag decision-intelligence-v1
```

See [Decision Studio architecture](./docs/DECISION_STUDIO_FOUNDATION.md) and the
[monthly operations runbook](./docs/DECISION_STUDIO_OPERATIONS.md). The v0.3 interaction boundary is
documented in [Conversational Decision Intelligence](./docs/CONVERSATIONAL_DECISION_INTELLIGENCE.md).
The v0.4 domain engines are documented in
[Domain Decision Intelligence v1](./docs/DECISION_STUDIO_REENGINEERING_V1.md).

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

## Factory status

The repository now contains the first controlled factory bootstrap: governance, scoped agent contracts, Feature Creator, task/backlog conventions, product templates, local-AI contracts, a model registry, architecture guardrails, tests, offline evaluations, and a GitLab CI definition. Vriddhi remains the production reference product; Narrative Architect now includes a deliberately bounded, deterministic Foundation Alpha for Create mode.

See [FACTORY_STATUS.md](./FACTORY_STATUS.md). Items remain in `REVIEW` until human review and a real GitLab pipeline are available; the configured remote is currently GitHub, so this repository does not claim a GitLab merge request has run.

## Design goals

- At least 80% platform reuse for HouseWise.
- A new product is primarily schemas, plugins, decision logic, fixtures, and configuration.
- Deterministic replay and complete evidence for every published recommendation.
- No UI, report renderer, or LLM owns authoritative decision logic.
- No failed candidate can partially replace a published release.
- Domain independence without reducing every domain to an artificial common data model.

## Reading order

Start with the [Constitution](./docs/CONSAAS_CONSTITUTION.md), [Vision](./docs/VISION.md), [First Principles](./docs/FIRST_PRINCIPLES.md), [Architecture](./docs/ARCHITECTURE.md), and root [AGENTS.md](./AGENTS.md). Factory operation is defined by [Factory Mode](./docs/FACTORY_MODE.md), [Feature Creator](./docs/FEATURE_CREATOR.md), and the [Definition of Done](./docs/DEFINITION_OF_DONE.md).

## Document map

- Direction: [Vision](./docs/VISION.md), [Manifesto](./docs/MANIFESTO.md), [First Principles](./docs/FIRST_PRINCIPLES.md)
- Platform: [Architecture](./docs/ARCHITECTURE.md), [Pipeline](./docs/CONSAAS_PIPELINE.md), [Components](./docs/SYSTEM_COMPONENTS.md), [Repository](./docs/REPOSITORY_STRUCTURE.md)
- Contracts: [Plugin SDK](./docs/PLUGIN_SDK.md), [Golden Knowledge Asset](./docs/GOLDEN_KNOWLEDGE_ASSET.md), [Decision Engine](./docs/DECISION_ENGINE.md), [Data Connectors](./docs/DATA_CONNECTOR_FRAMEWORK.md), [Report Engine](./docs/REPORT_ENGINE.md)
- Delivery: [Product Generator](./docs/PRODUCT_GENERATOR.md), [Roadmap](./docs/ROADMAP.md), [Coding Standards](./docs/CODING_STANDARDS.md), [ADR Register](./docs/ARCHITECTURE_DECISION_RECORDS.md)
- Extraction: [Vriddhi Module Inventory](./docs/VRIDDHI_MODULE_INVENTORY.md)
- Narrative Architect: [Architecture](./docs/NARRATIVE_ARCHITECTURE.md), [Narrative Knowledge Asset](./docs/NARRATIVE_KNOWLEDGE_ASSET.md), [Virtual Screenplay Expert](./docs/VIRTUAL_SCREENPLAY_EXPERT.md), [MVP Scope](./docs/MVP_SCOPE.md), [Implementation Roadmap](./docs/IMPLEMENTATION_ROADMAP.md)
- Factory: [Constitution](./docs/CONSAAS_CONSTITUTION.md), [Factory Mode](./docs/FACTORY_MODE.md), [Quality Gates](./docs/QUALITY_GATES.md), [Architecture Guardrails](./docs/ARCHITECTURE_GUARDRAILS.md), [Initial Backlog](./docs/INITIAL_FACTORY_BACKLOG.md)
- Assurance: [AI Evaluation](./docs/AI_EVALUATION.md), [Security](./docs/SECURITY.md), [Privacy](./docs/PRIVACY.md), [Observability](./docs/OBSERVABILITY.md), [Reproducibility](./docs/REPRODUCIBILITY.md)

## Local verification

```powershell
python -m pytest -q
python evals/run_nka_statement_eval.py
python -m factory.guardrails .
```

Install the optional `dev` dependencies to run formatting, linting, typing, security, and dependency-audit gates identical to `.gitlab-ci.yml`.

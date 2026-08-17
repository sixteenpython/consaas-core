# Roadmap: Vriddhi to ConSaaS Core

The migration uses a strangler pattern. Vriddhi remains deployable from its current repository throughout. Every phase has an adapter path back to its existing JSON/CSV artifacts and Streamlit UI.

## Phase 0 — Baseline and freeze contracts (2–3 weeks)

Document current artifact schemas, module dependencies, refresh/release invariants, UX view models, and operating SLOs. Add characterization and golden-output tests around the August 2026 release. Capture current refresh duration, failure rate, replay hash, and deployment health.

**Exit:** current behavior can be detected if changed; no production path altered.

## Phase 1 — SDK and artifact envelope (3–5 weeks)

Implement the minimal SDK value types, artifact envelope, schema registry, validation result, run context, plugin descriptor, and filesystem adapters. Wrap existing Vriddhi loaders/builders with compatibility adapters; continue emitting legacy files byte-for-byte.

**Exit:** Vriddhi artifacts are addressable through Core contracts and legacy tests still pass.

## Phase 2 — Release kernel (4–6 weeks)

Extract staging, idempotency, validation composition, manifests/hashes, approvals, atomic promotion, rollback, run state, and structured telemetry from `vriddhi_monthly_refresh.py` and `vriddhi_validation.py`. Shadow-run Core beside the existing refresh and compare artifacts.

**Exit:** repeated shadow runs match; failure injection proves no partial promotion.

## Phase 3 — Knowledge and connector framework (4–6 weeks)

Wrap Yahoo/NSE acquisition and ticker resolution as Vriddhi connectors. Define Vriddhi GKA schema v1 and lineage. Retain source snapshots where licensing permits. Dual-write CSV and the new artifact format.

**Exit:** GKA quality and freshness gates equal or exceed current validation; legacy builder can consume an exported CSV.

## Phase 4 — Decision and recommendation plugins (5–8 weeks)

Move screening, forecasting, optimization, walk-forward evidence, gates, and rebalance semantics behind SDK contracts without changing methodology. Introduce Decision View, Decision Result, Recommendation Set, and ledger artifacts. Run old/new paths on identical inputs and require tolerance-based parity.

**Exit:** domain-owned plugin produces approved parity across all horizons and retained releases.

## Phase 5 — Reporting and UI shell (4–6 weeks)

Extract report blocks and reusable UX patterns. Adapt current Streamlit panels to `ReportBundle`; preserve routes, labels, and production deployment. Add renderer contract tests and visual smoke tests.

**Exit:** Vriddhi serves only promoted view models while matching accepted UX.

## Phase 6 — Generator and HouseWise proof (6–10 weeks)

Build Product Generator from the proven contracts. Scaffold HouseWise, implement only its domain plugins, and measure reuse. Do not move a second-domain abstraction into Core until comparison proves shared semantics.

**Exit:** HouseWise reaches a validated candidate with at least 80% non-domain code supplied by Core/templates.

## Phase 7 — Platform hardening (ongoing)

Add object/relational production adapters, tenant isolation, approval UI, plugin signing, sandboxed workers, schema migration automation, policy packs, cost controls, disaster recovery, and platform SLOs. Migrate CareerSim next to test a non-financial domain.

## Rollout controls

- Feature flags select legacy, shadow, or Core path per stage.
- Dual-run comparisons block cutover on unexplained deltas.
- One stage migrates at a time; rollback changes only routing.
- Historical artifacts are immutable; migrations create descendants.
- Production cutover requires performance, security, data-quality, replay, and operator-runbook sign-off.

## Measures

Track shared-code percentage, product-specific LOC, time to first candidate/release, plugin conformance, replay success, provenance completeness, candidate rejection rate, escaped defects, mean recovery time, decision stability, and cost per run.

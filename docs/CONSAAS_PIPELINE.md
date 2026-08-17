# ConSaaS Pipeline

Each stage implements `prepare`, `execute`, and `validate`; consumes named artifacts; emits typed artifacts; and declares side effects, retry policy, resource needs, and compatibility. The runtime owns scheduling, checkpoints, cancellation, lineage, and publication.

| Stage | Input | Output | Platform invariant | Product responsibility |
|---|---|---|---|---|
| Acquire | source specs, watermark | source snapshots | identity, checksums, retries, provenance | endpoints, mappings, credential scope |
| Build knowledge | source snapshots | Golden Asset | envelope, schema registry, lineage, quality execution | canonical schema and transformations |
| Distill | Golden Asset, request | Decision View | feature lineage and leakage checks | relevance, features, constraints |
| Decide | Decision View | Decision Result | engine lifecycle, diagnostics, execution identity | scoring, rules, optimization, ML/LLM logic |
| Recommend | result, context, policy | Recommendation Set | action/evidence schema and policy evaluation | domain actions, suitability, reason codes |
| Report | recommendations, evidence | Report Bundle | accessibility, disclosures, view-model schema | narratives and page extensions |
| Release | all artifacts | promoted release | validation, approval, hashes, atomic promotion | product release gates |

## Execution

A `RunRequest` fixes product version, effective date, configuration digest, connector watermarks, and decision context. The orchestrator builds a DAG from the product manifest. Stages write only to an isolated candidate namespace. Contract and product validators run at boundaries; policy gates run before promotion. The content-addressed release manifest captures every artifact and execution identity. Serving resolves one promoted pointer and cannot observe partial candidates.

The graph supports scheduled refresh, event-driven update, scenarios, backfill, and replay. Connectors expose cursors; builders declare incremental support. Historical runs use an explicit knowledge cutoff to prevent future-data leakage.

Transient errors retry within declared limits. Invalid data is quarantined. Required-stage failure stops publication. Optional enrichment may degrade only through a declared fallback that appears in the report. Methodology never changes silently.

Outcomes are stored separately from historical recommendations. Evaluators can measure calibration, drift, backtests, and prospective performance without rewriting published evidence.

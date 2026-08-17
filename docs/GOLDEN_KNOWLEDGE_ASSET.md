# Golden Knowledge Asset

## Definition

The Golden Knowledge Asset (GKA) is the complete, governed, canonical knowledge available to a product at a declared cutoff. It is not a feature table, recommendation, report, or mutable operational database.

Core defines a stable envelope; each product defines one or more versioned payload schemas. This preserves cross-product governance without inventing a universal ontology.

## Envelope

Required metadata includes asset and run IDs, product/tenant, schema and methodology versions, effective interval, observation and ingestion times, knowledge cutoff, source snapshot IDs, lineage, producer identity, content hash, quality result, sensitivity classification, license/retention tags, and reproducibility class.

## Knowledge layers

1. **Raw snapshots:** byte-preserved or source-addressable evidence.
2. **Canonical entities/events:** normalized identifiers, units, temporal facts, and relationships.
3. **Derived knowledge:** calculations that remain broadly useful across decisions.
4. **Decision Views:** narrow, purpose-bound features and constraints; these are not part of the complete GKA.

## Temporal and provenance rules

Facts may carry valid time and system/observation time. Historical evaluation resolves only facts known at its cutoff. Every derived field links to transformation version and parent fields or source records. Entity resolution decisions and overrides are retained as auditable records.

## Quality gates

The platform runs structural, semantic, referential, freshness, completeness, uniqueness, range, drift, and cross-source reconciliation checks. Products add domain invariants. Results are data, not logs: each check has severity, observed value, threshold, affected records, and disposition.

## Evolution

Schemas use semantic versions. Additive compatible changes remain within a major version; changed meaning requires a new field or major version. Migrations are explicit, pure where possible, tested against retained assets, and recorded as lineage. Readers declare supported schema ranges.

## Vriddhi example

`grand_table_expanded.csv` is an early GKA payload: company identifiers, sectors, prices, fundamentals, and forecasts. In Core it becomes a versioned domain payload with retained source snapshots, field lineage, temporal semantics, validation output, and no dependence on CSV as the contract.

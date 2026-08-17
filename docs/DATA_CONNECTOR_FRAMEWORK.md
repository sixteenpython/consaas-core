# Data Connector Framework

## Contract

A connector translates a `SourceSpec` into one or more immutable `SourceSnapshot` artifacts. It declares source identity, authentication type, supported temporal modes, pagination/cursor strategy, rate limits, licensing/retention terms, expected schema, sensitivity, and network capabilities.

`discover` creates a plan without mutation; `acquire` executes it; `checkpoint` exposes a resumable cursor; `validate` reports source-level quality; and optional `normalize` maps provider records into a declared canonical input schema. Domain-wide knowledge construction is not a connector responsibility.

## Runtime services

Core supplies scoped secrets, HTTP/client factories, retries with jitter, throttling, circuit breakers, pagination helpers, cache, checksums, watermark storage, deduplication, quarantine, structured telemetry, and test doubles. Plugins do not receive raw global credentials.

## Modes

- full snapshot;
- incremental since cursor;
- as-of historical acquisition;
- webhook/event ingestion;
- user-uploaded file;
- licensed dataset reference where bytes cannot be retained.

Every connector states consistency and replay guarantees. When raw retention is prohibited, the snapshot stores a signed source reference, query, retrieval time, response hash where permitted, and license metadata.

## Entity resolution

Core provides alias tables, candidate matching workflow, audit records, and human-review states. Domain plugins supply identity keys and match policy. Vriddhi’s self-healing ticker resolver becomes the reference for this capability, while NSE/Yahoo naming rules remain in the Vriddhi connector.

## Testing

Connector conformance requires recorded fixtures, pagination/cursor tests, timeout/retry tests, rate-limit behavior, schema-drift detection, idempotency, secret-redaction checks, and a network-disabled replay test. Live tests are separate and never required for deterministic CI.

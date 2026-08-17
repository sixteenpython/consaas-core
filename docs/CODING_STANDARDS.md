# Coding Standards

## Boundaries and APIs

- Code against SDK protocols and ports; dependency injection occurs at composition roots.
- Product packages cannot import Core internals or another product.
- Domain rules are pure functions where practical; I/O stays in adapters.
- Public APIs, schemas, reason codes, and artifact meanings are documented and versioned.
- No dataframe is an implicit cross-package contract; validate at the boundary.

## Python baseline

Use supported Python with type checking in strict mode for public packages, Ruff formatting/linting, immutable dataclasses or validated models for contracts, `pathlib`, timezone-aware UTC instants, `Decimal` for monetary settlement, explicit units, and injected clocks/randomness. Avoid mutable globals and import-time I/O.

## Errors and telemetry

Use the SDK error taxonomy with retryability and safe operator messages. Never swallow exceptions or silently substitute methodology. Emit structured events with run/artifact/plugin IDs. Secrets and sensitive payloads must be redacted by construction.

## Data and models

- Record missingness; do not confuse missing, zero, and not applicable.
- Reject non-finite numbers at serialization boundaries.
- Preserve raw precision; round only in reports or execution policies.
- Capture model, prompt, solver, dependency, seed, configuration, and code identity.
- Time-aware tests must verify knowledge cutoffs and leakage prevention.

## Tests

Each plugin requires unit tests, Core conformance tests, fixtures, schema compatibility, idempotency, provenance, degraded/failure paths, and offline replay. Engines require golden and metamorphic/property tests. Renderers require semantic and accessibility tests. Release code requires failure injection and atomicity tests.

## Review gates

CI runs compile/type/lint/unit/contract/integration checks, dependency and secret scans, schema compatibility, architecture dependency rules, license policy, and artifact reproducibility where applicable. Code owners review SDK and schema breaking changes. Security-sensitive changes require threat-model updates.

## Documentation

Every plugin documents purpose, inputs/outputs, configuration, side effects, data license, failure behavior, reproducibility class, limitations, and owner. Significant decisions receive an ADR; methodology changes include comparison evidence and migration impact.

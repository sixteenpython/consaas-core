# ADR-CORE-002: Separate expert dialogue, Case Knowledge and decision authority

Status: Accepted  
Date: 2026-08-23

## Decision

Evolve Decision Studio from fixed questionnaires to adaptive expert consultations. Introduce an
immutable session-only Case Knowledge Asset, a deterministic information-value dialogue policy,
validated optional open-weight wording, and versioned product metric catalogs. Deterministic product
engines continue to own all calculations, rankings and verdicts.

CareerSim is narrowed to Indian students evaluating overseas undergraduate, master's and PhD ROI.

## Why

A consultant must interpret answers, explain implications, challenge uncertainty and ask the next
most decision-relevant question. Allowing a model to own state or verdicts would weaken replay,
provenance and safety. A metric catalog makes knowledge expansion explicit and testable without
claiming unavailable evidence.

## Consequences

Question contracts gain importance and expert-context metadata. GKA artifact hashes include the
metric catalog. Existing 2026-08-22 releases remain valid rollback points but v0.2 UI requires a
v0.2 release containing the catalog. External wording remains optional; deterministic conversation
is the always-available production fallback.


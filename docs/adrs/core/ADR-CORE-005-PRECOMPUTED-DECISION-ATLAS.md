# ADR-CORE-005: Precomputed Decision Atlas

- **Status:** Accepted
- **Date:** 2026-08-23

## Decision

Each product refresh must process the entire covered decision universe into an immutable Decision
Atlas before promotion. Live consultations apply validated customer constraints to this atlas; they
do not perform universe research or model training.

The deterministic champion remains authoritative until a learned challenger passes out-of-time
ranking, downside-calibration and stability gates. Recommendations use progressive disclosure and
remain downloadable and evidence-drillable.

## Consequences

Releases are larger but reproducible. Consultation latency and LLM dependence fall. Every live
verdict can be replayed against an exact atlas, policy and case. Expanding “the entire universe” now
has an auditable meaning: the whole governed coverage set, not an unsupported claim to all possible
real-world choices.

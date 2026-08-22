# ADR-NA-007: Provenance Is a Stored Evidence Graph

Status: Proposed  
Date: 2026-08-17

## Context

Users must move from recommendation to finding, score, scene, and source. Regenerating citations conversationally would be unreliable.

## Decision

Store typed provenance nodes and edges for source spans, parsed blocks, NKA statements, inferences, scores, observations, findings, recommendations, and compiled spans. UI drill-down traverses the graph deterministically.

## Consequences

Unsupported claims can be rejected and evidence remains inspectable. Storage and invalidation are more complex. Missing evidence makes a diagnostic claim non-authoritative rather than triggering model reconstruction.

# ADR-NA-009: Analyze Hierarchically, Not by One Giant Prompt

Status: Proposed  
Date: 2026-08-17

## Context

Published context windows can hold long text but local memory, latency, attention degradation, provenance, and revision invalidation make whole-script prompting fragile.

## Decision

Parse deterministically, analyze scene evidence packets, aggregate validated sequence/act results, and retrieve exact spans for questions. Whole-script prompts are exceptional, budgeted, and recorded.

## Consequences

The design works across hardware tiers and preserves evidence. Cross-scene synthesis needs explicit dependency graphs and tests. Long-context capability remains useful but is not canonical memory.

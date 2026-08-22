# ADR-NA-008: Use Immutable NKA Revisions

Status: Proposed  
Date: 2026-08-17

## Context

Create/Doctor/Revise requires undo, comparison, alternative directions, stale-analysis detection, and defensible lineage.

## Decision

Every accepted change creates a content-addressed NKA revision with parent(s) and typed change set. One project head advances atomically with optimistic concurrency. Undo is a new restoring descendant; history is not rewritten.

## Consequences

Analyses and compilations bind precisely to story state. Storage grows append-only and semantic merges require future design. MVP supports branching but no automatic merge.

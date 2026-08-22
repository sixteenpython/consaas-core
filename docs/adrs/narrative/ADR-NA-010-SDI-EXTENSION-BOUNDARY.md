# ADR-NA-010: Separate SDI from Product Extensions

Status: Proposed  
Date: 2026-08-17

## Context

The supplied paper is authoritative, but future product work may introduce genre patterns, retrieval methods, learned engagement models, or other screenplay theories.

## Decision

Canonical concepts and rules use the `sdi.*` namespace and cite the framework version. Non-SDI methods use `extension.<name>.*`, are labelled “Beyond SDI,” and cannot alter canonical SDI scores.

## Consequences

Users can distinguish framework diagnosis from experimental enhancement. Product evolution requires parallel reports or clearly composed views instead of quietly expanding what “SDI” means.

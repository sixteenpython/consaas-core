# ADR-NA-004: Local-Only Inference Behind a Port

Status: Proposed  
Date: 2026-08-17

## Context

Screenplays are unpublished intellectual property. Model capability and licensing evolve. Hard-coding Ollama or one model would couple business logic and weaken portability.

## Decision

All screenplay-bearing inference uses a provider-neutral `LocalLLM` port. The MVP Ollama adapter accepts loopback/local endpoints only. Model registry entries pin artifacts, license, runtime, parameters, and evaluated tasks.

## Consequences

No paid/external API is required and models are replaceable. Operators install model weights separately. Runtime conformance and hardware profiles become required product capabilities.

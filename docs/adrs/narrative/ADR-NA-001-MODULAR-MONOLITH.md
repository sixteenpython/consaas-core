# ADR-NA-001: Start as a Modular Monolith

Status: Proposed  
Date: 2026-08-17

## Context

Narrative Architect has several domain components but one product lifecycle, local deployment, and small initial team. Distribution would add privacy, failure, deployment, and versioning complexity without a proven scaling need.

## Decision

Build one Python deployable with strict domain/application/adapter package boundaries and ports. Streamlit is an adapter. Modules may later move behind processes without changing domain contracts.

## Consequences

Local installation and transactions remain simple; boundaries require architecture tests. Split only for measured isolation, scaling, or ownership needs. No microservices in MVP.

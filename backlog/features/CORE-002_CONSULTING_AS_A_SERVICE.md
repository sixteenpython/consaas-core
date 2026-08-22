---
id: CORE-002
mode: RELEASE
status: REVIEW
product: core
type: vertical-slice feature
owner: product-owner
created: 2026-08-23
dependencies: [CORE-001]
---

# Consulting as a Service

## User outcome

A user experiences an adaptive domain-expert consultation, can revise confirmed facts, understands
why each question matters, and receives the same reproducible evidence-backed decision.

## Acceptance criteria

1. Question selection responds to current case facts.
2. Conversation wording cannot mutate canonical facts or deterministic results.
3. Every confirmed revision is visible in session history.
4. Every product exposes a versioned decision-metric coverage catalog.
5. CareerSim evaluates overseas education ROI for Indian students across UG, master's and PhD.
6. The application remains useful without network or model inference.
7. Refresh, unit, integration, UI, type, lint, security and production smoke gates pass.

## Rollback

Revert the release and restore the retained 2026-08-22 promoted pointers.


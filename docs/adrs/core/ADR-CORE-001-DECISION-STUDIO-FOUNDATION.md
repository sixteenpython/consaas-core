# ADR-CORE-001: Launch the three-product Decision Studio as a bounded modular monolith

Status: Accepted
Date: 2026-08-22

## Decision

Add StartupEval to the approved portfolio and launch CareerSim, HouseWise and StartupEval through a
single ConSaaS Decision Studio Streamlit application. Each remains a domain product with its own
knowledge schema, questions, policy and engine. Only artifact lifecycle, refresh mechanics, model
contracts and reusable presentation primitives belong to Core.

The first release uses governed `GKA v0.1 Foundation` seed assets and an atomic monthly refresh. It
does not claim comprehensive coverage. Deterministic engines own verdicts; optional local or
free-hosted open-weight models may only narrate validated results.

## Why

The shared shell tests the factory thesis across three materially different domains while preserving
domain semantics. A bounded, runnable vertical slice gives evidence about genuine reuse before more
abstractions are promoted into Core.

## Alternatives rejected

- Three independent applications: duplicates lifecycle and UX infrastructure before learning.
- One universal decision schema: erases important domain meaning.
- LLM-owned recommendations: cannot provide deterministic replay or reliable evidence.
- Exhaustive-data claim at launch: unsupported and unsafe.
- Microservices: no measured isolation or scaling need.

## Consequences

The Constitution portfolio is updated. Public hosted synthesis requires a separate disclosed profile;
local inference remains the default architecture. New Core reuse candidates require evidence from at
least two implemented products and a later ADR.

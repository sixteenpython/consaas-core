---
id: CORE-004
mode: RELEASE
status: REVIEW
product: core
type: vertical-slice feature
owner: product-owner
created: 2026-08-23
dependencies: [CORE-003]
---

# Domain Decision Engines v1

## User outcome

Users receive three scenario-tested CareerSim or HouseWise options, or an evidence-backed StartupEval
Horse/Jockey verdict, through the existing conversational Decision Studio.

## Acceptance criteria

1. CareerSim uses complete economic cost, counterfactual NPV/IRR and top-three robust ranking.
2. HouseWise uses complete ownership cash flow, downside scenarios and property diligence gates.
3. StartupEval asks exactly eleven narrative questions and applies the documented 70/30 policy.
4. ConSaaS is `STRONG`; vague evidence cannot be `STRONG`.
5. Tagged immutable releases, provenance, rollback and all quality gates pass.

## Explicit exclusions

No programme admission, property title approval, startup success prediction or claim of exhaustive
knowledge coverage.

# ADR-CORE-004: Use domain-shaped deterministic engines over versioned decision universes

Status: Accepted
Date: 2026-08-23

## Decision

CareerSim and HouseWise will search a versioned option universe, simulate explicit downside, base
and upside scenarios, remove dominated choices and robustly rank three recommendations. StartupEval
will instead adjudicate exactly eleven natural-language founder answers against a versioned India
Problem Observatory using a deterministic Horse (70%) / Jockey (30%) policy.

All final calculations, gates, scores, rankings and verdicts remain deterministic. Language models
may interpret or explain a consultation turn but cannot create evidence or alter authoritative
outputs. Knowledge assets are coverage-bounded decision references, not claims of exhaustive truth.

## Why

The three products share artifact lifecycle, provenance, consultation and reporting infrastructure,
but they do not share one artificial decision algorithm. Education and property decisions compare
feasible investments; startup diligence tests the evidence for one proposition and its team.

## Alternatives rejected

- LLM-generated final recommendations: not reproducible or sufficiently auditable.
- One generic weighted score for all products: hides domain economics and creates false reuse.
- Prestige, property-price growth or startup novelty as a single objective: ignores downside and
  feasibility.
- Founder charisma or language fluency as a Jockey signal: discriminatory and non-evidentiary.
- Calling a curated first release exhaustive: creates false authority.

## Consequences

Product policy and schemas can evolve independently while the shared optimizer, artifact lifecycle,
consultation contracts and report model remain reusable. Forecasts must be labelled as scenarios.
HouseWise never approves a title or project without property-level diligence. CareerSim requires
offer-level verification. StartupEval rejects a proposition “in its current form,” never a person.

## Rollback

Revert the CORE-004 release commit and restore each `knowledge/releases/<product>/current.json`
pointer to the preceding immutable 2026-08-23 release. The tagged methodology releases remain
available for audit.

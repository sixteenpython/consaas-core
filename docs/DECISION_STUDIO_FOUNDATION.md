# ConSaaS Decision Studio — Foundation MVP

Status: Approved for implementation
Product decision: 2026-08-22

## Outcome

ConSaaS Decision Studio is one Streamlit application with three bounded specialist journeys:

- CareerSim — assess overseas education ROI for Indian students across UG, master's and PhD;
- HouseWise — compare Indian residential purchase locations;
- StartupEval — assess pre-seed through Series A ventures from founder or investor context.

The landing promise is: **We de-risk high-stakes decisions in real estate, higher education and
startup evaluation.** The system provides structured decision support, not financial, legal,
admission, valuation or investment advice.

## Foundation boundary

This release proves the complete product loop with governed seed knowledge. Each product owns a
`GKA v0.1 Foundation`: a versioned schema, source catalog, curated public-data seed, quality report,
content hash and promoted release pointer. It is not represented as exhaustive market coverage.

The shared monthly workflow is:

`source catalog -> snapshots -> candidate GKA -> validation -> manifest -> atomic promotion`

A failed candidate never moves the promoted pointer. Re-running the same effective date and inputs
is idempotent. Source rows record URL, publisher, observation date and confidence. Sources that
cannot be safely machine-ingested are explicitly marked `reference_only`; the refresh reports them
as such instead of pretending to scrape them.

## Runtime architecture

The MVP is a modular monolith.

```text
Streamlit UI
  -> consultation service
      -> product question contract
      -> canonical Case Knowledge Asset with revisions (session-only)
      -> product decision engine
          -> promoted GKA
          -> versioned decision policy
          -> deterministic score/verdict/options
      -> optional open-model narrator
          -> validated wording only; cannot change scores or verdict
  -> evidence, assumptions, sensitivity and downloadable result
```

Products own their questions, GKA schema, seed knowledge, policy and scoring. Core owns artifact
identity, hashing, validation, candidate isolation, promotion and provider-neutral model contracts.
No product imports another product.

## Deterministic and model boundary

Deterministic code owns information-value question selection, answer validation, eligibility gates, calculations,
weights, ranking, verdict thresholds, evidence references, confidence/data-sufficiency, manifests
and report structure. A configured open-weight model may translate the immutable decision result
into concise consultant prose using the product `SKILL.md`. Model output is untrusted, schema
validated and never allowed to alter canonical numbers, options, evidence or verdict.

Hosted synthesis is optional and disclosed. The application remains fully useful without a key.
Local Ollama remains the private profile. No paid inference service is required.

## Privacy and safety

- anonymous and session-only;
- no durable storage of personal, property or startup inputs;
- no user input in logs;
- downloads are produced in memory;
- external synthesis is opt-in and clearly disclosed;
- insufficient information produces a typed `NEEDS_MORE_EVIDENCE` outcome;
- all recommendations expose assumptions, limitations and what could change the verdict.

## Initial coverage

- CareerSim: Indian students assessing overseas UG, master's and PhD options represented by a
  governed illustrative archetype set.
- HouseWise: Bengaluru, Mumbai, Pune, Hyderabad, Chennai, Delhi NCR and Kolkata locality archetypes.
- StartupEval: India-first sector/stage benchmarks for founder and investor evaluation.

## Rollback

The Decision Studio is an isolated root entrypoint. Narrative Architect remains independently
runnable under `narrative/`. Rollback is either a Git revert of this feature or repointing the
Streamlit deployment. GKA rollback changes only a product's promoted release pointer.

## Known limitations

Seed data is intentionally small and illustrative. Costs, property indicators, rankings and startup
benchmarks can change and must be independently verified before a real decision. The monthly
pipeline is production-shaped, but several official sources remain reference-only until stable,
licensed machine-readable endpoints are confirmed.

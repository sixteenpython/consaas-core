# Consulting as a Service — Decision Studio v0.3

Status: Implemented for review  
Effective: 2026-08-23

## Outcome

Decision Studio separates five responsibilities:

1. the Virtual Domain Consultant conducts an adaptive, plain-language conversation;
2. the session-only Case Knowledge Asset stores confirmed facts and revisions;
3. the Grand Knowledge Asset supplies governed domain evidence and a decision-coverage catalog;
4. the deterministic product engine owns scores, options and verdicts.
5. an optional provider-free browser model interprets and words turns through a typed validation
   gate.

The conversation is not canonical memory. Model wording and proposed actions are never
authoritative. Free-form conversation, epistemic case states and the live Decision Position are
specified in [Conversational Decision Intelligence](./CONVERSATIONAL_DECISION_INTELLIGENCE.md).

## Expert conversation loop

For each confirmed answer the application acknowledges the fact, explains its governed decision
implication, recomputes the information value of unresolved topics and asks the most useful next
question. Question order is therefore adaptive rather than a fixed array. Users can revise confirmed
facts; the prior value and revision reason remain visible for the anonymous session.

Optional open-weight wording is provider-neutral. Local Ollama is selected with
`CONSAAS_OLLAMA_MODEL`; the hosted demonstration profile uses an explicitly configured key and
disclosure. Both routes return only acknowledgement and implication fields. Invalid model output
falls back to deterministic expert wording and cannot mutate the Case Knowledge Asset.

## Knowledge coverage

Each product now publishes a versioned metric catalog with:

- metric identity and plain-language label;
- the decision it informs;
- current coverage state;
- freshness expectation;
- preferred authoritative source.

Coverage states are `available`, `planned_connector`, and `required_case_evidence`. This makes
comprehensiveness measurable without inventing unavailable property, programme or company facts.
The monthly refresh validates and promotes both observations and the metric catalog under one
artifact hash.

## CareerSim boundary

CareerSim is for Indian students assessing the ROI and downside risk of overseas undergraduate,
master's and PhD study. It considers all-in INR-normalised cost, funding structure, destination,
post-study work pathways, relevant employment evidence, overseas versus India-return income,
payback horizon and compound admission/visa/debt risk. It does not predict admission, employment,
salary or migration outcomes.

## Privacy and rollback

Cases remain session-only. Hosted wording remains optional and disclosed. Rollback is a Git revert
plus restoration of the retained 2026-08-22 GKA pointers; no retained release is rewritten.

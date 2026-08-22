# ConSaaS Reuse Candidates

## Promotion rule

Narrative Architect may consume approved Core contracts, but a new abstraction is promoted only when Vriddhi and Narrative Architect—or another second product—demonstrate the same semantics. Shared code is not justified by similar names alone.

## Reuse now

| Capability | Core status | Narrative use |
|---|---|---|
| Artifact envelope, hashes, lineage | Established architecture | source PDFs, NKA, analyses, compiled scripts |
| Candidate validation and immutable release principles | Proven in Vriddhi | parser imports, NKA revisions, analyses, compiler artifacts |
| Validation result/error taxonomy | Cross-domain | schemas, invariants, parse/analysis quality |
| Report/ViewModel separation | Cross-domain | SDI scorecards and evidence UI |
| Plugin/port boundaries and conformance tests | Core design | LLM, parser, store, compiler adapters |
| Structured provenance and audit events | Cross-domain requirement | recommendation-to-source drill-down |

## Strong candidates to prove here

| Candidate | Why potentially reusable | Promotion evidence needed |
|---|---|---|
| Local LLM abstraction | future products need replaceable inference | two products share task-neutral request/result semantics |
| Model registry/license gate | all LLM products require reproducibility and governance | successful Narrative plus another product integration |
| Immutable revision store/change-set protocol | evolving knowledge assets need history | HouseWise/CareerSim demonstrates compatible semantics |
| Evidence graph and claim taxonomy | recommendations need traceability | map cleanly to Vriddhi recommendation evidence |
| Local artifact/privacy profile | sensitive product data | second private-data product validates controls |
| Streamlit conversation/evidence components | reusable interaction mechanics | domain-free view models work in another app |
| Golden fixture/model-evaluation harness | probabilistic plugins need promotion gates | task adapters remain product-owned |

## Remain Narrative-specific

NKA entity schema, screenplay grammar, scene ordering semantics, screenplay compiler, SDI pillars/rubric/scales, momentum rules, character/arc interpretation, script-doctor language, and screenplay UX. These encode domain meaning and must not enter Core.

## Anti-patterns

- Do not rename NKA to a universal chat memory model.
- Do not force Vriddhi’s monthly release cadence onto interactive revisions.
- Do not make `DataFrame` or Streamlit session state a Core contract.
- Do not create one universal “score engine” hiding domain rubrics.
- Do not put model prompts in Core merely because multiple products use LLMs.

## Measurement

Track reused package/code percentage, adapter conformance, product-specific schema/rule volume, duplicated lifecycle code, and number of cross-domain contract exceptions. The target is useful reuse without reducing Narrative Architect to Vriddhi with different nouns.

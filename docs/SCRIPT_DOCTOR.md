# Script Doctor

## Role

The Script Doctor converts validated SDI observations into prioritized, evidence-grounded improvement options and supports follow-up conversation. It cannot change scores, source text, or the NKA head.

## Finding model

```yaml
finding_id: id
analysis_revision_id: id
type: extracted_fact | inferred_element | framework_score | diagnostic_observation | recommendation
scope: scene | sequence | act | character | dialogue | whole_script
severity: note | opportunity | concern | critical
summary: string
mechanism: string
sdi_concepts: [plot, scenes, characters, dialogue, momentum, catharsis]
evidence_refs: [id]
score_refs: [id]
confidence: 0..1|null
limitations: [string]
```

Recommendations additionally contain expected narrative effect, affected entities, alternatives, trade-offs, author decision required, and proposed patch/template only when requested.

## Generation pipeline

1. Deterministic queries select observations, score patterns, and evidence.
2. The local model explains the diagnosed mechanism using only the packet.
3. A validator checks SDI terminology, claim type, evidence coverage, prohibited success predictions, and numeric consistency.
4. Deterministic prioritization considers severity, breadth, confidence, dependency, and revision staleness.
5. The report layer assembles overview and drill-down views.

## Conversation

Questions such as “why 2/5?” use stored assessment evidence, not a fresh untracked opinion. “Which scenes?” returns stable scene IDs and source links. “Should I remove it?” must consider whether the scene advances plot, deepens character, intensifies tension, or supports later setup/payoff, then present retain/revise/merge/remove options. The human chooses.

## Recommendation to revision

A recommendation can generate a proposed NKA change set only on explicit request. The proposal identifies generated content, affected continuity, and diagnostics to rerun. Acceptance creates a descendant revision; the original finding remains tied to its original analysis.

## Prioritization language

The product says “highest-leverage under SDI,” not “guaranteed improvement.” It distinguishes weaknesses from deliberate low-intensity setup and flags parser/inference uncertainty before prescriptive advice.

## MVP outputs

- Four-pillar overview with evidence coverage.
- Weak-scene and low-impact-run findings.
- Character/arc observations derived from scene evidence.
- Pointed improvement options with drill-down.
- Evidence-grounded conversational answers.
- Before/after diagnostic comparison after user-approved revision.

# SDI Diagnostic Engine

## Authority and scope

The supplied SDI manuscript is the authoritative framework. The engine implements only its named concepts: four pillars, scene scoring, audience dynamics/catharsis, momentum heartbeat, and the stated narrative paradigms/rules. Any additional heuristic is namespaced `extension.*` and visibly labelled “Beyond SDI.”

## Input and output

Input is a validated NKA revision plus source/provenance index and analysis configuration. Output is an immutable `SDIAnalysis` containing per-scene pillar assessments, SIS values, momentum series, aggregate pillar summaries, detected diagnostic observations, uncertainty, evidence, and engine manifest.

## Stages

1. Freeze revision, scene selection, SDI policy version, and scale definitions.
2. Build scene evidence packets from source text and NKA facts.
3. Obtain structured qualitative assessments for Plot, Scenes, Characters, and Dialogue.
4. Validate each assessment has evidence and rubric-conformant score/rationale.
5. Calculate SIS deterministically.
6. Calculate momentum and declared SDI thresholds deterministically.
7. Aggregate scene evidence into pillar and character/sequence views without inventing scores.
8. Create typed observations; pass them to Script Doctor for recommendations.

## Four Pillars

- **Plot:** creation/escalation of central conflict, stakes, obstacles, causal progression, meaningful resolution contribution.
- **Scenes:** clear micro-objective and outcome; advances plot, deepens character, or intensifies emotional tension.
- **Characters:** motivations, recognizable traits, consequential decisions, and arcs that support the plot.
- **Dialogue:** interaction of text, subtext, and context, aligned with motivation and scene objective.

The LLM interprets evidence and proposes rubric levels. The engine validates level definitions, stores exact rationale/evidence, and owns arithmetic. A score without resolvable evidence is invalid.

## Analysis statuses

`complete`, `complete_with_uncertainty`, `needs_parse_review`, `insufficient_evidence`, or `failed`. Low-confidence parsing can block exact scene diagnosis while allowing clearly labelled provisional analysis.

## Re-analysis

Analyses are revision-bound. Changing any affected story statement marks dependent scene and aggregate analyses stale via provenance edges. MVP may recompute the full script; incremental invalidation is a later optimization, not a semantic change.

## Claims boundary

The engine reports framework-relative diagnosis, not audience response prediction. “Likely pacing weakness under the SDI rubric” is permitted; “viewers will abandon the film” is not. Case-study patterns in the paper are illustrative, not training truth.

## Framework ambiguities

The paper uses both per-pillar/mean `0–5` and total `/20`. The engine stores and labels all three representations. Scene-based and page-based cadence rules remain separate policies. No conversion or threshold is implicit.

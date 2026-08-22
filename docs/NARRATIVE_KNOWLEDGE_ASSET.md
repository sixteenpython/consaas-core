# Narrative Knowledge Asset

## Role

The NKA is the canonical, versioned representation of the current story. Conversation, uploaded PDFs, compiled scripts, diagnostics, and reports are sources or projections. None may silently replace it.

## Aggregate envelope

```yaml
schema_version: narrative-nka/1.0
project_id: uuid
revision_id: content-addressed-id
parent_revision_ids: [id]
title: string
format: feature | short | episode | bounded_script | unknown
language: BCP-47
status: seed | developing | compiler_ready | compiled | imported | under_revision
created_at: utc-instant
created_by: user | parser | expert-assisted
source_artifact_ids: [id]
change_set_id: id
entities: {...}
story_structure: {...}
provenance_index: {...}
quality: {...}
```

## Canonical payload

- **Story identity:** title, logline, premise, genre labels, intended format, language, tone, audience constraints.
- **Meaning:** themes with statement, dramatic question, supporting/opposing evidence, status.
- **Plot:** central conflict, sub-conflicts, stakes, goals, obstacles, turning points, setup/payoff links.
- **Structure:** acts, sequences, beats, episodes where relevant; ordered membership and purpose.
- **Characters:** stable ID, name/aliases, role, traits, external objective, internal need, motivations, fears, beliefs, secrets, relationships, arc states, first/last scene.
- **World:** locations, time periods, timeline events, rules, continuity facts.
- **Scenes:** stable ID, ordinal, optional source scene number, heading components, location/time, participating characters, objective, obstacle/conflict, outcome, emotional shift, plot effects, setup/payoff, dialogue blocks, status.
- **Dialogue:** speaker, text, addressee, text meaning, inferred subtext, context, provenance.
- **Open questions:** unresolved author choices, contradictions, missing dependencies, compiler blockers.

## Statement model

Narrative values that may be uncertain use a statement wrapper:

```yaml
value: "Meera hides the letter to protect Arun"
epistemic_status: user_asserted | extracted | inferred | proposed
confidence: 0.0..1.0     # only for extraction/inference
evidence_refs: [evidence-id]
introduced_in_revision: id
last_confirmed_in_revision: id|null
model_run_id: id|null
```

An inference never overwrites a user assertion. Conflicts coexist as candidates until resolved by a command.

## Identity and ordering

Entity IDs are stable UUIDs and do not encode names or ordinals. Scene order uses an explicit ordered list; reordering does not change scene IDs. Display scene numbers are deterministic projections. Deletion is a tombstoned change event so old evidence remains resolvable.

## Mutation protocol

All changes use typed commands producing JSON-Patch-like domain operations: add entity, revise field, merge identity, split scene, reorder scenes, delete/tombstone, accept/reject inference, and resolve contradiction. Each change set includes base revision, actor, reason, source message/evidence, and expected invariants. The UI previews material patches when authorial intent is ambiguous.

## Invariants

- All references resolve or are explicitly external/unresolved.
- Scene order is unique and total for active scenes.
- Dialogue speakers resolve to a character or declared off-screen voice.
- Act/sequence membership cannot duplicate a scene at the same hierarchy level.
- Timeline contradictions are findings, not silently normalized facts.
- Imported source text is immutable; edits create NKA values with lineage.
- Diagnostics and compilations name the exact revision analyzed.

## Derived, not canonical

SIS scores, momentum series, findings, recommendations, retrieval embeddings, UI summaries, compiler page numbers, and conversational summaries are derived artifacts. They link to an NKA revision but are not embedded as authoritative story facts.

## Minimum compiler-ready profile

An MVP script can compile when it has a title, format, ordered active scenes, a valid scene heading or declared bounded-script equivalent for each scene, action or dialogue content, resolved speakers, and no blocking structural errors. Premise, theme, arcs, and SDI annotations improve expertise but are not mandatory for syntactic compilation.

## Schema evolution

Schemas use semantic versions. Additive fields are minor; changed meaning or removed invariants are major. Migrations create a descendant revision, preserve prior payload/hash, and record migration code version. Unknown extension fields are retained under namespaced `extensions`.

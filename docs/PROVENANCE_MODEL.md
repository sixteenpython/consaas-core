# Provenance Model

## Goal

Every important claim supports the path:

`Recommendation -> Finding -> Observation -> Score/Rationale -> Scene/NKA entity -> Source span -> Source screenplay`

## Evidence graph

Nodes:

- source artifact and version;
- source page/block/span;
- parsed screenplay element;
- NKA statement/entity/revision;
- model inference;
- pillar assessment and SIS calculation;
- momentum observation;
- diagnostic finding;
- recommendation;
- compiled artifact/span;
- conversation claim and accepted change set.

Edges use typed relations: `extracted_from`, `inferred_from`, `asserted_by`, `derived_from`, `calculated_from`, `supports`, `contradicts`, `recommends_change_to`, `compiled_from`, and `supersedes`.

## Evidence reference

```yaml
evidence_id: id
artifact_id: id
artifact_hash: sha256
page: 12|null
block_id: id|null
line_start: 4|null
line_end: 11|null
char_start: 120|null
char_end: 412|null
quoted_text_hash: sha256
display_excerpt: local-derived excerpt
```

Coordinates are deterministic and source-bound. Display excerpts are conveniences; the source span is authoritative.

## Claim taxonomy

- `extracted_fact`: directly represented in source/user statement.
- `user_asserted`: explicitly established by the author.
- `inferred_element`: model interpretation with confidence/evidence.
- `framework_score`: SDI rubric output plus deterministic arithmetic.
- `diagnostic_observation`: rule or grounded synthesis over evidence/scores.
- `recommendation`: proposed action and expected framework-relative effect.

UI styling and API schemas preserve these types. A recommendation cannot masquerade as a fact.

## Run manifest

Every derived artifact records input revision/hashes, code version, parser/engine/policy version, model registry entry/digest, runtime, prompt/schema version, parameters/seed, context evidence IDs, timestamps, validation results, and parent run IDs.

## Drill-down behavior

The UI traverses stored graph edges; it never asks an LLM to reconstruct provenance. If an edge is missing or source artifact unavailable, the claim is labelled unverified and cannot support an authoritative finding.

## Privacy and retention

Evidence remains project-local. Logs contain IDs/hashes, not screenplay excerpts. Export packages include only explicitly selected source evidence and warn about unpublished-IP exposure. Deleting a project deletes all content-bearing nodes subject to local backup policy.

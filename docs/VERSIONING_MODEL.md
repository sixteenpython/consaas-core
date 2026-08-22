# Versioning Model

## Objects with independent versions

- source artifact version;
- NKA schema version;
- immutable NKA content revision;
- conversation summary/prompt version;
- parser and parse revision;
- SDI framework/policy and analysis revision;
- model registry entry and prompt schema;
- compiler/profile and compiled artifact;
- report/view-model version.

No single application version substitutes for these identities.

## NKA revision graph

An NKA revision is immutable and content-addressed from canonical payload, schema, parent(s), and accepted change set. Normal editing creates one-parent descendants. Branching permits alternative story directions. MVP supports one active head and explicit branch creation; automatic merge is prohibited. A future merge must surface semantic conflicts for human resolution.

## Command concurrency

Every mutation includes `base_revision_id` and idempotency key. If project head moved, reject with a comparison and rebase/redo options. A transaction writes change set, revision, provenance edges, and head pointer atomically.

## Undo and deletion

Undo creates a new descendant whose content restores a prior state; it does not erase history. Entity deletion tombstones the entity in the new revision. Hard project deletion is a separate privacy operation that removes local content and backups according to policy.

## Derived artifacts

Parsing, analysis, compilation, embeddings, and reports name exact input revisions and hashes. They never mutate when the NKA changes; they become `current`, `stale`, or `superseded`. UI defaults to current artifacts and can compare historical ones.

## Schema migration

Migration functions are versioned, deterministic, and tested forward. They create a descendant artifact with `migrated_from`, migration version, warnings, and hashes. There is no silent migration during read. Backward export is optional and explicitly lossy where necessary.

## Model/prompt changes

Re-running the same NKA with a new model, quantization, runtime, prompt, or inference parameters creates a new analysis revision. Comparison reports separate screenplay changes from assessor changes.

## Compilation lineage

Compiled scripts are immutable releases named by NKA revision and compiler manifest. Recompilation after formatting-only changes is distinguishable from story-content revisions. Imported PDFs remain source artifacts even if an equivalent NKA later compiles.

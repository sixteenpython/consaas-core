# Screenplay Compiler

## Objective

Compile one NKA revision into a deterministic, professionally formatted screenplay or explicitly bounded script. The compiler translates established content; it does not invent missing story decisions.

## Inputs and outputs

Input: NKA revision, compilation profile, title-page metadata, formatting configuration, and optional selection bounds. Output: screenplay document/PDF, compilation manifest, page/line/source map, warnings, and readiness report.

## Compilation stages

1. Validate compiler-ready invariants and selection bounds.
2. Resolve ordered scenes and active content from the named revision.
3. Materialize screenplay elements: scene headings, action, cues, parentheticals, dialogue, transitions.
4. Apply deterministic typography, indentation, spacing, pagination, continuations, and scene numbering.
5. Render output and generate `nka_entity -> compiled span/page` provenance.
6. Reopen and structurally verify the artifact; render-test in CI fixtures.

## Authoring boundary

Missing headings, action, or dialogue become compiler blockers or warnings. An optional pre-compilation expert workflow may propose content, but only accepted changes enter a new NKA revision before compilation. The compiler itself is pure and replayable.

## Profiles

- `standard_screenplay_mvp`: title page and conventional scene/action/dialogue layout.
- `bounded_script_mvp`: selected acts, sequences, or scenes with an explicit “partial draft” label.
- Future extensions: Fountain/FDX import-export, television profiles, localized conventions. These are beyond SDI and must be labelled product extensions.

## Determinism

Identical NKA hash, compiler version, fonts, profile, and configuration must produce semantically identical output. Binary PDF hashes may vary by metadata; a canonical content/layout manifest is the replay assertion. Generated timestamps live in the manifest, not content unless requested.

## Revision loop

A compiled artifact records its source revision. Doctoring it may use the compiler source map to recover exact NKA IDs. Accepted recommendations create a descendant NKA revision; recompilation creates a new artifact rather than overwriting the prior screenplay.

## MVP readiness report

Report blocking errors, non-blocking gaps, unresolved speakers, missing/invalid headings, empty scenes, uncertain ordering, and partial/bounded status. “Compiled successfully” means syntactically complete for the selected bounds, not narratively strong.

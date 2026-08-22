# Testing Strategy

## Pyramid

1. Pure domain tests for NKA invariants, patches, ordering, scale arithmetic, thresholds, and version hashes.
2. Contract tests for LLM, parser, stores, compiler, provenance, and report ports.
3. Component tests with recorded/local fakes and golden screenplay fixtures.
4. Vertical-slice integration tests through application services.
5. Headless Streamlit smoke tests for both modes and all required views.
6. Human expert evaluation for interpretive quality and authorial experience.

## Fixture corpus

Use synthetic or explicitly licensed scripts covering feature, short, episodic, thriller/deceptive setup, dialogue-heavy, weak middle, ambiguous formatting, revised scenes, and partial/bounded drafts. Never commit unpublished customer screenplays. SDI papers define rubric fixtures but are not empirical ground truth.

## Deterministic tests

- parser block order/source-span coverage and malformed PDF handling;
- stable IDs, revision atomicity, conflict/retry/idempotency, undo and migration;
- exact SIS sum/mean and named threshold behavior;
- momentum runs, missing-score gaps, scene reorder comparison;
- compiler semantic replay, readiness failures, source mapping;
- evidence graph traversal and broken-edge rejection;
- report numeric consistency and prohibited success claims.

Property tests cover arbitrary scene reorder/patch sequences and score ranges. Failure injection covers interrupted persistence, parser crash, model timeout, invalid JSON, and out-of-memory.

## Probabilistic evaluation

Versioned benchmark cases score structured-output validity, extraction precision/recall, evidence citation precision/recall, contradiction detection, motivation/conflict/subtext usefulness, SIS exact and adjacent agreement with expert raters, unsupported claims, recommendation grounding, continuity across turns, and unauthorized creative mutation.

Run models repeatedly where sampling exists; publish distributions and regressions. A model upgrade cannot be approved on generic benchmarks alone.

## Privacy/security tests

Assert no non-loopback inference endpoint, no screenplay text in logs/telemetry, path traversal rejection, PDF resource limits, local artifact access boundaries, export consent, model digest allowlist, and secure project deletion behavior.

## Acceptance gates

Slice 1 requires complete conversational-to-NKA-to-compiler workflow, reload continuity, undo, and zero silent material mutations. Slice 2 requires parser provenance coverage, valid SDI arithmetic, evidence drill-down, and grounded doctor answers. Performance gates are hardware-profile specific.

## Manual screenplay review

Before a release, a screenplay expert reviews representative conversations and score rationales. Engineering validates arithmetic/provenance; screenplay reviewers validate interpretation. Disagreement is captured as evaluation data, not hidden by averaging.

# Narrative Architect Architecture

## Product definition

Narrative Architect is a local-first Virtual Screenplay Expert with two equal modes: **Create** develops a story through conversation and compiles it; **Doctor** parses an existing screenplay, applies SDI, and supports evidence-grounded diagnosis. Both operate on the same canonical Narrative Knowledge Asset (NKA).

`Chat is the experience; SDI is the brain; NKA is memory; Compiler is creation; Diagnostic Engine is the script doctor.`

The product diagnoses screenplay construction according to SDI. It never predicts commercial or cinematic success.

## Modular monolith

The MVP is one Python application with explicit internal packages and ports:

```text
Streamlit UI
  -> Application services / use cases
     -> Conversation orchestrator -> Virtual Screenplay Expert
     -> NKA command/query services -> version store
     -> Create services -> Screenplay Compiler
     -> Doctor services -> Parser -> SDI Engine -> Script Doctor
  -> Ports: LocalLLM, ArtifactStore, VersionStore, VectorIndex, PDFExtractor
  -> Local adapters: Ollama, filesystem/SQLite, local PDF tools
```

No module communicates through Streamlit session state as a system of record. No domain module imports Streamlit or Ollama. No LLM writes persistence directly.

## Domain boundaries

- `narrative.domain`: NKA entities, invariants, patches, evidence references.
- `narrative.application`: create/doctor workflows, transactions, permissions, orchestration.
- `narrative.conversation`: dialogue policy, context assembly, expert response plans.
- `narrative.create`: elicitation, story gaps, compiler readiness, screenplay compiler.
- `narrative.doctor`: screenplay parsing, SDI scoring, momentum, findings, recommendations.
- `narrative.llm`: provider-neutral tasks, registry, prompts, structured-output validation.
- `narrative.provenance`: source spans, claim lineage, evidence traversal.
- `narrative.persistence`: SQLite metadata, content-addressed local artifacts, migrations.
- `narrative.reporting`: scorecards, evidence view models, screenplay exports.
- `narrative.ui`: Streamlit composition only.

## Core flows

**Create:** message -> intent/evidence extraction -> proposed NKA patch -> invariant check -> user confirmation policy -> new NKA revision -> expert response -> readiness -> compiler -> screenplay artifact.

**Doctor:** PDF -> immutable source artifact -> deterministic layout extraction -> screenplay parse -> structured NKA import -> human review of uncertainty -> SDI analysis -> findings/recommendations -> evidence-grounded conversation.

**Continuous loop:** Create -> Compile -> Doctor -> approved revisions -> Recompile -> re-diagnose. Compiled and imported screenplays are versioned projections of an NKA revision, never separate truth.

## State and transactions

A workspace contains a project, source artifacts, NKA revision graph, conversations, analyses, findings, compiled scripts, and model/run manifests. Commands use optimistic concurrency with `base_revision_id`. A valid mutation creates a new immutable revision and advances the project head atomically. Analyses are bound to one revision and become stale when the head changes.

## Trust boundaries

- Screenplay content and inference remain local.
- LLM output is untrusted structured input until schema and domain validation pass.
- Deterministic services own IDs, scene order, arithmetic, thresholds, versioning, persistence, provenance, and assembly.
- Creative changes are proposals; the human remains author and approves material invention or replacement.
- Every answer distinguishes `extracted`, `user_asserted`, `inferred`, `framework_score`, `diagnostic_observation`, and `recommendation`.

## Non-functional MVP targets

- Recoverable local persistence and atomic NKA updates.
- No network call containing screenplay content.
- Evidence path from recommendation to source span.
- Runnable without a GPU using a reduced model profile, with graceful performance disclosure.
- Deterministic replay for parsing, scoring, momentum, compilation, and report assembly.
- Model/prompt replay metadata for probabilistic tasks.

## Deliberate exclusions

Microservices, collaborative editing, cloud synchronization, autonomous rewrites, production prediction, biometric engagement, final-draft interchange, OCR, fine-tuning, and multi-user tenancy are outside the first MVP unless promoted by the roadmap.

# Local LLM Architecture

## Boundary

All screenplay-bearing inference is local. Business logic calls a `LocalLLM` port; it does not import Ollama libraries or model-specific prompt syntax.

```python
class LocalLLM(Protocol):
    def capabilities(self, model_id: str) -> ModelCapabilities: ...
    def complete(self, request: CompletionRequest) -> CompletionResult: ...
    def embed(self, request: EmbeddingRequest) -> EmbeddingResult: ...
    def health(self) -> RuntimeHealth: ...
```

`CompletionRequest` includes task ID/version, messages, evidence context, JSON Schema, temperature, seed where supported, context/output budgets, timeout, stop policy, and privacy classification. `CompletionResult` includes validated structured output, token counts, timing, runtime/model digest, effective parameters, and warnings.

## Adapters

MVP adapter: local Ollama HTTP endpoint bound to loopback. Future local adapters may support llama.cpp, MLX, vLLM, or Transformers. Equivalent adapters must meet the same structured-output, cancellation, health, provenance, and no-network conformance suite.

## Task profiles

- `expert_conversation`: nuanced counsel and next question; moderate creativity.
- `nka_extraction`: schema-constrained facts/patch candidates; low temperature.
- `scene_interpretation`: objectives, conflict, motivations, subtext with evidence.
- `sdi_assessment`: four independent rubric assessments; low temperature.
- `doctor_recommendation`: evidence-bounded options; moderate creativity.
- `hierarchical_synthesis`: combine validated scene summaries; low temperature.
- `embedding`: local retrieval vectors; no generation.

Model selection is task-profile based through the registry. One deployment can route different tasks to different models without changing domain code.

## Long screenplay strategy

Context length is not memory. Parse first; analyze scene evidence packets; aggregate sequences/acts hierarchically; retrieve exact source spans for conversation. Whole-script prompts are exceptional and recorded. Summaries carry revision and evidence dependencies and are invalidated after related edits.

## Structured output

Use JSON Schema-constrained outputs and validate again in application code. Ollama documents local schema-constrained structured outputs and recommends low temperature for reliability: [Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs). Models never calculate SIS totals or commit NKA changes.

## Privacy and network controls

- Default runtime URL must be loopback or Unix socket.
- Reject non-local endpoints unless a future explicit product edition and policy permit them; MVP has no such mode.
- Disable telemetry/download during screenplay processing; model acquisition is a separate operator action with no project data.
- Prompts/responses remain local encrypted/project-scoped artifacts according to retention settings.
- Do not log screenplay text in application logs.

## Failure behavior

Unavailable/insufficient models produce a capability error and suggested local profile. Invalid structured output retries with a bounded repair prompt; after exhaustion, no mutation occurs. Context overflow triggers smaller evidence packets/hierarchical analysis, never silent truncation.

## Evaluation

Registry promotion requires Narrative Architect task fixtures: extraction F1, schema validity, evidence citation precision/recall, SIS adjacent/exact agreement, contradiction detection, authorial-control violations, unsupported-claim rate, latency, peak memory, and long-context degradation.

# Model Registry

## Purpose

The registry makes model choice explicit, reproducible, hardware-aware, and replaceable. Product code asks for a task profile, never a raw model name.

The bootstrap's executable registry is `factory/model_registry.json`; parsing and policy live in `core/ai/registry.py`. Its entries are candidates for local evaluation, not claims of benchmark superiority. Product code must use the Core AI contract and resolver rather than importing a runtime SDK or naming a model directly.

## Registry entry

```yaml
id: qwen3-30b-a3b-q4-local
family: qwen3
publisher: Qwen
artifact_uri: ollama://qwen3:30b-a3b-q4_K_M
artifact_digest: sha256:...
license: Apache-2.0
license_uri: https://...
license_reviewed_at: 2026-08-17
runtime: ollama
runtime_min_version: "..."
capabilities:
  chat: true
  structured_output: true
  tools: true
  embeddings: false
  published_context_tokens: 131072
approved_context_tokens: 32768
hardware: {min_ram_gb: ..., recommended_vram_gb: ...}
tasks: [expert_conversation, nka_extraction, scene_interpretation, sdi_assessment]
prompt_compatibility: {min: 1, max: 1}
benchmark: {suite_version: ..., status: candidate, report_id: ...}
privacy: {local_only: true, telemetry: prohibited}
status: candidate | recommended | fallback | blocked | retired
```

## Resolution

`ModelResolver.resolve(task, hardware, policy)` filters by capability, license approval, local-only endpoint, context/output budget, memory, benchmark threshold, and status. It returns a model plus exact inference policy. Automatic fallback is allowed only within a declared ordered profile and is recorded; it cannot change an authoritative analysis unnoticed.

## Configuration layers

Repository defaults -> installation registry -> project preference -> per-run explicit override. Lower layers may narrow but not bypass license/privacy/policy. Secrets are irrelevant for local inference and must not appear in entries.

## Lifecycle

`discovered -> license_review -> benchmarked -> candidate -> recommended -> deprecated -> retired/blocked`. Upgrading model tag, quantization, prompt template, runtime, or effective context creates a distinct entry. Mutable tags are resolved to digests before use.

## Runtime health

Startup checks endpoint locality, runtime version, model presence/digest, memory estimate, structured-output probe, context probe, and task smoke tests. Missing models produce operator instructions; the app never downloads multi-gigabyte weights during a user request.

## Governance

Registry changes require a model evaluation report and license evidence. A blocked entry cannot be selected even by project configuration. Historic projects retain manifests sufficient to identify prior runs; model binaries may follow separate retention policy.

The bootstrap registry records model families, declared Apache-2.0 licensing, task capabilities, and coarse RAM/context constraints. Before production use, replace mutable runtime tags with digests, verify license artifacts, benchmark on target hardware and representative product cases, and record quantization/runtime/prompt versions.

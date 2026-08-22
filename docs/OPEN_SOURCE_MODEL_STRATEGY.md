# Open/Open-Weight Model Strategy

## Selection principles

Models are selected by Narrative Architect task performance, hardware fit, local runtime maturity, structured-output reliability, context behavior, and license—not popularity. Apache-2.0 models are preferred because they are clear for commercial modification and distribution. Each release records exact model artifact/digest and license review date.

## MVP candidate set (architecture baseline)

| Profile | Candidate | Why evaluate | License / published capability | Position |
|---|---|---|---|---|
| Quality local | Qwen3 30B-A3B | MoE efficiency, tool/structured workflows, reasoning/non-reasoning modes, 128K context | Apache-2.0; Qwen recommends local runtimes including Ollama and llama.cpp in its [official Qwen3 release](https://qwenlm.github.io/blog/qwen3/) | Preferred quality baseline, subject to task benchmark |
| Balanced dense | Mistral Small 3.2 24B | instruction following, reduced repetition, mature local quantizations | Apache-2.0 on the [publisher model repository](https://huggingface.co/mistralai/Mistral-Small-3.2-24B-Instruct-2506) | Challenger for dialogue/creative counsel |
| Accessible | Granite 3.3 8B Instruct | smaller footprint, 128K published context, instruction/reasoning focus | Apache-2.0; [IBM model card](https://huggingface.co/ibm-granite/granite-3.3-8b-instruct) | CPU/16GB-class fallback and extraction challenger |
| Workstation research | Mistral Small 4 119B-A6B | 256K context, hybrid instruct/reasoning, document extraction | Apache-2.0; [Mistral model card](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) | Not default: weight footprint is too large for mainstream MVP hardware |
| Embedding | Qwen3 Embedding 0.6B or 4B | long-text/multilingual retrieval family and local deployment | Apache-2.0; [publisher model card](https://huggingface.co/Qwen/Qwen3-Embedding-4B) | 0.6B default candidate; 4B quality profile |

Gemma 3 is a useful benchmark but requires acceptance of Google’s custom Gemma terms rather than Apache-2.0; it is not the default despite its 128K and multimodal capabilities ([Gemma model card and terms gate](https://huggingface.co/google/gemma-3-12b-it)). Meta-licensed Llama models and research/non-production licenses require separate legal approval. “Free to download” is not sufficient.

## Provisional MVP routing

- Default quality profile: Qwen3 30B-A3B quantization proven by benchmark/hardware test.
- Low-resource profile: Granite 3.3 8B.
- Creative-dialogue challenger: Mistral Small 3.2 24B.
- Embeddings are optional in slice 1; begin with deterministic entity/scene retrieval, then enable Qwen3 Embedding only if retrieval tests justify it.

This is a testable baseline, not a permanent winner. No model becomes `recommended` until it passes the product benchmark and license manifest gate.

## Benchmark corpus

Use licensed/synthetic screenplay fixtures plus the SDI rubric: conversational elicitation, correction/undo, structured NKA extraction, cross-scene continuity, long-context retrieval, scene purpose, motivation/conflict/subtext, four-pillar scoring, score explanation, grounded recommendation, and refusal to claim film success. Human raters include screenplay expertise and engineering review.

## Hardware tiers

Registry profiles declare estimated RAM/VRAM, quantization, context budget, throughput, and fallback. Published maximum context is never assumed achievable at useful local speed or quality. The application runs a capability/health check and explains trade-offs before analysis.

## Supply-chain and license controls

Allowlist publisher or reviewed quantization sources, verify content digest, preserve model card/license, generate an SBOM entry, and prohibit arbitrary remote model names in production configuration. Re-review licenses before distribution and model upgrades.

## Runtime

Ollama is the MVP adapter because it supports local models, tool calling, streaming, and JSON-schema structured outputs ([official structured-output documentation](https://docs.ollama.com/capabilities/structured-outputs)). The architecture remains runtime-neutral.

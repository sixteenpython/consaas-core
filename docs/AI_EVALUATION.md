# AI Evaluation Framework

## Principle

Evaluate models and prompts on real ConSaaS work. Generic benchmarks inform discovery but cannot promote a model for a product task.

## Evaluation case

Each case contains stable ID, product/task, purpose, non-sensitive input fixture, expected schema, deterministic validation, acceptable semantic criteria, prohibited behavior, provenance requirements, and applicable model profiles.

## Pipeline

`Fixture -> model adapter/fake -> raw output -> schema validation -> domain validation -> canonical candidate -> scorer -> report`

Raw output is retained only under local/test privacy policy and is never treated as canonical. Deterministic validators run even when semantic scoring passes.

## Metrics

As applicable: schema validity, extraction precision/recall, evidence citation precision/recall, deterministic consistency, groundedness, unsupported-claim rate, refusal correctness, exact/adjacent rubric agreement, authorial-control violations, latency, token/compute usage, peak memory, and run failures.

## Golden suites

Use synthetic or explicitly licensed fixtures. Never commit customer screenplays, private financial records, or PII. Human-reviewed labels identify reviewer role, rubric version, disagreement, and approval date.

## Promotion and regression

A registry entry becomes recommended only after required suites meet task-specific thresholds and license/hardware gates. Compare model, quantization, runtime, prompt, and configuration as a complete evaluated profile. Upgrades that regress a critical metric are blocked even if aggregate scores improve.

## MVP scaffold

`evals/` contains JSON golden cases and offline runners. The factory demonstration evaluates NKA statement validation using recorded model-like output, proving the raw-to-canonical gate without downloading a model or exposing private content.

# Architecture Guardrails

## Enforced now

The `factory.guardrails` scanner checks Python source for:

- product packages importing another product;
- direct imports of hosted/provider SDKs outside approved Core adapters;
- obvious embedded credential/private-key patterns;
- application imports from `streamlit` outside UI paths;
- model/provider names hard-coded into domain modules;
- prohibited production Vriddhi modifications in factory-only tasks when the task policy declares them forbidden.

It also detects duplicate task/feature IDs and malformed factory status references. Unit tests exercise the rules.

## Dependency direction

`product domain -> public Core contracts`  
`adapters -> public Core contracts`  
`UI -> application/view models`  
`Core never -> product`

Products do not import one another. Domain modules do not import Streamlit, persistence implementations, or Ollama. LLM adapters do not contain product decisions.

## Review-only guardrails

Automated syntax cannot reliably identify premature abstractions, altered methodology, unsafe migrations, or misleading claims. Reviewers must inspect Core promotions, schema/contract changes, provenance, deterministic/probabilistic ownership, privacy boundaries, and rollback.

## Exceptions

Exceptions are narrow, time-bound, linked to an ADR/task, and encoded in one reviewed allowlist with owner and expiry. Inline suppression without explanation is forbidden.

## Evolution

When packages stabilize, add import-linter or equivalent graph enforcement, schema compatibility checks, public API snapshots, and deployment policy checks. Do not introduce tools whose configuration is more complex than the boundary being protected.

# Privacy

## Principles

Collect and retain only what the product needs, keep sensitive decisions and unpublished artifacts local where appropriate, disclose boundaries, and make deletion/export behavior explicit.

## Data classification

- Public/reference data.
- Internal product/operational metadata.
- Personal or customer-confidential data.
- Highly sensitive intellectual property, credentials, or regulated data.

Classification controls storage, encryption, logging, retention, export, model access, and test-fixture eligibility.

## AI boundary

Narrative Architect screenplay content must not be sent to external LLM APIs by default; its MVP permits local inference only. Other products must declare external processing and consent/policy before any sensitive payload crosses a boundary.

## Logging and analytics

Use IDs, hashes, counts, timing, and redacted error context. Do not log screenplay passages, PII, prompts containing private content, model responses, or financial/customer records. Product analytics must not capture content silently.

## Development

Use synthetic/licensed fixtures. Production data does not enter developer machines or CI without approved controls. Project deletion covers content artifacts, derived indexes, model traces, and documented backups according to retention policy.

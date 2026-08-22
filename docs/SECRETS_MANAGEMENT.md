# Secrets Management

## Rules

- Secrets never appear in source, committed configuration, fixtures, task text, logs, or model prompts.
- Configuration references environment variables or an approved secret store; code receives scoped values through adapters.
- `.env` files are local and ignored; provide `.env.example` with names and non-secret descriptions only.
- CI secrets use protected/masked variables and are unavailable to untrusted forks.
- Rotate on exposure, personnel/role change, provider policy, or scheduled control.

## Local-first models

Ollama loopback inference requires no API secret. Do not add placeholder hosted-provider keys to normalize its interface. Model downloads and registries use public artifacts or separately managed credentials without product content.

## Detection and response

Run secret scanning pre-merge and in CI. If a secret is committed, revoke/rotate first, then remove it from current and historical exposure under an approved incident procedure. Deleting the visible line is not remediation.

# Security

## Baseline

Use least privilege, deny-by-default external access, dependency pinning/scanning, input validation, safe subprocess boundaries, immutable/audited artifacts, and reviewed release gates.

## Engineering requirements

- No credentials, tokens, private keys, or production data in source, fixtures, prompts, or logs.
- Validate untrusted files and model output before use; resource-limit parsers and inference.
- Scope filesystem/database/network capabilities to the active product/project.
- Pin and verify model/runtime/dependency artifacts; record licenses and hashes.
- Protect branch/merge/deployment roles; production requires review and rollback.
- Report vulnerabilities privately and rotate exposed secrets immediately.

## CI

Run dependency audit, static security analysis, secret scanning, architecture checks, and tests. Findings are triaged by severity and exploitability; suppression requires owner, rationale, scope, and expiry.

## Threat-model triggers

New upload formats, external endpoints, authentication, multi-tenancy, model adapters, plugin execution, sensitive data classes, production migrations, or public APIs require threat-model review and possibly an ADR.

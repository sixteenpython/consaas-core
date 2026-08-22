# Automated Quality Gates

## Required pipeline

1. **Format:** Ruff format check.
2. **Lint:** Ruff rules for correctness/imports/security-adjacent patterns.
3. **Types:** mypy over factory, Core, and product source packages.
4. **Unit tests:** deterministic domain and helper tests.
5. **Integration tests:** cross-module/application workflows.
6. **Architecture:** repository guardrail scanner and import-boundary tests.
7. **Security/dependencies:** Bandit and pip-audit; secret scanning by CI platform or approved scanner.
8. **AI evaluations:** applicable versioned golden suites.

`.gitlab-ci.yml` expresses these as visible stages. The same commands must run locally. A skipped gate requires a documented reason and reviewer approval; a failing required gate blocks merge.

## Change-aware evaluation

AI/model/prompt/extraction changes run affected eval suites. Registry/license changes run model-governance checks. Product code changes run that product’s suites plus Core contracts. Documentation-only changes still run link/structure/guardrail validation where available.

## Evidence

MRs report command, version/environment, exit status, test/eval summary, artifacts, and known skips. CI artifacts retain evaluation reports and security findings without sensitive content.

## Gate integrity

Do not delete tests, lower thresholds, broaden ignores, mark flaky, or exclude paths solely to make a change pass. Gate-policy changes require review and, when architectural/security significance exists, an ADR.

## Current limitation

The repository provides GitLab configuration, but the configured remote is currently GitHub. Until a GitLab project/runner exists, local execution proves commands—not GitLab service behavior.

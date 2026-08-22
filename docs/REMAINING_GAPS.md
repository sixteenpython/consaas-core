# Remaining gaps

## Required before the factory is operational in GitLab

1. Create or identify the authoritative GitLab repository.
2. Add it as a remote without removing the existing GitHub remote unless ownership policy explicitly changes.
3. Configure a runner capable of Python 3.12 jobs and protected branch rules.
4. Require every job in `.gitlab-ci.yml` before merge.
5. Define CODEOWNERS and approval rules for Core, security/privacy, and product architecture.
6. Run the first pipeline and record evidence; do not convert REVIEW items to DONE before that review.

## Required before local-model feature development

- Benchmark the registry candidates on representative Narrative tasks and target hardware.
- Record exact model digests, quantization, runtime version, prompt version, and evaluation results.
- Add an embeddings contract only when a retrieval use case is approved.

## Platform maturity gaps

- Artifact lifecycle and report abstractions need evidence from a second product before Core promotion.
- Vriddhi integration should use an incremental strangler path, not a rewrite.
- Backup, restore, telemetry retention, and release signing need deployment-specific decisions.

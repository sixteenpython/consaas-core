# Observability

## Correlation model

Structured events use `execution_id`, `task_id`, `product_id`, `artifact_id`, `revision_id`, `model_run_id`, and `correlation_id` where applicable. IDs are opaque and contain no user content.

## Logs

Emit timestamp, severity, event name, component/version, correlation IDs, status, duration, safe error code, and retryability. Avoid payloads, prompts, screenplay excerpts, PII, credentials, filesystem secrets, and raw model output.

## Metrics

- execution success/failure and stage duration;
- validation rejection and retry counts;
- artifact/version counts and stale state;
- model latency, context/output tokens, memory profile, schema failure, fallback;
- evaluation scores/regressions;
- CI gate duration/failure;
- product-specific quality metrics under product namespaces.

## Errors

Use typed safe errors with internal cause chaining. User messages explain recovery without leaking content. Unexpected failures receive an execution ID for local diagnosis.

## Provenance and audit

Observability is not provenance. Important outputs store formal lineage/manifests; logs only help operate the process. Audit events capture actor, action, target, before/after version, reason, and outcome.

## Local operation

MVP storage may use structured JSON logs and local reports. Export/telemetry is opt-in and content-redacted. Retention and rotation are configurable by data classification.

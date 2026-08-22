# Reproducibility

## Reproducibility manifest

Important outputs record applicable input artifact IDs/hashes, knowledge revision, schema/methodology, code commit, dependency lock, configuration digest, model artifact/digest/license, runtime and quantization, prompt/template/schema version, parameters/seed, timestamp, validation results, and output artifact/hash.

## Classes

- **Deterministic:** identical canonical inputs and environment produce semantically identical output.
- **Seeded:** replay depends on recorded seed/runtime behavior.
- **Snapshot-replayable:** remote/nondeterministic response is retained with identity.
- **Non-replayable:** explicitly labelled and barred from authoritative use unless policy approves.

## Rules

Do not use mutable `latest` identities in manifests. Resolve model/container/dependency tags to immutable digests. Binary document metadata may differ; define canonical semantic/layout assertions. Clock and randomness are injected in deterministic tests.

## Replay

Replay reads immutable inputs and manifest, writes a new comparison artifact, and never overwrites the original. Differences distinguish input, code, configuration, model, prompt, and environment changes.

## Limitations

Local hardware kernels and quantized inference may not be bit-identical. Record enough context to reproduce the evaluated profile and compare validated canonical results, not hidden reasoning traces.

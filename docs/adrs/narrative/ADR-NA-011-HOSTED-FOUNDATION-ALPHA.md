# ADR-NA-011: Hosted Foundation Alpha and local-private profile

Status: Accepted for Foundation Alpha
Date: 2026-08-22
Owners: Product Owner, Narrative Architect

## Context

Narrative Architect is local-first because unpublished screenplay material is sensitive intellectual
property. The product also needs a public, same-day demonstration that can be deployed on Streamlit
Community Cloud. Browser input to a hosted Streamlit process is not local-only, and Community Cloud
cannot reach an Ollama runtime on a user's computer.

## Decision

The Foundation Alpha has two explicitly labelled profiles:

- `hosted_demo`: deterministic guidance only, no external LLM, no durable server-side project
  persistence, no content analytics, and project JSON download/upload for portability. The UI warns
  users not to enter confidential or unpublished material.
- `local_private`: the same application runs locally. Project content remains on the user's machine;
  a future increment may enable Ollama through the approved `LocalLLM` port.

The hosted profile is a product demonstration, not the completed private MVP. Doctor mode, screenplay
upload, and external model calls are disabled. The application never implies that session memory is
durable.

## Alternatives considered

- External free-tier inference: rejected because screenplay content would be sent to another service.
- Browser-to-local-Ollama tunnelling: rejected because it introduces security and support complexity.
- No hosted application: rejected because it prevents early product feedback.

## Consequences

The public alpha can launch without secrets or inference cost and still proves the canonical NKA loop.
Users must export projects before the hosted session ends. Private authoring uses the documented local
run command. Future hosted private work requires a separate reviewed privacy, identity, storage, and
inference decision.

## Validation

UI tests assert the disclosure and absence of Doctor/upload behavior. Architecture tests assert no
hosted model dependency. Project export/import round-trips all canonical revisions.

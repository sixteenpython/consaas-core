---
name: feature-creator
description: Translate vague, rough, partial, or detailed ConSaaS product ideas into architecture-aware, testable feature specifications and optional backlog entries. Use when a user says “use the Feature Creator,” invokes `$feature-creator` or `/feature`, asks to define/decompose a feature, convert product intent into implementation work, detect duplicate backlog work, allocate a feature ID, or prepare a ConSaaS feature for junior-developer/coding-agent delegation.
---

# Feature Creator

Turn product intent into the smallest valuable factory-ready vertical slice. Do not invent missing product decisions.

## Workflow

1. Identify product and requested output mode: `DRAFT`, `READY`, or `BACKLOG`. Default to DRAFT when readiness is uncertain.
2. Read repository guidance in this order: root `README.md`, Constitution, root/product `AGENTS.md`, product README/spec/architecture/roadmap, relevant ADRs, knowledge/intelligence definitions, related backlog/tasks, implementation, tests/evals, and Definition of Done.
3. Load only relevant context. Use `references/context-routing.md`; search with `rg` before opening broad files.
4. Search current implementation and backlog for duplicates or adjacent work.
5. Determine user problem, existing capability, affected domain/knowledge/intelligence components, deterministic versus AI work, provenance/versioning, dependencies, Core reuse, architecture impact, and smallest valuable slice.
6. If one consequential product definition is missing, ask the minimum blocking question. Present alternatives only when multiple legitimate interpretations remain. Do not allocate READY status while blocked.
7. Allocate the next unused namespace ID with `scripts/next_feature_id.py`. Never reuse an ID.
8. Produce every section in `references/output-contract.md`. Mark non-applicable sections explicitly with reason.
9. Validate architecture, acceptance criteria, tests/evals, privacy/security, observability, rollback, and Definition of Done.
10. In BACKLOG mode, write the approved specification to `backlog/features/`, update `backlog/index.json` and `factory/status.json`, and preserve dependency/status consistency. Do not add blocked drafts.

## Decision rules

- Classify the work as feature, enhancement, bug, refactor, migration, or architecture decision.
- Prefer end-to-end vertical slices over layer-sized technical epics.
- Keep the product runnable after each suggested task.
- Treat a Core promotion as a candidate until two-product evidence and an ADR exist.
- Stop on architecture conflict; identify the exact conflict and required ADR/owner.
- Separate deterministic mechanics from model interpretation. Require raw-output and domain validation for AI.
- Never claim a feature is already absent or present without inspecting implementation and backlog.

## Output modes

- **DRAFT:** complete proposal for review; unresolved decisions are visible.
- **READY:** all consequential decisions/dependencies/acceptance/tests are actionable.
- **BACKLOG:** READY specification plus repository index/status updates.

State the mode, readiness verdict, and unresolved blockers at the top.

## Invocation

Users may say `Use the Feature Creator`, `$feature-creator`, or `/feature <idea>`. Treat these as equivalent. Ask for a mode only when the requested repository mutation is unclear; otherwise infer DRAFT for plain ideation and BACKLOG when explicitly asked to add it.

## Resources

- Read `references/context-routing.md` for selective repository discovery.
- Read `references/output-contract.md` before drafting a specification.
- Run `scripts/next_feature_id.py --repo <root> --namespace <NAME>` before assigning an ID.

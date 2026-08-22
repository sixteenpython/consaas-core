# ConSaaS Agent and Developer Operating Contract

This file governs human developers and coding agents in this repository. More specific product `AGENTS.md` files add constraints but cannot weaken this contract or the Constitution.

## Before coding

1. Read the root `README.md` and `docs/CONSAAS_CONSTITUTION.md`.
2. Read the relevant product architecture, specification, roadmap, and ADRs.
3. Read the feature and executable task specification.
4. Inspect the current implementation, dependencies, related backlog items, tests, and evaluations.
5. Restate the task boundary, acceptance criteria, required tests/evals, provenance, privacy, and rollback needs.
6. Check dependencies and current repository status; preserve unrelated work.

## During coding

- Stay within scope and implement the smallest valuable vertical slice.
- Do not casually redesign architecture, create speculative abstractions, or promote product logic into Core without evidence and an ADR.
- Do not modify unrelated modules or production Vriddhi to simplify extraction.
- Preserve deterministic ownership, provenance, artifact identity, and versioning.
- Treat model output as untrusted; validate before canonical persistence.
- Do not couple product code directly to an LLM provider/model.
- Add no unnecessary dependency, secret, remote inference requirement, or sensitive logging.
- Keep the repository/product runnable after each increment.
- Never bypass or weaken tests, evaluations, guardrails, or CI.

If a requirement conflicts with architecture or creates a new consequential architectural capability: **stop**, explain the conflict, and create/propose an ADR or escalate to the Product Owner.

## After coding

1. Run formatting, lint, type checks, unit tests, integration tests, architecture guardrails, security checks, and applicable AI evaluations.
2. Inspect the full git diff and confirm no unrelated files or secrets.
3. Update task status, factory status, documentation, contracts, and ADRs as required.
4. Report exactly what changed, verification evidence, risks, known limitations, rollback, and the next recommended task.
5. Do not mark DONE until `docs/DEFINITION_OF_DONE.md` and task-specific gates pass.

## Standard task invocation

“Execute `TASK-ID` according to the ConSaaS Factory.”

Resolve the task from `backlog/tasks/`, follow `docs/FACTORY_EXECUTION_PROMPT.md`, and do not infer authority beyond the task.

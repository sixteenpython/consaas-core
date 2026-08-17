# First Principles

1. **A recommendation is a released artifact.** It has identity, time, evidence, methodology, policy status, and lineage.
2. **The pipeline is a graph of contracts.** Stages exchange versioned artifacts, never hidden module state.
3. **The Golden Knowledge Asset is domain-specific.** Core owns its envelope and governance; a product owns its payload and meaning.
4. **Decision and explanation are separate.** Explanation may verbalize a decision but may not invent or alter it.
5. **Presentation is downstream.** UI and reports consume published view models, not providers or engine internals.
6. **Reproducibility is declared.** A run records code, configuration, schemas, inputs, dependencies, random seeds, and model/prompt versions.
7. **Idempotency is mandatory.** Repeating a release key cannot silently create a different decision.
8. **Publication is transactional.** Build in isolation, validate, smoke-test, and atomically promote; retain a last known-good release.
9. **Policies are first-class.** Freshness, confidence, suitability, fairness, review, and domain constraints are auditable gates.
10. **Uncertainty travels with the result.** Estimates, ranges, assumptions, and limitations survive every stage.
11. **Plugins are replaceable and least-privileged.** Capabilities and side effects are declared before execution.
12. **No premature universal algorithm.** Common mechanics move to Core; domain judgment moves only when proven reusable.
13. **Backward compatibility has a budget.** Schemas have migration windows; silent coercion is prohibited.
14. **Human review is a designed state.** `needs_review` is a valid run outcome, not an exception.
15. **Platform value is measured.** Reuse, time-to-release, replay success, provenance coverage, and conformance are release metrics.

## Boundary rule

If changing code changes what a domain expert believes, it belongs in a product plugin. If every trustworthy Decision Intelligence product needs the behavior, it belongs in Core.

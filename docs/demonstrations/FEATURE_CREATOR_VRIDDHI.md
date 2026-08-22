# Feature Creator demonstration C — explain a changed stock health score

**Mode:** DRAFT  
**Provisional ID:** VRIDDHI-001  
**Backlog action:** none

## Input

“Explain why a stock’s health score changed this month.”

## Feature Creator result

The current ConSaaS/Vriddhi documentation defines screening, portfolio construction, recommendations, and explainability, but it does not establish one canonical metric named **stock health score** with a formula and historical ledger. Treating a nearby score as equivalent could create a financially misleading explanation.

### Minimum blocking clarification

Which exact persisted metric is “stock health score”—its field/formula and current-versus-prior snapshot source—or is this request asking us to define a new score?

No backlog item is created until the metric is identified. Once identified, the feature must use deterministic metric deltas and data provenance; an LLM may phrase the explanation but must not calculate or alter the score.

## Context and classification

- **Product:** Vriddhi
- **Type:** explainability enhancement, or a new metric/ADR if the score does not exist
- **Existing capability:** production screening, portfolio recommendations, monthly snapshots, and plain-English rationale; no canonical “stock health score” is identified in the ConSaaS inventory
- **Likely dependencies:** exact metric contract, prior/current persisted inputs, formula version, release provenance, and a Vriddhi compatibility adapter

## Deferred specification checkpoints

After clarification, READY acceptance criteria must reconcile the displayed delta exactly to stored prior/current metric components, distinguish data changes from formula-version changes, and drill through to source artifacts. Tests must cover unchanged, improved, deteriorated, missing, stale, and formula-migration cases. If an LLM phrases the explanation, evaluations must detect number drift, causal overclaim, omitted dominant factors, and financial-advice language. Out of scope: inventing a score, changing portfolio logic, predicting returns, rewriting Vriddhi, or modifying production during Core extraction.

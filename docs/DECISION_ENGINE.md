# Decision Engine

The Decision Engine turns a validated `DecisionView` and request into a `DecisionResult`. It does not fetch data, publish releases, render prose, or infer undeclared suitability.

Supported families are deterministic rules/simulation, optimization, ML, constrained LLM reasoning, and explicit hybrid graphs. Hybrid precedence and conflict resolution must be configuration, never hidden control flow.

The result records candidates, scores/objectives, selected set, constraints and binding status, uncertainty, diagnostics, rejected alternatives and reason codes, evidence references, parameters, engine/methodology version, seed, model/prompt/solver identity, and warnings. Infeasibility is a typed result.

Engines declare whether they support `fit`, `evaluate`, and `decide`, plus a reproducibility class: deterministic, seeded, snapshot-replayable, or non-replayable. Authoritative use of non-replayable engines requires explicit product policy. Champion/challenger promotion uses domain outcome metrics.

Release gates may constrain freshness, evidence, confidence, drift, fairness, stability, turnover, solver feasibility, and baseline comparison. Overrides record actor, reason, scope, and expiry.

Vriddhi’s screening, capped long-only optimization, forecasts, efficient frontier, walk-forward evidence, risk gates, and horizon verdict form a domain engine plugin. Generic metric and solver adapters may later move to libraries, but thresholds, universe, benchmark, horizon semantics, and investment objective remain Vriddhi-owned.

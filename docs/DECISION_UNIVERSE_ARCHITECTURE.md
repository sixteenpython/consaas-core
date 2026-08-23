# Decision Universe Architecture

## Product contract

Vriddhi processes the investable market before a customer arrives and exposes the research.
ConSaaS processes its covered decision universe before a customer arrives, but initially reveals
only the intelligence relevant to that customer's case. The full report, evidence and methodology
remain progressively explorable and downloadable.

The chat is therefore not the research engine. It is the client-facing constraint-discovery and
explanation layer over a versioned research release.

## Release pipeline

```text
governed sources
  -> Golden Knowledge Asset
  -> feature matrix
  -> downside / base / upside scenarios
  -> Growth / Stable / Persistent / Decline classification
  -> robust Pareto frontier
  -> Decision Atlas + model card + validation evidence
  -> atomic promotion
  -> customer-specific retrieval and optimisation
```

Every promoted product release contains:

- `grand_knowledge_asset.csv`: source-level canonical observations;
- `feature_matrix.csv`: derived, decision-ready measures for every covered option;
- `growth_decline_classification.csv`: pathway and frontier membership;
- `scenario_matrix.json`: downside, base and upside state;
- `pareto_fronts.json`: non-dominated options before customer constraints;
- `decision_atlas.json`: the complete live retrieval contract;
- `model_card.json`: champion method, limitations and promotion policy;
- `backtest_evidence.json`: temporal validation state and gates;
- manifest, source catalogue, quality report and validation report.

## Live decision boundary

The live application may:

1. interpret natural language into proposed case facts;
2. validate and preserve confirmed facts in the Case Knowledge Asset;
3. select the next question by decision value;
4. apply customer constraints to the frozen atlas;
5. rank feasible options and explain the frozen result.

It may not research a missing universe fact, train a model, alter a deterministic score, or turn an
inference into a confirmed fact without validation. When no option clears the evidence, resilience
or feasibility gates, `WAIT` is a successful decision outcome.

## Adaptive stopping

CareerSim and HouseWise stop after their mandatory safety and feasibility facts are established
only when the verdict family and leading option remain unchanged across every bounded value of the
remaining questions. Those omitted values are recorded as sensitivity-tested assumptions, never as
user facts. StartupEval retains all eleven Horse/Jockey evidence dimensions because an unanswered
dimension can be the fatal unknown.

## Model discipline

The current champion is a transparent deterministic multi-criteria scenario model. The release is
cross-sectional and does not yet support honest learned outcome prediction. A statistical or ML
challenger can be promoted only after dated historical vintages and realised outcomes demonstrate
out-of-time ranking lift, calibrated downside and subgroup stability. Until then, calling the
heuristic a predictive ML model would weaken rather than strengthen the product.

## Progressive disclosure

The recommendation view leads with verdict, “so what”, exact next action and three ranked moves.
Numbers, risks, evidence, policy and hash are available on demand. The customer can download JSON
for machines or Markdown for people and ask natural-language follow-ups that retrieve from the
frozen report without changing it.

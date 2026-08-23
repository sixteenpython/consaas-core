# Decision Studio: Domain Decision Intelligence v1

## Outcome

Decision Studio v0.4 replaces illustrative scorecards with three explicit decision systems while
preserving the shared ConSaaS consulting shell, canonical Case Knowledge Asset, provenance and
explainable report contract.

## CareerSim

The Golden Knowledge Asset contains 26 overseas-education pathways across undergraduate, master's
and PhD study; six fields; and the United States, Canada, United Kingdom, Europe and Australia. Each
row carries complete cost, foregone-income counterfactual, salary P10/P50/P90 scenarios, employment,
completion, funding, visa, evidence and risk signals.

The engine calculates complete economic cost, incremental NPV and IRR against not studying abroad,
debt resilience and affordability. It uses Pareto filtering and robust ranking to return three paths
with `GO`, `ADJUST`, `WAIT` or `DO NOT INVEST YET`. Rows are pathway references, not programme offers.

## HouseWise

The asset contains 28 micro-market search zones across seven Indian cities. It covers indicative
price, rent, acquisition and maintenance friction, vacancy, transit, liveability, liquidity,
climate/water/supply risk, evidence authority and price-growth scenario bands.

The engine simulates leveraged ownership cash flow, net rental yield and equity IRR, applies
household-resilience and affordability gates, filters dominated zones and returns three search
zones. `BUY` always means subject to property-level title, approval and technical diligence.

## StartupEval

The India Problem Observatory contains 30 decision-relevant problem spaces across household,
education, property, finance, health, agriculture, climate, work and public-service contexts. It
records problem reality, severity, frequency, willingness to pay, current solution coverage,
remaining white space and source provenance.

The consultant collects exactly eleven bounded narrative answers. The deterministic engine matches
the proposition to the Observatory and evaluates:

- Horse, 70%: reality, pain, payer, white space, mechanism, traction and economics;
- Jockey, 30%: founder–problem fit, completed execution, learning and capital discipline.

Answer scoring rewards specificity, behavioural evidence, measurable results and falsifiability.
It explicitly ignores prose polish, confidence and declared passion. Verdicts are `STRONG`, `NOT
QUITE THERE` and `FORGET IT — IN ITS CURRENT FORM`.

## Shared lifecycle

The monthly command builds, validates and atomically promotes all three assets. Tagged same-day
methodology releases preserve immutable history:

```powershell
python refresh_monthly.py --effective-date 2026-08-23 --release-tag decision-intelligence-v1
```

Each release includes the CSV, metric catalog, source catalog, manifest, quality report and
validation report. The current pointer is the only mutable promotion surface.

## Authority and limitations

- Forecasts are scenarios, not predictions or guarantees.
- Curated coverage is broad enough for the v1 decision contract but not exhaustive.
- User answers are self-reported until verified.
- No recommendation is admission, legal, property-title, valuation or investment advice.
- Open-weight models improve conversation only; deterministic code owns every verdict.

## Validation and release gate

Release requires formatting, lint, unit, integration, UI, architecture, security, evaluation and
production smoke checks. Golden simulations cover reproducibility, scenario ordering, stretched
affordability, evidence deterioration, vague startup claims and the ConSaaS `STRONG` reference case.

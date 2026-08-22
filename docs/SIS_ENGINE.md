# Scene Impact Score Engine

## Canonical score model

Each scene has four integer pillar scores from 0 to 5:

| Score | SDI label | Meaning |
|---:|---|---|
| 0 | Detrimental | Actively harms the narrative element. |
| 1 | Weak / Expository | Surface-level execution; narrative liability. |
| 2 | Functional | Performs the basic job without distinction/escalation. |
| 3 | Solid / Engaging | Element succeeds with meaningful movement or depth. |
| 4 | Highly Effective | Multi-tasks with significant escalation/depth. |
| 5 | Masterful | Perfectly calibrated pivot/transformation/dense subtext. |

The engine records:

```text
plot_0_5, scenes_0_5, characters_0_5, dialogue_0_5
sis_total_0_20 = exact integer sum
sis_mean_0_5 = sis_total / 4
```

Labels always include their scale. No field named only `impact_score` is allowed.

## Assessment contract

For every pillar: score, SDI rubric label, concise rationale, positive/negative evidence refs, uncertainty, assessor model run, and validation status. The model may not return totals. Deterministic code checks integer range, required evidence, scene membership, and rubric/rationale consistency before summing.

## Thresholds from SDI

- Mean 1–2: narrative liability.
- Mean 3: solid momentum.
- Mean 4–5: deliberate high-impact spike/cathartic potential.
- Appendix “flatline”: three or more consecutive sampled scenes with `sis_total_0_20 < 10`.
- Diagnostic discussion also refers to 10–15 scenes around 1–2 without a spike; store this as a separately named SDI cadence observation.

These rules are not merged. Configuration names the rule, scale, sampling strategy, and policy version.

## Explainability

“Why 2/5?” resolves to the relevant pillar rubric, rationale, and exact scene spans. A scene’s mean is descriptive aggregation, not a fifth model opinion. Aggregate act/character scores disclose weighting and missing scenes.

## Human review and overrides

Users may contest a score. An override creates a new analysis revision with original score, replacement, actor, reason, and affected aggregates. It never changes screenplay/NKA facts. Model re-evaluation is a new assessment, not mutation of history.

## Calibration

The MVP uses expert-authored golden scenes and inter-rater review to measure rubric agreement. Scores are ordinal diagnostics, not probabilities. Cross-model score drift, evidence coverage, and adjacent-level disagreement are tracked before a model profile is promoted.

## SDI extensions

Alternative weighting, genre-specific rubrics, learned engagement prediction, and biometric calibration are beyond SDI. They must not alter the canonical SDI scores and require separate fields, labels, and evaluation.

# Scene Assessor

## Purpose
Assess construction evidence without pretending to predict commercial success.

## iMaSc construction dimensions
- Conflict
- Character development
- Plot function
- Blocking and staging
- Placement

## SDI evidence view
Keep Plot, Scenes, Characters and Dialogue as separately labelled 0–5 pillars. Never merge a `/20` total and `/5` mean under a bare `impact_score` field.

## Method
For every score cite exact scene-card evidence, identify missing construction, state uncertainty and propose the smallest repair. Deterministic code owns weights, totals and thresholds.

Report two different measures:

- **Completion coverage** asks whether required scene-card evidence exists.
- **Craft quality** asks whether that evidence is story-specific, causal, playable and character-revealing.

Never infer craft quality from populated fields alone. Generic instructions, archetypal character placeholders, structural-space headings and repeated boilerplate cap craft quality at a low score even when completion is 5/5. Deterministic checks own the cap; a model may propose evidence and rationale but cannot award or persist the final score.


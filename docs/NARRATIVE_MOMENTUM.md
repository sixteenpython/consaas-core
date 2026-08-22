# Narrative Momentum

## SDI definition

The Narrative Momentum Graph plots chronological Scene Impact Scores to visualize the screenplay’s heartbeat: quieter setup valleys and escalation peaks. It diagnoses prolonged low-impact zones and cadence; it does not predict audience behavior.

## Series construction

Input is an ordered set of scored scenes from one analysis revision. The primary chart uses scene ordinal on X and clearly selected `sis_mean_0_5` on Y, matching the paper’s described 0–5 axis. A secondary toggle may show `sis_total_0_20`. Tooltips expose all four pillar scores, scene heading, confidence, and evidence link.

The graph is deterministic. Missing/unreviewed scenes appear as gaps, never zero. Reordered or deleted scenes require a new NKA/analysis revision.

## SDI observations

- `sdi.low_impact_run`: a declared run of scenes with mean in the 1–2 band and no 4/5 spike.
- `sdi.appendix_flatline`: three or more consecutive sampled scenes with total below 10.
- `sdi.escalation_peak`: upward movement culminating in 4/5 territory.
- `sdi.setup_valley`: quieter 2/3 scenes; not inherently defective.
- `sdi.episodic_spike_gap`: for an explicitly episodic format, no 4/5 spike over the declared 10–15-page interval.

The 10–15-scene and 10–15-page statements use different units and remain distinct. The selected sampling policy—every scene, every fifth scene, or major sequence—appears in the analysis manifest and chart subtitle.

## Interpretation guardrails

A low scene can be purposeful setup, particularly in deceptive thrillers. Detection generates an observation for contextual interpretation, not an automatic delete recommendation. The Script Doctor examines setup/payoff, later relevance, and pillar composition before recommending action.

## Views

- overall heartbeat;
- act/sequence bands and turning-point markers;
- pillar overlays;
- before/after revision comparison using stable scene IDs;
- click-through from point -> scene scorecard -> evidence -> source page/line.

## Metrics

Store series, runs, peaks, sampling coverage, missing-score count, and rule evaluations. Avoid invented “momentum percentage” in the SDI namespace. Smoothing, genre templates, predicted drop-off, and learned ideal curves are explicitly future extensions beyond SDI.

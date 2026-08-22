# ADR-NA-006: Preserve and Label Both SDI Score Scales

Status: Proposed  
Date: 2026-08-17

## Context

The SDI paper defines four pillar scores from 0–5, a combined worksheet score `/20`, a momentum Y-axis of 0–5, and a flatline threshold below total 10.

## Decision

Store each pillar `0–5`, deterministic `sis_total_0_20`, and `sis_mean_0_5`. Every field, chart, threshold, and sentence names its scale. Keep scene-based and page-based cadence policies separate.

## Consequences

The implementation preserves the paper without inventing a preferred interpretation. Configuration and UI are more verbose. A bare `impact_score` field is forbidden.

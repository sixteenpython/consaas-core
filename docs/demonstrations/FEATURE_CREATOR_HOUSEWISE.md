# Feature Creator demonstration A — HouseWise financial attractiveness

**Mode:** DRAFT  
**Provisional ID:** HOUSEWISE-001  
**Backlog action:** none

## Input

“Tell a buyer whether a property is financially attractive.”

## Feature Creator result

The phrase **financially attractive** is not decision-complete. It could mean affordable to occupy, positive rental cash flow, superior risk-adjusted investment return, or attractive relative to comparable properties. Those objectives can recommend different properties, and the required inputs and thresholds differ.

### Minimum blocking clarification

Which primary decision should HouseWise optimize in the MVP: **owner-occupier affordability**, **rental investment return**, or **relative value versus comparable properties**—and over what holding period?

Until that is answered, Feature Creator must not invent a score, acceptance criteria, or backlog item. Likely later inputs include purchase/financing costs, cash flows, vacancy/maintenance assumptions, comparables, uncertainty, and provenance.

## Context and classification

- **Product:** HouseWise
- **Type:** new domain feature
- **Existing capability:** only a planned product envelope; no approved HouseWise architecture, knowledge schema, or valuation implementation exists
- **Likely dependencies:** HouseWise product specification, property Golden Knowledge Asset, source/provenance policy, and a selected financial objective

## Deferred specification checkpoints

After the Product Owner answers the one blocking question, READY acceptance criteria must define reproducible calculations, units/currency/holding period, missing-data behaviour, uncertainty, evidence drill-down, and explicit non-advice language. Tests must cover formulas, boundaries, missing/stale inputs, and repeatability. AI evaluation is not applicable to calculations; if AI later explains results, golden cases must test numeric fidelity, provenance, uncertainty, and unsupported claims. Out of scope for the first slice: transaction execution, lender approval, legal/title advice, and universal claims that a property is “good.”

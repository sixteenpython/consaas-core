# Report Engine

## Purpose

The Report Engine turns recommendations and evidence into a channel-neutral `ReportBundle`. It separates what the system decided from how a channel presents it.

## Model

A bundle contains title/context, release badge, executive summary, recommendation groups, metrics, tables, chart specifications, evidence panels, assumptions, uncertainty, limitations, methodology, disclosures, calls to action, and provenance. Sections use typed blocks; renderers target Streamlit, web, PDF, Markdown, email, or API JSON.

Narrative templates consume structured explanation tokens and evidence references. An optional LLM can improve fluency or summarize, but output is validated against allowed facts and cannot create metrics, actions, or confidence. All generated claims retain evidence IDs.

## Shared components

- release freshness and methodology banner;
- verdict and confidence panel;
- “why this?” evidence card;
- comparison/rebalance table;
- risk and uncertainty panel;
- scenario and historical-evidence charts;
- action/execution sheet;
- disclosures, data limitations, and glossary;
- export and accessibility metadata.

## Validation

Core checks schema, evidence resolvability, numeric consistency, missing disclosures, accessibility labels, chart/table data agreement, forbidden unsupported claims, and renderer smoke tests. Products add regulatory and domain-language validators.

## Versioning

Report content schema, renderer version, theme, template, locale, and narrative generator identity are recorded independently. Re-rendering an old release is distinguishable from changing its underlying recommendation.

Vriddhi’s tab panels, finance-doctor framing, stock thesis cards, risk narratives, rebalance action cards, SIP replays, and execution ledger are reference report patterns. Their visual components are reusable; their investment copy and calculations remain product-owned.

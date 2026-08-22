# Decision Studio operations

## Monthly refresh

From the repository root:

```powershell
python refresh_monthly.py --effective-date 2026-09-22
```

The workflow validates all three source seeds and decision-metric catalogs, constructs isolated
candidates, writes combined content hashes, manifests and quality results, and promotes each release
atomically. The same date and content is
idempotent. Different content cannot silently overwrite an existing effective date.

## Before refresh

1. Review every `sources.json` disposition and official source for newer information.
2. Update only defensible seed records and observation dates.
3. Do not infer unavailable values from marketing copy.
4. Preserve source URLs, confidence and limitations.
5. Use a new effective date whenever content changes.
6. Review `metric_catalog.json`: mark evidence available only when a governed value/source exists.

## Validation and rollback

Run `python -m pytest -q` after refresh. Inspect each product's `quality.json` and `manifest.json`.
Serving resolves `knowledge/releases/<product>/current.json`; rollback is an atomic pointer change to
a retained valid release. Never edit an old release in place.

## Public app

`streamlit run streamlit_app.py`

The hosted Foundation profile is anonymous and session-only. `GROQ_API_KEY` is optional. When
configured, a user must explicitly consent before the structured consultation and frozen result are
sent to the hosted open-weight narrator. Without it, every core decision journey still works.

## Source maturity

`curated_snapshot` rows are ingested into the current asset. `reference_only` sources are reviewed by
an operator because a stable licensed machine-readable contract has not yet been confirmed. The
quality report exposes this distinction. A later connector increment may automate an official source
only after fixtures, licensing, schema-drift and network-disabled replay tests exist.

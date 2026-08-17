# Vriddhi Module Inventory and Extraction Map

This inventory classifies the current production repository by responsibility. “Platform” means reusable behavior should be extracted behind a generic contract. “Vriddhi” means the code embodies investment meaning, policy, data vocabulary, or presentation. Several files contain both and must be split rather than copied wholesale.

## Platform candidates

| Current module or cluster | Target | Why platform-owned |
|---|---|---|
| `vriddhi_monthly_refresh.py`: preflight, run-step lifecycle, isolated staging, backup/restore, candidate promotion, pruning | `core.runtime`, `core.release` | Every product needs safe orchestration, candidate isolation, recovery, and atomic promotion. |
| Same-date retry preservation and idempotent publication | `core.release` | Release identity and retry semantics are domain-neutral safety invariants. |
| Release metadata, dependency/code identity, SHA-256 manifest | `core.artifacts` | Provenance and integrity apply to every artifact. Provider/methodology text becomes product metadata. |
| `vriddhi_validation.py`: finite-value traversal, dates, hashes, validation result/reporting | `core.validation`, `knowledge.quality` | Generic primitives and validation composition are cross-domain. |
| Artifact loaders in `vriddhi_core.py` | artifact repository ports/adapters | Versioned artifact resolution and missing/corrupt behavior are shared serving needs. |
| `vriddhi_ledger.py`: append-only snapshots, unique ordered release dates, atomic write, manifest linkage | release/evaluation ledger service | Prospective history and non-rewriting semantics apply to all decision products. |
| `ticker_resolver.py`: alias cache pattern, resolution audit, health report and review queue | connector entity-resolution service | Aliasing, fallback candidates, audit, and human review recur across providers/domains. |
| `streamlit_app.py`: formatting primitives, release banners, cards/tables/chart containers, disclosure/glossary patterns | `reporting`, `ui` | Presentation mechanics and evidence components are reusable when driven by typed view models. |
| Headless all-variant smoke test | renderer/dashboard conformance kit | Every generated product needs “all configured pages/variants render” validation. |
| `tests/test_core_loaders.py`, validation and published-artifact tests | SDK conformance and release test kit | Loader, schema, provenance, freshness, hash, and publication invariants are universal. |
| GitHub CI and candidate-PR workflow structure | generator CI templates | Locked install, build, validate, evidence upload, review, and deploy gates recur. |
| Runbooks, refresh summary, methodology/release templates | generator documentation templates | Operational readiness should be scaffolded consistently. |

## Vriddhi-specific modules

| Current module or cluster | Future Vriddhi plugin | Why domain-owned |
|---|---|---|
| `build_grand_table.py`: Nifty universe, Yahoo symbols, finance fundamentals, sector mapping, forecast columns and guardrails | `vriddhi.knowledge` and connectors | The fields, source semantics, horizons, financial formulas, and guardrails encode investment knowledge. |
| `ticker_resolver.py`: NSE/BSE/Yahoo search rules and corporate-action interpretation | `vriddhi.connectors.yahoo_nse` | The platform can host entity resolution; these candidates and acceptance rules are market-specific. |
| `build_research_db.py`: price/risk metrics, stock screening, Max-Sharpe optimization, caps/floors, efficient frontier, walk-forward design | `vriddhi.decision` | These implement Vriddhi’s investment objective and evidence standard. |
| `build_research_db.py`: Nifty benchmark, risk-free rate, transaction cost, horizons, performance gates, optimal-view narrative | `vriddhi.policy` / `vriddhi.reporting` | Benchmark and threshold meanings are product methodology, not infrastructure. |
| `build_explanation` and financial metric interpretations | `vriddhi.recommendation` | PEG/PE/PB, volatility, drawdown, contribution, and stock-selection language are investment-specific. |
| `vriddhi_ledger.py`: `INITIAL/PICK/DROP/TOP-UP/TRIM/HOLD`, 1% threshold, monthly SIP policy, 12-release rule | `vriddhi.recommendation` / `vriddhi.policy` | Core owns generic action records; this taxonomy and execution policy express Vriddhi behavior. |
| `vriddhi_core.py`: legacy selector/optimizer, CAGR feasibility, projection, whole-share allocation | `vriddhi.decision` / `vriddhi.execution` | Financial objective, cash-flow math, and share settlement are domain semantics. Generic optimizers may be shared later. |
| `vriddhi_core.py`: OOS SIP and recommendation-ledger replay | `vriddhi.evaluation` | Core supplies evaluation lifecycle; SIP timing, shares, benchmark, and returns are investments. |
| `streamlit_app.py`: finance-doctor copy, portfolio/risk/backtest/optimal/rebalance panels, stock thesis, execution plan | `vriddhi.reporting` / page extensions | Page composition and narratives answer Vriddhi’s user questions. |
| `grand_table_expanded.csv`, portfolio bundles, benchmark, universe health, recommendation ledger | Vriddhi artifact schemas/instances | These payloads and their business meaning belong to the product, though wrapped by Core. |
| `Vriddhi_Alpha_Finder.ipynb`, historical app variants, images, competitive/reengineering docs | product research/archive/assets | They are reference material or product history, not platform runtime. |

## Mixed-module split details

`vriddhi_validation.py` should become generic validators plus a Vriddhi validation suite for universe size, required finance columns, weights, benchmark alignment, horizon completeness, turnover, and ledger action validity.

`vriddhi_monthly_refresh.py` should become a declarative pipeline run. Vriddhi supplies stage plugins and policies; Core supplies lifecycle. Git publication and Streamlit deployment become deployment adapters, not runtime assumptions.

`vriddhi_core.py` currently mixes legacy computation, artifact access, evaluation, and allocation. Introduce ports first, then move each cluster independently. Do not rename the whole module into Core.

`streamlit_app.py` should first consume an explicit Vriddhi view model. Only then extract stable block renderers; copying panels directly would leak financial concepts into the UI framework.

## Extraction rule

Move mechanics with unchanged semantics; wrap domain behavior behind contracts; promote an abstraction to Core only after a second product proves it. This avoids creating “Vriddhi with configurable nouns.”

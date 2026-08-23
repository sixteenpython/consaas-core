# Vriddhi–ConSaaS Architecture Solution

**Status:** Implemented architecture and engineering reference  
**Effective date:** 23 August 2026  
**Audience:** Product owners, architects, engineers, reviewers and monthly-release operators  
**Systems covered:** Vriddhi, ConSaaS Core, Decision Studio, CareerSim, HouseWise, StartupEval and the reusable factory foundations  
**Current Decision Studio UI:** v0.5.2  

## 1. Purpose

This document captures the architecture that evolved from Vriddhi into ConSaaS Core and the
complete design implemented for the Decision Studio full stack. It explains not only which modules
exist, but why authority is divided as it is, how the “Stockfish for decisions” idea is implemented,
how natural-language consulting remains compatible with deterministic verdicts, and how research
is refreshed, tested, promoted and served without compromising production.

The central product promise is:

> Given everything we know today, which decision maximizes the probability of superior long-term,
> risk-adjusted outcomes?

Vriddhi answers this for an investable stock universe. CareerSim and HouseWise apply the same
research-first pattern to overseas education and residential property. StartupEval uses the same
platform lifecycle but a different domain engine: it assesses whether the Horse—the problem and
business model—and the Jockey—the founders and their execution evidence—justify the next unit of
capital.

The architecture does not predict guaranteed success. It creates a governed, replayable and
explainable decision from the strongest evidence currently available.

### 1.1 Solution inventory and technology stack

| Surface | Repository / deployment | Role |
|---|---|---|
| Vriddhi | [GitHub](https://github.com/sixteenpython/vriddhi-core) · [Live app](https://vriddhi-core-beta.streamlit.app/) | Production investment-intelligence reference product |
| ConSaaS Core | [GitHub](https://github.com/sixteenpython/consaas-core) | Shared decision-intelligence operating system and product monorepo |
| Decision Studio | [Live app](https://consaas-decision-studio.streamlit.app/) | CareerSim, HouseWise and StartupEval consulting shell |

The implemented stack is deliberately small: Python 3.12 for research and domain intelligence,
Streamlit for the current user experience, CSV/JSON and filesystem releases for immutable MVP
artifacts, Git/GitHub for source and release history, and Streamlit Community Cloud for serving.
Optional model inference is provider-neutral and open-weight; no paid model is required for an
authoritative decision.

## 2. Executive architecture statement

Vriddhi proved that a high-value intelligence product does not need an expensive live AI backend.
It can research the complete governed universe before the user arrives, publish an immutable
release, and let a thin Streamlit application explain the resulting recommendations.

ConSaaS generalizes that pattern:

```text
OFFLINE RESEARCH PLANE

Governed sources
    -> Golden Knowledge Asset
    -> decision-ready features
    -> downside / base / upside scenarios
    -> pathway classification
    -> robust frontier / admissible decision set
    -> immutable Decision Atlas
    -> validation + model card + manifest
    -> atomic promotion

LIVE CONSULTING PLANE

Natural-language user conversation
    -> validated DialogueAction
    -> canonical Case Knowledge Asset
    -> customer constraints applied to promoted Decision Atlas
    -> domain-specific deterministic Decision Engine
    -> frozen Decision Report
    -> Vriddhi-style verdict, reasons, risks and next actions
    -> follow-up evidence exploration
```

The chat is not the research engine. The language model is not the consultant by itself. The
consultant is the combined system:

```text
conversation policy
+ optional open-weight language model
+ canonical Case Knowledge Asset
+ promoted Golden Knowledge Asset and Decision Atlas
+ deterministic domain engine
+ provenance and release policy
+ plain-English report experience
```

## 3. Architectural lineage: what Vriddhi contributed

Vriddhi is the production reference architecture and Version 1 of the ConSaaS idea. Its most
important contribution is not an investment formula; it is the separation of expensive research
from inexpensive serving.

### 3.1 Vriddhi research plane

Vriddhi performs the following work offline:

1. Acquire adjusted price history and current fundamentals.
2. Resolve ticker changes and assess universe health.
3. Build `grand_table_expanded.csv`, the canonical investment knowledge asset.
4. Screen securities and create decision-ready candidate sets.
5. Run capped long-only portfolio optimisation for five investment horizons.
6. Calculate expected return, covariance, volatility, Sharpe, drawdown and contribution evidence.
7. Run walk-forward out-of-sample evaluation against the Nifty 50 benchmark.
8. Produce current and previous portfolio bundles, risk evidence and release provenance.
9. Append the actual published portfolio to the prospective recommendation ledger.
10. Validate the full candidate and promote it only after every gate passes.

### 3.2 Vriddhi serving plane

The live application reads committed CSV and JSON artifacts. It does not download market data,
train a model or optimise a portfolio during a user session. This gives the product:

- predictable latency;
- low hosting cost;
- resilience to market-data outages;
- reproducible recommendations;
- a small runtime dependency surface; and
- a direct connection from every displayed claim to a published research release.

### 3.3 Vriddhi trust and execution layer

Vriddhi also established the UX standard now used by ConSaaS:

- lead with the verdict and its meaning;
- translate technical measures into everyday language;
- explain why an action improves the whole portfolio rather than citing one isolated metric;
- distinguish historical evidence, forecasts and actual published recommendations;
- separate CAGR, cash-flow illustrations and future XIRR correctly;
- show PICK, DROP, TOP-UP, TRIM and HOLD with quantitative rationale; and
- convert portfolio intent into an executable, whole-share, netted order sheet.

The ConSaaS recommendation screen follows the same sequence: verdict, “so what”, three best moves,
numbers on demand, risks, evidence, change conditions and an executable next step.

## 4. ConSaaS operating principles

### 4.1 Product judgment before AI firepower

The system optimises for small, well-defined, testable increments. Repository architecture,
contracts and automated gates carry context so that inexpensive coding and inference models can
implement or explain bounded work. The scarce resource is clarity, not tokens.

### 4.2 Common infrastructure, domain-specific intelligence

Core owns reusable mechanics. Products own domain truth. CareerSim, HouseWise and StartupEval share
artifact lifecycle, consultation, model boundaries, reporting and release safety, but they do not
share an artificial universal scoring formula.

### 4.3 Deterministic authority

Where practical, deterministic code owns:

- identifiers, schemas and state transitions;
- validation and epistemic status;
- arithmetic, cash flows and scenario calculations;
- constraints, gates, thresholds and ranking;
- optimisation and frontier construction;
- manifests, hashes, versioning and promotion;
- report structure and numeric consistency; and
- rollback and replay.

Language models may interpret natural language, propose typed actions, improve wording or challenge
a frozen result. They cannot silently alter facts, scores, options, evidence or verdicts.

### 4.4 Evidence before authority

A missing fact reduces authority; it is never filled with invented precision. Extracted facts,
user-confirmed facts, estimates, model inferences, calculated values and recommendations remain
distinguishable. Every consequential recommendation exposes assumptions, risks, evidence and the
conditions that could change it.

### 4.5 Modular monolith before microservices

The current products are deployed as modular Python applications. A directory boundary expresses
ownership; it does not justify a network boundary. Services should be introduced only for measured
security isolation, independent scaling, reliability or team ownership needs.

## 5. The full-stack logical architecture

```text
                                  USER
                                    |
                                    v
                         Streamlit advisory shell
                landing / consultant / brief / result / evidence
                                    |
                    +---------------+----------------+
                    |                                |
                    v                                v
         Conversational controller          Report exploration
         next-question policy                download / follow-up Q&A
                    |
                    v
          typed DialogueAction boundary
                    |
           schema + domain validation
                    |
                    v
       session-only Case Knowledge Asset
       facts + epistemic state + revisions
                    |
                    v
         DecisionStudio application service
                    |
          +---------+---------+----------------+
          |                   |                |
          v                   v                v
      CareerSim           HouseWise        StartupEval
      cash-flow           ownership        Horse/Jockey
      optimiser           optimiser        adjudicator
          |                   |                |
          +---------+---------+----------------+
                    |
                    v
        promoted product Decision Atlas
     + GKA + policy + scenarios + evidence
                    |
                    v
          immutable DecisionReport
                    |
        +-----------+--------------------+
        |                                |
        v                                v
 deterministic Vriddhi-style copy   optional open-model narration
 authoritative                      validated, non-authoritative
```

The live service is read-only with respect to promoted research. It may interpret a user message,
validate a case fact, select the next question, retrieve from the frozen atlas, rank feasible
options and explain the result. It may not conduct new universe research, train a model or modify a
published release.

## 6. The four canonical artifacts

### 6.1 Golden Knowledge Asset

The Golden Knowledge Asset (GKA) is the complete governed domain knowledge available at a declared
cutoff. It is broader than one user decision. Examples include:

- Vriddhi company fundamentals, prices, sectors and forecast signals;
- CareerSim education pathway economics and outcome scenarios;
- HouseWise micro-market price, rent, risk and liveability evidence; and
- StartupEval’s India Problem Observatory.

A GKA release records product identity, effective date, schema and methodology versions, source
provenance, content hash, quality results and limitations. Core governs the envelope; the product
owns the payload schema.

### 6.2 Case Knowledge Asset

The Case Knowledge Asset is the canonical representation of the customer’s current decision. It is
not the transcript. Facts carry an epistemic state:

- `confirmed`—provided or explicitly selected by the user;
- `estimated`—an explicit working estimate accepted by the user;
- `inferred`—a hypothesis that is not decision-ready;
- `unknown`—the user does not know;
- `uncertain`—the user cannot confirm confidently; or
- `deferred`—the issue was intentionally postponed.

Only confirmed and accepted estimated values enter the authoritative engine. Revisions are
preserved so the current case can change without erasing how it changed. The public MVP keeps this
artifact in the anonymous Streamlit session and does not durably store personal information.

### 6.3 Decision Atlas

The Decision Atlas is the ConSaaS equivalent of Vriddhi’s precomputed market research. It contains
the complete **covered** decision universe after feature engineering and scenario processing. A
promoted release includes:

| Artifact | Purpose |
|---|---|
| `grand_knowledge_asset.csv` | Canonical source-level observations |
| `feature_matrix.csv` | Derived decision-ready measures for every covered option |
| `growth_decline_classification.csv` | Pathway and frontier membership |
| `scenario_matrix.json` | Downside, base and upside states |
| `pareto_fronts.json` | Non-dominated options before customer constraints |
| `decision_atlas.json` | Complete live retrieval contract |
| `model_card.json` | Champion method, limits and promotion requirements |
| `backtest_evidence.json` | Temporal validation status and challenger gates |
| `manifest.json` | Identity, hash, lineage and effective date |
| `quality.json` / `validation_report.json` | Release-gate evidence |

“Complete universe” means every record inside the governed coverage set is processed exactly once.
It does not mean every university, property, company or human problem in existence. Coverage grows
through governed releases rather than marketing claims.

### 6.4 Decision Report

The Decision Report freezes the output of one case against one knowledge release and policy. It
contains:

- verdict, score and confidence;
- data sufficiency;
- up to three ranked moves;
- structured reasons, risks and metrics;
- immediate actions;
- conditions that could change the verdict;
- evidence references;
- consultation facts; and
- GKA artifact ID, effective date, hash and policy version.

Both JSON and Markdown downloads are derived from this object. Follow-up questions retrieve from
the frozen report and cannot silently recompute or alter it.

## 7. The “Stockfish for decisions” design

The analogy is architectural, not literal. Stockfish evaluates a bounded game state using a known
rule system and returns the strongest moves. ConSaaS builds a governed decision state before the
customer arrives, applies customer-specific constraints, and returns the strongest admissible
moves.

```text
Vriddhi:   investable stocks -> scenario/risk evidence -> optimal portfolio
CareerSim: education paths   -> full economic cash flows -> robust programme pathways
HouseWise: search zones      -> ownership cash flows     -> robust property search zones
Startup:   Indian problems   -> Horse/Jockey evidence    -> fund / hold / stop actions
```

The current champion is a transparent deterministic multi-criteria scenario model. A learned model
is not promoted merely because machine learning sounds more advanced. ML becomes authoritative only
after dated historical vintages and realised outcomes demonstrate:

- out-of-time ranking improvement over the deterministic baseline;
- calibrated downside estimates;
- stability across important subgroups;
- reproducible training and inference lineage; and
- no regression in interpretability or safety gates.

Until those conditions exist, claiming predictive ML would reduce trust. The platform nevertheless
stores model cards and backtest requirements so a future challenger can be evaluated honestly.

## 8. Product decision engines

### 8.1 Vriddhi

Vriddhi screens an investable stock universe and optimises capped long-only portfolios across five
horizons. It combines valuation, forecast, historical growth, covariance, risk and benchmark
evidence. Walk-forward testing provides out-of-sample methodology evidence; the prospective ledger
separately records what Vriddhi actually published. The monthly rebalance translates changes into
PICK, DROP, TOP-UP, TRIM and HOLD, then produces a netted whole-share execution sheet.

### 8.2 CareerSim

The current governed universe contains 26 overseas education pathways across undergraduate,
master’s and PhD study, six fields and five destination regions. Rows are pathway references, not
specific admission offers.

For each feasible path the engine calculates:

- all-in education cost;
- foregone-income counterfactual and complete economic cost;
- destination/return-dependent salary P10, P50 and P90 bands;
- ten-year incremental cash flows and NPV;
- incremental IRR;
- probability-weighted positive-NPV evidence;
- affordability, debt resilience, work-rights and risk fit; and
- evidence authority.

The engine filters infeasible options, removes dominated choices, applies customer priorities and
returns three robust paths. Verdicts are:

- `GO`—proceed to offer-level diligence;
- `ADJUST`—change cost, funding or destination before committing;
- `DO NOT INVEST YET`—downside-adjusted value is too weak; or
- `WAIT`—no covered path responsibly satisfies the constraints.

The v0.5.2 narrative names the leading path, explains the funding or downside issue and tells the
student exactly what to verify before paying a deposit.

### 8.3 HouseWise

The current governed universe contains 28 micro-market search zones across Bengaluru, Mumbai,
Pune, Hyderabad, Chennai, Delhi NCR and Kolkata. A row is a search-zone reference, never approval of
a specific project or title.

For the required size, budget, financing and holding period, the engine calculates:

- indicative base price and transaction cost;
- leveraged ownership cash flows;
- remaining loan and terminal equity;
- downside, base and upside equity IRR;
- net rental yield and probability-of-loss reference;
- affordability, household resilience and liquidity;
- liveability, climate and water risk; and
- evidence authority.

Stretched financing is a veto even when a zone scores well. A short holding period is penalised
because transaction friction and illiquidity matter. Verdicts are:

- `BUY`—subject to exact property legal, technical and price diligence;
- `BUY ONLY IF ADJUSTED`—use the displayed maximum-price and risk gates;
- `RENT/WAIT`—do not force a fragile or weak purchase; or
- `WAIT`—no covered search zone satisfies the case.

The narrative makes household resilience explicit: a good property is still a bad purchase if it
makes the household fragile.

### 8.4 StartupEval

StartupEval does not optimise a catalogue of investment products. It tests one proposition against
30 governed Indian problem spaces and exactly eleven evidence dimensions.

The Horse owns 70% of the verdict:

- problem reality;
- pain and frequency;
- willing payer;
- remaining white space;
- solution mechanism;
- behavioural traction; and
- sustainable economics.

The Jockey owns 30%:

- founder–problem fit;
- execution evidence;
- learning discipline; and
- capital discipline.

Natural-language answers are scored for specificity, behavioural evidence, measurable results and
falsifiability—not grammar, confidence, declared passion or verbosity. Critical evidence gates
prevent an attractive aggregate score from hiding the absence of a real problem, payer, solution
outcome or capable execution.

Verdicts are:

- `STRONG`—fund the next controlled proof milestone, not uncontrolled scale;
- `NOT QUITE THERE`—hold scale capital and test the fatal unknown; or
- `FORGET IT — IN ITS CURRENT FORM`—stop funding the present proposition, while leaving open a
  materially different future version.

The recommendation always identifies the weakest supported dimension, proposes a bounded test and
recommends rerunning the versioned assessment after evidence changes.

## 9. Conversational consulting architecture

### 9.1 Adaptive consultation

Each product supplies versioned questions with importance, answer type, allowed ranges, why the
fact matters and expert guidance. The consultant recomputes the next unresolved issue by decision
value rather than following a visually rigid questionnaire.

CareerSim and HouseWise may stop after mandatory safety and feasibility facts are established only
when the verdict family and leading option remain unchanged across every bounded value of the
remaining questions. Omitted values are recorded as sensitivity-tested assumptions, not user
facts. StartupEval requires all eleven dimensions because any one can reveal the fatal unknown.

### 9.2 Natural-language interaction

Users may narrate a problem, answer conversationally, say “I don’t know,” express uncertainty, ask
why a question matters or revise an earlier answer. The interaction becomes:

```text
user message
    -> proposed DialogueAction
    -> question identity validation
    -> type / choice / range validation
    -> duplicate and contradiction guards
    -> Case Knowledge Asset mutation
    -> acknowledgement + decision implication
    -> next highest-value question
```

The duplicate narrative guard prevents one attractive answer from being silently filed under a
different diagnostic dimension, which is especially important for StartupEval’s traction,
execution and learning evidence.

### 9.3 Optional model profiles

The application remains fully functional without external inference. Optional profiles are behind
provider-neutral contracts and a model registry:

- a browser-side Apache-2.0 open-weight WebLLM profile can interpret a turn on a compatible WebGPU
  device;
- a local Ollama adapter remains available where hardware permits; and
- an explicitly configured hosted open-weight narrator may explain a frozen report only after
  consent.

Every model output is untrusted. It must satisfy a typed schema and domain validation. Invalid,
unavailable or exhausted inference falls back to deterministic wording. Models cannot call product
engines directly or persist canonical knowledge.

## 10. Recommendation and reporting architecture

The report engine separates authoritative decision content from channel rendering. The Streamlit
experience uses progressive disclosure:

1. **Verdict**—the direct decision family.
2. **So what should you do?**—one unambiguous call to action.
3. **Three best moves**—ranked, distinct options with a plain-language reason.
4. **Numbers behind this option**—technical metrics available on demand.
5. **Risks and evidence**—the limits and provenance behind each move.
6. **Do next**—an execution sequence.
7. **What would change the verdict?**—sensitivity and falsification conditions.
8. **Assumptions**—the authority boundary.
9. **Technical identity**—release, policy and hash.
10. **Follow-up consultant**—retrieval from the frozen report.

The v0.5.2 narrative-quality rule is that customer copy must lead with the action, not internal
terms such as Pareto frontier, feature matrix or Decision Atlas. Those concepts remain visible in
the Method and Knowledge Asset views for users who want to inspect the machinery.

## 11. Platform modules versus product modules

### 11.1 Reusable platform modules

| Module | Platform responsibility |
|---|---|
| `core/artifacts.py` | Canonical serialization, hashing and artifact identity |
| `core/refresh.py` | Isolated candidate construction, validation and atomic promotion |
| `core/decision_atlas.py` | Shared release bundle construction and frontier metadata |
| `core/optimization.py` | Bounded arithmetic, IRR, present value, Pareto and stability helpers |
| `core/ai/contracts.py` | Provider-neutral generation request/result contracts |
| `core/ai/registry.py` | Task-based model selection and governed model metadata |
| `plugin_sdk/decision.py` | Stable question, option and Decision Report value types |
| `decision_studio/case.py` | Case facts, epistemic status and revision history |
| `decision_studio/conversation.py` | Typed dialogue actions and validation guards |
| `decision_studio/consultant.py` | Next-question and information-value policy |
| `decision_studio/service.py` | Product orchestration over promoted releases |
| `decision_studio/report_qa.py` | Frozen-report export and grounded follow-up retrieval |
| `decision_studio/ui.py` | Shared Streamlit consulting and progressive-disclosure shell |
| `factory/` | Guardrails, model registry, feature workflow and engineering controls |

### 11.2 Product-owned modules

Each of `careersim/`, `housewise/` and `startup/` owns:

- `questions.json`—domain consultation contract;
- `schemas/gka.schema.json`—canonical knowledge schema;
- `sources.json`—governed source catalog;
- `metric_catalog.json`—decision metrics and evidence coverage;
- `decision_policy.json`—methodology, weights, gates and versions;
- `decision.py`—authoritative domain engine;
- `cognitive_blueprint.md`—domain reasoning and explanation boundary;
- `SKILL.md`—optional language-model behavior; and
- seed/reference data used by the governed refresh.

StartupEval additionally owns `founder_execution_blueprint.md` because Jockey assessment is a
domain-specific construct, not a universal platform primitive.

## 12. Research release and monthly refresh

The shared Decision Studio refresh is:

```text
python refresh_monthly.py --effective-date YYYY-MM-DD
```

For a corrected same-day methodology release, a distinct release tag is required. The workflow:

1. reads governed source and metric catalogs;
2. constructs each candidate GKA in isolation;
3. validates schema, uniqueness, ranges, provenance and coverage;
4. derives feature, scenario and pathway artifacts for every governed row;
5. computes the robust frontier and Decision Atlas;
6. writes model-card and temporal-validation evidence;
7. calculates content hashes and manifests;
8. runs product validation gates; and
9. atomically advances `knowledge/releases/<product>/current.json`.

Retained releases are immutable. The current pointer is the only mutable promotion surface.
Rollback repoints it to a retained valid release; no historical release is rewritten.

Vriddhi uses the same transaction pattern with a richer market-data workflow: backup, staging,
candidate knowledge build, portfolio research, cross-artifact validation, ledger append, all-horizon
Streamlit smoke test, manifest creation and atomic promotion.

## 13. Provenance, versioning and replay

Important identities are independent:

- product version;
- GKA schema version;
- GKA artifact ID and content hash;
- effective date and observation date;
- decision methodology and policy version;
- model, prompt and runtime identity where applicable;
- report schema and renderer version; and
- application commit and deployment.

A recommendation must be replayable from the exact Case Knowledge Asset, promoted GKA/Decision
Atlas, policy and code. Model-generated wording does not replace these identities. A methodology
change creates a new tagged release; an old artifact is never silently reinterpreted.

## 14. Validation and release assurance

The release contract includes:

- format and lint checks;
- strict type checking;
- deterministic unit tests;
- cross-module integration tests;
- all-product Streamlit AppTest coverage;
- architecture guardrails;
- Bandit security scanning;
- dependency vulnerability audit;
- AI boundary evaluations;
- promoted-universe integrity checks;
- decision-sense regression cases; and
- production browser smoke tests.

The v0.5.2 stress release evaluated 26,249 deterministic cases:

- 19,440 CareerSim combinations;
- 6,804 HouseWise combinations; and
- five critical StartupEval evidence profiles.

The suite exercises favorable, conditional, adverse, infeasible, stretched-financing, short-horizon,
weak-payer, weak-learning and weak-problem-evidence paths. It fails when:

- scores leave the valid range;
- more than three moves are returned;
- options duplicate or lack reasons, metrics or evidence;
- no feasible option is returned without an explicit WAIT;
- customer copy leads with engine jargon;
- stretched property financing escapes the RENT/WAIT veto;
- a one-year ownership case receives an unconditional BUY; or
- a StartupEval critical-evidence failure receives STRONG.

At release, all 26,249 stress cases and 79 automated repository tests passed, with no known audited
dependency vulnerabilities. Production v0.5.2 loaded all three product workspaces without browser
errors.

## 15. Deployment architecture

### 15.1 Streamlit as the current shell

Streamlit remains appropriate for the MVP because it provides fast delivery, Python-native report
rendering, session state, downloads and low-cost hosting. The single root entrypoint serves the
landing page and three product workspaces. Product routes share one visual language while keeping
their intelligence modules independent.

### 15.2 Production path

```text
developer change
    -> local quality gates
    -> reviewed Git commit
    -> GitHub main
    -> Streamlit Cloud rebuild
    -> production version check
    -> product workspace smoke tests
```

Serving resolves committed immutable knowledge releases. A Streamlit redeployment changes code or
presentation; it does not mutate the promoted research asset during a session.

### 15.3 Future frontend boundary

The report, question and decision contracts are channel-neutral. A future React, mobile, API or
institutional dashboard can consume the same Case Knowledge, Decision Report and evidence model.
The frontend should be replaced only when measured accessibility, concurrency, workflow or
interaction needs exceed Streamlit—not for architectural fashion.

## 16. Privacy, security and safety

The public Decision Studio profile is anonymous and session-only:

- no durable personal, property or venture case store;
- no consultation text in application logs;
- downloads are created in memory;
- hosted inference is optional, disclosed and consent-based;
- browser inference keeps consultation reasoning on the device apart from downloading public model
  assets;
- secrets are configuration references, never artifacts;
- generated model content cannot mutate canonical facts without validation; and
- the app states that it is decision support, not regulated financial, legal, admission, valuation
  or investment advice.

High-stakes actions remain human decisions. CareerSim does not predict admission or immigration.
HouseWise does not approve title, construction or a property transaction. StartupEval does not
predict startup success or valuation. Vriddhi does not guarantee security returns or execute broker
orders.

## 17. Failure behavior and rollback

The architecture treats honest refusal as success:

- missing mandatory facts keep a case unresolved;
- unstable omitted facts prevent adaptive stopping;
- no feasible education or property option produces WAIT;
- stretched property financing produces RENT/WAIT;
- insufficient startup evidence produces HOLD or STOP;
- invalid model output falls back to deterministic interaction;
- a failed research candidate never replaces the promoted release; and
- a failed deployment is rolled back by Git revert and/or release-pointer restoration.

There is no silent downgrade from a required source, methodology or validation gate.

## 18. Repository design

```text
consaas-core/
├── core/                  reusable artifact, refresh, optimisation and AI ports
├── plugin_sdk/            stable product contracts and value types
├── decision_studio/       shared consultation, case, service, reporting and UI shell
├── careersim/             overseas-education domain plugin
├── housewise/             residential-property domain plugin
├── startup/               Horse/Jockey venture domain plugin
├── knowledge/releases/    immutable product releases and current pointers
├── narrative/             Narrative Architect domain product
├── factory/               engineering operating system and guardrails
├── connectors/            reusable acquisition adapters
├── reporting/             shared reporting evolution surface
├── recommendation_engine/ shared recommendation-contract evolution surface
├── templates/             product and documentation scaffolds
├── examples/              reference implementations
├── evals/                 offline behavioral and stress evaluations
├── tests/                 unit, integration, UI and architecture suites
├── docs/                  architecture, ADRs, operations and product references
├── refresh_monthly.py     three-product research-release command
└── streamlit_app.py       Decision Studio production entrypoint
```

Narrative Architect demonstrates that ConSaaS can also support an artifact whose intelligence is
not naturally reducible to an investment-style option universe. It reuses canonical artifact,
provenance, versioning, model-port and reporting concepts while retaining screenplay-specific
knowledge and SDI diagnostic engines. This validates the principle that Core is shared
infrastructure, not a forced universal domain model.

## 19. Architectural decisions that must remain stable

1. **Static/precomputed research is the source of live authority.** User sessions do not perform
   authoritative universe research.
2. **The Case Knowledge Asset, not chat history, is canonical customer memory.**
3. **Products own domain schemas and decision logic.** Similarity does not justify a universal
   scoring engine.
4. **Deterministic engines own verdicts.** Models interpret and explain through validated ports.
5. **Every governed universe row is processed before promotion.** Coverage boundaries remain
   explicit.
6. **Candidate releases are isolated and promotion is atomic.** Partial research is never served.
7. **Evidence, assumptions and change conditions travel with recommendations.**
8. **The recommendation begins with a decision and call to action.** Technical machinery is
   progressively disclosed.
9. **ML promotion requires realised-outcome evidence.** A complex model is not automatically a
   better model.
10. **The modular monolith remains the default.** Network services require measured justification.

## 20. Current limitations and known engineering debt

1. CareerSim, HouseWise and StartupEval coverage is governed and complete for the current release,
   but intentionally bounded rather than exhaustive.
2. Several desired metrics remain `planned_connector` or `required_case_evidence`; they must not be
   fabricated from generic web content.
3. Career and property forecasts are scenarios, not calibrated individual predictions.
4. The current Decision Atlas has cross-sectional evidence but insufficient longitudinal realised
   outcomes for an authoritative learned challenger.
5. Browser-side inference is device-dependent and the compact model improves interaction more than
   deep domain reasoning.
6. The anonymous session profile does not yet provide durable customer case history or institutional
   tenancy.
7. The root `decision-studio-release-manifest.json` still reflects the earlier v0.4 release label;
   the promoted GKA pointers and UI version are newer. The next release-governance increment should
   make this root manifest generated from the current product pointers and application version.
8. Product-specific legal, programme, lender, title and primary-evidence verification remains an
   external human diligence step.

## 21. Recommended evolution

### Near term

- expand each GKA using licensed, authoritative and replayable connectors;
- generate the root release manifest from current pointers and policy versions;
- preserve dated knowledge vintages and collect realised outcomes;
- add regression cases from real user disagreements and overrides;
- improve frozen-report follow-up retrieval without allowing recomputation; and
- keep the recommendation narrative as carefully tested as the numeric engine.

### Medium term

- introduce durable, encrypted and tenant-scoped Case Knowledge when a paid institutional workflow
  requires it;
- add institution and adviser review/approval workflows;
- compare deterministic champions with statistically trained challengers on temporal holdouts;
- add calibrated outcome and subgroup stability reporting; and
- extract report blocks and evidence panels only after reuse across multiple products is proven.

### Long term

- use the Product Generator to scaffold new products from domain sources, GKA schema, decision
  logic and UI page declarations;
- maintain one ConSaaS artifact and release operating system across ten or more products;
- let most new products consist of connectors, schemas, policies and domain engines rather than
  infrastructure; and
- preserve the factory cadence: think, specify, ship, learn and repeat under a fixed Definition of
  Done.

## 22. Definition of done for a ConSaaS product increment

A feature is complete only when:

- the consequential user decision and acceptance criteria are explicit;
- the domain knowledge and case facts are represented canonically;
- deterministic and probabilistic responsibilities are documented;
- the engine produces a replayable result with evidence and change conditions;
- the customer receives a plain-English verdict and an executable next action;
- failure and insufficient-evidence outcomes are safe and intelligible;
- unit, integration, UI, architecture, security and applicable behavioral evaluations pass;
- the complete diff contains no unrelated work or secrets;
- documentation, versions, manifests and rollback instructions are current;
- the application remains runnable; and
- production is smoke-tested after deployment.

## 23. Final system identity

Vriddhi is the reference product that proved the architecture. ConSaaS Core is the reusable
operating system. The Golden Knowledge Asset is domain memory. The Case Knowledge Asset is customer
memory. The Decision Atlas is the precomputed decision universe. Domain engines own judgment. The
report engine turns judgment into action. The optional LLM makes the interaction human without
becoming the authority. The factory makes each next increment small, testable and cumulative.

That is the complete Vriddhi–ConSaaS architecture:

> Research the governed universe before the user arrives. Understand the user without turning the
> transcript into truth. Decide through explicit domain logic. Explain the result in plain English.
> Preserve the evidence. Promote only what can be replayed, tested and trusted.

## 24. Related authoritative references

- [`ARCHITECTURE.md`](ARCHITECTURE.md)
- [`CONSAAS_CONSTITUTION.md`](CONSAAS_CONSTITUTION.md)
- [`CONSAAS_PIPELINE.md`](CONSAAS_PIPELINE.md)
- [`GOLDEN_KNOWLEDGE_ASSET.md`](GOLDEN_KNOWLEDGE_ASSET.md)
- [`DECISION_ENGINE.md`](DECISION_ENGINE.md)
- [`PLUGIN_SDK.md`](PLUGIN_SDK.md)
- [`DECISION_UNIVERSE_ARCHITECTURE.md`](DECISION_UNIVERSE_ARCHITECTURE.md)
- [`CONVERSATIONAL_DECISION_INTELLIGENCE.md`](CONVERSATIONAL_DECISION_INTELLIGENCE.md)
- [`DECISION_STUDIO_REENGINEERING_V1.md`](DECISION_STUDIO_REENGINEERING_V1.md)
- [`DECISION_STUDIO_OPERATIONS.md`](DECISION_STUDIO_OPERATIONS.md)
- [`QUALITY_GATES.md`](QUALITY_GATES.md)
- [`DEFINITION_OF_DONE.md`](DEFINITION_OF_DONE.md)
- [`VRIDDHI_MODULE_INVENTORY.md`](VRIDDHI_MODULE_INVENTORY.md)
- [`adrs/core/ADR-CORE-001-DECISION-STUDIO-FOUNDATION.md`](adrs/core/ADR-CORE-001-DECISION-STUDIO-FOUNDATION.md)
- [`adrs/core/ADR-CORE-002-CONSULTING-AS-A-SERVICE.md`](adrs/core/ADR-CORE-002-CONSULTING-AS-A-SERVICE.md)
- [`adrs/core/ADR-CORE-003-GOVERNED-BROWSER-CONVERSATION.md`](adrs/core/ADR-CORE-003-GOVERNED-BROWSER-CONVERSATION.md)
- [`adrs/core/ADR-CORE-004-DOMAIN-DECISION-ENGINES-V1.md`](adrs/core/ADR-CORE-004-DOMAIN-DECISION-ENGINES-V1.md)
- [`adrs/core/ADR-CORE-005-PRECOMPUTED-DECISION-ATLAS.md`](adrs/core/ADR-CORE-005-PRECOMPUTED-DECISION-ATLAS.md)

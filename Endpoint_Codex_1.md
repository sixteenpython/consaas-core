# Endpoint Codex 1

**Checkpoint date:** 29 August 2026

**Purpose:** A sanitized, cross-product handoff for future Codex sessions working on ThinkMath / Advaitian Commentary Engine or Narrative Architect.
**Status:** This captures the architectural and operating context established through the session ending at this checkpoint. It is not a substitute for inspecting current code, Git state, applicable `AGENTS.md` files, tests, or newer ADRs.

## 1. How a future agent must use this checkpoint

Read this file completely before proposing or making a product change. Then:

1. Identify which repository and product the task concerns.
2. Read every applicable `AGENTS.md`, starting at the repository root.
3. Read the named task sheet and only the source, tests, contracts, skills, and ADRs relevant to that task.
4. Inspect the current branch, `git status`, recent commits, dependencies, and current implementation.
5. Treat current source code and newer versioned decisions as authoritative if they conflict with this dated checkpoint.
6. Restate the task boundary, protected areas, acceptance criteria, verification commands, deployment authority, and stop condition.
7. Preserve all unrelated user files and changes. Never stage broadly when exact files can be named.

Recommended cold-start prompt:

> Read `Endpoint_Codex_1.md` completely. Then read the applicable `AGENTS.md` and the task sheet I name. Inspect the current implementation and Git state before acting. Preserve unrelated work, do not cross the documented product boundaries, run the specified verification, and stop when the acceptance criteria are satisfied.

This checkpoint supplies orientation. A future agent must not assume that reading it authorizes implementation, deployment, destructive operations, external writes, or changes outside the user's explicit task.

## 2. Repository and deployment map

### ThinkMath / Advaitian Commentary Engine

- GitHub: `https://github.com/sixteenpython/advaitian-philosophy/tree/main/commentary_engine`
- Product directory: `commentary_engine/`
- Ordinary local checkout used by the owner: `C:\Users\ajayv\Documents\jupyter-python\advaitian-philosophy`
- Live Streamlit application: `https://advaitian-commentary-engine.streamlit.app/`
- Baseline Git state before this checkpoint commit: `30dcb24` on `origin/main`
- Last documented experience: ThinkMath Student Experience v3.2

### Narrative Architect

- GitHub: `https://github.com/sixteenpython/consaas-core/tree/main/narrative`
- Product directory: `narrative/`
- Ordinary local checkout used by the owner: `C:\Users\ajayv\Documents\jupyter-python\consaas-core`
- Live Streamlit application: `https://narrative-architect.streamlit.app/`
- Baseline Git state before this checkpoint commit: `9a081fc` on `origin/main`
- Current documented release: Screenplay Builder 0.3.0, NKA schema `narrative-nka/alpha-2`, compiler `screenplay-fountain/3`

### Hard scope boundary

Decision Studio is outside the Narrative product scope. Do not inspect, modify, refactor, test, commit, deploy, or otherwise disturb Decision Studio merely to simplify Narrative work. Narrative changes belong under `narrative/` except for a deliberately approved repository-level contract or checkpoint such as this file.

The two products share architectural doctrine but do not share canonical domain state. Do not merge the ThinkMath mathematics asset with the Narrative screenplay asset.

## 3. Shared architectural doctrine

These products are not prompt wrappers. They are governed hybrid-intelligence systems.

> The model proposes; deterministic tools test; application policy decides; the model communicates.

The common stack is:

1. A canonical, typed, versioned domain asset.
2. Deterministic state transitions, phase gates, identifiers, arithmetic, thresholds, and compilation.
3. Versioned cognitive doctrine or skill Markdown.
4. Open or open-weight models assigned bounded semantic or creative roles.
5. Typed model output treated as untrusted proposed data.
6. Grounding, schema, evidence, and policy validation before canonical acceptance.
7. Human authority over accepted mathematical knowledge or screenplay material.
8. Explicit provenance and release evidence.
9. Honest privacy, assurance, inference-capacity, and product-quality language.

The central state principle is:

> Conversation is the experience, but conversation is not canonical truth.

Chat can be summarized, compacted, or lost. Accepted state must remain in the appropriate canonical asset and in repository-resident contracts. A confident model statement does not become evidence merely because it is fluent.

## 4. ThinkMath product intent

ThinkMath is a Socratic olympiad-mathematics mentor designed to teach mathematical thinking and the Advaitian Six-Point framework. It must not collapse into an answer engine.

The intended learning transformation is:

```text
initial instinct
  -> observation
  -> Seed
  -> plausible directions
  -> Setup
  -> Move
  -> Closure
  -> checked Six-Point commentary
  -> same-Seed transfer
```

The Six-Point commentary payoff contains:

- Seed;
- Brute-force surface;
- Pivot;
- Pitfall;
- Connection;
- Takeaway.

The mentor should ask one useful question at a time, preserve student agency, avoid revealing the decisive move prematurely, and remain operationally useful when model inference is unavailable.

## 5. ThinkMath experience and canonical state

The public student experience has four primary views:

1. **Learn** — a calm, teacher-like conversation with one precise question per turn.
2. **Thinking Map** — a deterministic projection of accepted observations, Seed hypotheses, directions, proof obligations, and Setup–Move–Closure.
3. **Commentary** — the earned, structured Six-Point learning artifact with calibrated assurance.
4. **My Journey** — before/after reasoning, downloadable session material, and a Pattern Passport based on completed structures rather than points or streaks.

The four-level hint ladder is:

1. Small experiment — a useful test case without the solution.
2. Archetype nudge — a likely structural family without the operational move.
3. Direction map — plausible mechanisms and their differences without convergence.
4. Pivot shadow — the shape of the pivot while retaining the decisive step.

`thinkmath.domain.AdvaitianSession` is the source of truth. It records the problem, phase, student-grounded observations, Seed and archetype hypotheses, MVC, rejected approaches, connections, hint level, proof status, verification, provenance, mentor decisions, claim ledger, current obligation, reflection, and a bounded untrusted `ProblemMap`.

Three trust classes must remain distinct:

- **Student-grounded state:** accepted only when supported by the student's language.
- **Untrusted problem map:** model-inferred directions, misconceptions, obligations, and candidate MVC used for teaching but not credited to the student.
- **Reviewed or compiled knowledge:** curated maps and demonstrations that can be served without fresh analysis.

## 6. ThinkMath mentor intelligence

Human-like mentorship is implemented through deterministic pedagogical policy plus model judgment, not through persona prompting alone.

`conversation.classify_student_turn` distinguishes substantive work from confusion, “I don't know,” uncertainty, disagreement, example requests, simplification requests, and other recovery language. Recovery must never fabricate mathematical evidence or advance a phase.

The mentor policy selects a typed action such as:

- ask for an observation;
- narrow the current goal;
- test the smallest useful case;
- offer two bounded directions;
- demonstrate one justified micro-step;
- change representation;
- check a disputed or assertive claim;
- correct a reviewed misconception;
- compare directions;
- complete MVC;
- stress-test a proposed proof path;
- release checked commentary.

Repeated confusion increases support deterministically:

1. narrow the goal;
2. test the smallest useful case;
3. offer two concrete choices;
4. model one justified micro-step;
5. change representation and rebuild.

For substantial student work, the response must summarize the mathematical techniques actually attempted and identify one load-bearing proof obligation. It must not reset an advanced attempt to a generic opening question. `ensure_teacher_response` guards one-question-per-turn behavior, near-duplicate prompts, empty model responses, generic resets, and preservation of reviewed corrections.

## 7. ThinkMath progression, verification, and assurance

The canonical phases are:

| Phase | Purpose | Advancement requirement |
|---|---|---|
| Seed | Observe structure and form a hypothesis | Student-grounded observation, Seed, or archetype evidence |
| Directions | Compare mechanisms and build MVC | Structural hypothesis plus Setup–Move–Closure development |
| Convergence | Release synthesis | Complete, independently validated MVC |

An explicit request for a full answer or commentary cannot bypass an incomplete MVC. Setup–Move–Closure is a logical proof gate, not a field-population checklist. For descent, for example, the path must include both an extremal move and a valid boundary or termination mechanism.

Deterministic checks cover the Six-Point contract, restricted symbolic equivalence through a safe SymPy parser, known closure failures, MVC completeness, and phase/reveal gates. Arbitrary prose proofs are not formally certified by heuristics.

Checked commentary requires an independent qualified critic:

- critic output fails closed;
- missing or malformed output remains unverified;
- the mentor/commentary model cannot certify itself;
- deterministic failures override model confidence.

Student-facing assurance language distinguishes exploratory work, structural drafts, structurally checked work, unresolved mathematical review, and curated demonstrations. None implies general formal proof certification.

## 8. ThinkMath open-model and resilience architecture

Open models retain meaningful responsibility: interpreting informal reasoning, identifying candidate structures, comparing directions, drafting explanations, maintaining an untrusted working map, and speaking naturally. They do not own progression, truth, proof release, or canonical memory.

Provider doctrine:

- Ollama is the private, user-funded, local-first capacity route.
- Groq is an optional hosted route for registered open/open-weight models and remains quota-bound.
- SambaNova is intentionally unsupported under the documented billing condition.
- No paid proprietary LLM is a required application dependency.

Open weights do not imply unlimited hosted inference. Provider exhaustion is expected operational state, not an application failure. The fallback ladder should preserve the learning turn through smaller qualified routes, cached or compiled problem maps, curated journeys, and deterministic rendering of the already selected teaching action. Full proof release still fails closed without qualified verification.

Confident `ProblemMap` objects may be reused within a session and in a bounded 256-entry process-local LRU cache keyed by normalized problem fingerprint. Curated compiled maps establish a no-analysis route for reviewed demonstrations. Cache reuse is an availability optimization, not mathematical certification.

Privacy and persistence principles:

- sessions are private by default;
- Firebase persistence is opt-in through explicit save/commit actions;
- admin mode fails closed behind `ADMIN_PIN`;
- no fallback admin credential may exist;
- student-facing errors must not expose raw provider exceptions;
- local and hosted processing must be described honestly.

## 9. ThinkMath work completed in this session lineage

The recent sequence of improvements included:

- fitting prompts within hosted free-tier constraints;
- repairing structured-output/Markdown rendering and hiding private model state;
- redesigning the student experience around Learn, Thinking Map, Commentary, and My Journey;
- hardening open-model failover;
- fixing mobile visibility of the team login control;
- making mentoring conversational;
- accepting “I don't know,” confusion, uncertainty, partial answers, and substantial attempts;
- introducing deterministic recovery and humane-teacher guardrails;
- building the algorithmically governed hybrid mentor;
- clarifying closure obligations and proof assurance;
- aligning README and architecture documentation with the shipped system.

One observed Archetype Nudge response temporarily rendered a raw structured JSON block. A refresh later showed correct rendering, so no unrelated change was made solely for that transient symptom. Future regressions must be reproduced before patching.

The last documentation verification ran 24 focused dependency-free conversation, pedagogy, and student-experience tests successfully. A full suite was not rerun in that sandbox because optional Firebase, Groq, and SymPy dependencies were absent. The repository documents the normal command from `commentary_engine/` as:

```powershell
python -m unittest discover -s tests -v
```

Do not claim a current passing count without running the appropriate suite in the current environment.

## 10. Narrative Architect product intent

Narrative Architect is a screenplay construction studio whose purpose is to help an author build a structurally stronger, high-scoring first draft one approved layer at a time. It should feel like a construction engineer working from a blueprint, not a generic story chatbot.

The six phases are:

| Phase | Construction outcome |
|---|---|
| 1. Centre Knot | Lock the one-line dramatic knot, Booker plot family, genre, and tone |
| 2. Characters | Lock playable character sketches, objectives, contradictions, behavior, voice, and arcs |
| 3. Full Plot | Build and approve the complete causal plot |
| 4. Structure | Select and map the best screenplay structure |
| 5. Scene Construction | Engineer story-specific scenes as causal mini-plots |
| 6. Build & Score | Compile the accepted screenplay draft and evidence-facing scorecard |

The seven basic plot families and genre/tone are related inputs but must not be collapsed into one field. The five supported screenplay structures are Three Act, Freytag's Pyramid, Seven-Point Story, Save the Cat, and Non-linear. Three Act is the default, but the Architect should recommend the best fit from the approved plot.

## 11. Narrative canonical asset, phases, and authorship

The immutable Narrative Knowledge Asset (NKA) is canonical, not the chat transcript. It stores the centre knot, plot family, genre/tone, characters, plot, structure and beats, engineered scenes, locks, provenance, and revision lineage.

Core invariants:

- phase progression and lock order are deterministic;
- an upstream edit invalidates dependent downstream phases;
- stale writes are rejected;
- undo restores content as a new revision rather than rewriting history;
- generated content remains a proposal until the author accepts or locks it;
- compilation binds to one exact NKA revision;
- the author retains creative authority.

The hosted demo uses temporary session storage. Users must download project JSON before ending a hosted session. No confidential or unpublished screenplay material should be entered into the hosted demonstration.

## 12. Narrative skill-library and model boundary

The context and craft intelligence live in versioned skills rather than in one large prompt. The skill library includes screenplay concerns such as plot construction, character sketching, character building, structure selection, scene construction, scene assessment, and dialogue context/text/subtext.

Deterministic services own:

- identifiers, typed schema, and revision lineage;
- phase ordering, locks, invalidation, and readiness gates;
- structure templates and beat coverage;
- scoring weights, arithmetic, caps, and build gates;
- source/reference validation;
- Fountain and scorecard compilation;
- privacy boundaries and provenance.

Models may propose:

- centre-knot and plot alternatives;
- character ensembles and refinements;
- causal full-plot material;
- structure recommendations with rationale;
- story-specific scene action, conflict, reversals, behavior, dialogue, and subtext;
- evidence-facing craft critique.

Model output remains untrusted until typed validation and author approval. The optional private generator is a provider-neutral Ollama adapter restricted to loopback endpoints. The public hosted profile uses deterministic editable skill blueprints and sends no screenplay content to an external inference service.

## 13. Narrative scene-construction correction in Builder 0.3

Builder 0.2 proved the six-phase mechanics but exposed a serious quality problem during the “Accidental Chef” test. Phase 5 could populate every scene-card field with generic construction language such as “the first tactic fails,” “a choice changes the meaning,” or “the event is completed.” Placeholder locations and archetypal names could still receive 5/5 because the score measured field completeness rather than screenplay craft.

Builder 0.3 corrected this in two ways.

First, Phase 5 now generates editable story-grounded proposals using the approved centre knot, plot, cast, objectives, stakes, behavior, locations/props, structural beat, and adjacent causal events.

Second, the scorecard separates:

- **Completion coverage:** whether the required construction components exist.
- **Craft quality:** whether the text contains concrete, story-specific dramatic evidence.
- **Structural coverage:** whether accepted scenes serve the required screenplay beats.
- **Quality flags and build gates:** why a scene is capped or blocked.

The deterministic calibration is deliberately conservative:

- fully populated content may reach 5/5 completion without high craft;
- known boilerplate, structural-space headings, placeholder locations, and archetypal cast names cap craft at 2/5 and keep Phase 5 open;
- story-grounded Architect scaffolds cap craft at the 3/5 revision-ready floor until an author or approved local model completes a genuine craft pass;
- 5/5 craft requires story-specific evidence rather than populated fields;
- model-generated scores must cite exact scene evidence and remain untrusted until references validate.

The current iMaSc-derived score is a construction and revision diagnostic. It is not IMDb, expert certification, or a validated prediction of artistic or commercial success. Predictive claims would require an independently scored screenplay corpus and outcome validation.

## 14. Narrative scene contract and outputs

Every accepted scene should justify its existence through:

- a concrete playable location and time;
- the structural beat served;
- characters present and viewpoint;
- entry state and immediate objective;
- active resistance and mini-conflict;
- escalation, turning point, decision, and consequential exit state;
- character/emotional change proven through visible behavior;
- blocking and staging that externalize power or resistance;
- setup/payoff or causal connection to adjacent scenes;
- dialogue context, spoken text, and subtext.

Phase 6 compiles accepted material rather than inventing missing material. Outputs include a portable project JSON, Fountain screenplay draft, and evidence-facing Markdown scorecard bound to a specific source revision and compiler version.

Builder 0.3 was documented with 25 Narrative tests and 89 repository-wide tests at the release boundary, plus lint, formatting, focused type checks, architecture guardrails, local browser checks, and post-deployment verification. These are historical release facts; rerun current checks before claiming the present branch passes.

## 15. Narrative known limits and next priorities

Known limits at this checkpoint:

- no durable server-side project database;
- no screenplay PDF import or export;
- no authentication or multi-user collaboration;
- hosted sessions are temporary and not for confidential material;
- hosted generation is deterministic rather than generative inference;
- generated scenes remain disclosed scaffolds until a real craft pass;
- craft scoring is a revision aid, not expert review or commercial prediction;
- no completed evidence-bound SDI Four-Pillar analysis or Doctor mode.

Candidate next priorities, subject to a new task sheet and product-owner approval:

1. Detect repeated dramatic functions across adjacent scenes.
2. Add labelled, evidence-bound SDI Four-Pillar assessment alongside iMaSc.
3. Add continuity, setup/payoff, character-arc, and scene-dependency checks.
4. Package skills with schemas, rubrics, examples, and evaluations.
5. Add model-run provenance and proposal-review diffs.
6. Expand Fountain compilation into genuinely playable action and dialogue.
7. Calibrate deterministic craft checks against independent screenplay-expert review.

These are priorities, not blanket authorization to implement them.

## 16. Principal source map

### ThinkMath

- `commentary_engine/thinkmath/domain.py` — canonical `AdvaitianSession`.
- `commentary_engine/thinkmath/conversation.py` — turn and recovery classification.
- `commentary_engine/thinkmath/mentor_engine.py` — teaching policy, problem maps, grounding, caching, and guardrails.
- `commentary_engine/thinkmath/state_machine.py` — deterministic learning-phase gates.
- `commentary_engine/thinkmath/verification.py` — restricted symbolic and commentary checks.
- `commentary_engine/thinkmath/model_registry.py` — model role, capability, and licence routing.
- `commentary_engine/thinkmath/resilience.py` — provider classification and fallback.
- `commentary_engine/thinkmath/structured_output.py` — typed untrusted model-envelope parsing.
- `commentary_engine/thinkmath/rendering.py` — private-state removal and visible-response repair.
- `commentary_engine/thinkmath/student_experience.py` — deterministic view models.
- `commentary_engine/thinkmath/student_ui.py` — Streamlit presentation.
- `commentary_engine/app.py` — orchestration.

### Narrative Architect

- `narrative/src/narrative_architect/knowledge/nka.py` — canonical immutable NKA.
- `narrative/src/narrative_architect/application/projects.py` — construction services and phase locks.
- `narrative/src/narrative_architect/construction/blueprints.py` — deterministic construction intelligence.
- `narrative/src/narrative_architect/construction/scoring.py` — completion/craft arithmetic, quality flags, caps, and build gates.
- `narrative/src/narrative_architect/inference/local_model.py` — loopback-only Ollama boundary.
- `narrative/src/narrative_architect/create/compiler.py` — Fountain and scorecard compilation.
- `narrative/src/narrative_architect/ui/app.py` — six-phase Streamlit studio.
- `narrative/skills/*.md` — versioned screenplay craft library.
- `narrative/tests/` — domain, workflow, compiler, privacy, and UI verification.

## 17. Git, deployment, and safety contract

- Inspect status before editing; existing changes belong to the user unless proven otherwise.
- Stage exact files. Never commit local secrets, credential files, reference books, attachments, or unrelated course material.
- Use non-destructive Git operations. Never use `reset --hard` or discard user work without explicit authorization.
- Fetch before push and integrate remote changes without overwriting intervening work.
- Push or deploy only when the user explicitly asks.
- For Narrative, touch only the Narrative product unless a repository-level change is explicitly required.
- Run focused tests proportional to the change, then broader release checks when risk or deployment warrants them.
- Verify a live deployment rather than assuming that a successful push proves the app is healthy.
- Report exact verification evidence, known gaps, and whether local and remote heads match.

At the end of the documentation session preceding this checkpoint, the ordinary local checkouts and `origin/main` matched at `30dcb24` for Advaitian and `9a081fc` for ConSaaS/Narrative. Pre-existing untracked private/reference/course materials were deliberately preserved and must remain untouched.

## 18. Codex operating-model finding

The initial assessment of Codex was that it offers high autonomous execution depth but benefits from detailed task definitions because operational visibility and steering may be less continuous than a terminal-first pairing workflow.

Deeper longitudinal testing refined that verdict.

At cold start, an open-ended request requires the agent to acquire product intent, architecture, constraints, conventions, tests, deployment knowledge, and quality standards. A detailed user story or plan-first discovery phase is therefore valuable.

Inside a mature project conversation, or when equivalent trusted context has been capitalized in the repository, the latest message is only a delta against an established working model. A short request can then be sufficient because the accumulated context functions as an evolving project specification.

> Codex benefits from detailed task definitions at cold start. Once sufficient project context has been established, it can often interpret intent-level instructions reliably, preserve architectural continuity, and deliver complex incremental changes with substantially less specification.

The key relationship is:

> Required prompt specificity decreases as reliable, relevant, and current project context increases.

This does not eliminate the need for scope and verification. It changes their form: architecture and durable rules live in the repository, while the new prompt states the bounded change.

## 19. Free-tier execution strategy

The expensive context-acquisition phase has largely been converted into repository-resident architecture, contracts, skills, tests, release notes, and this checkpoint. Future work is expected to be moderate, targeted, and driven by detailed task sheets derived from client feedback.

The intended operating model is:

> The architecture is capitalized in the repository. Codex is no longer being used primarily to discover what the system is; it is being used to execute verified changes against established contracts.

Free-tier Codex can be the default lane for quick, bounded implementation work, but it is not guaranteed production capacity. Limits may depend on model, task complexity, context, tools, local/cloud execution, and service policy. Do not design release obligations around an assumption of unlimited free inference.

Operational safeguards:

- each developer uses an authorized individual account;
- GitHub, task sheets, tests, and CI are the shared system of record, not private chat memory;
- confidential client feedback is sanitized and handled according to applicable data-control and contractual requirements;
- routine tasks use an appropriately efficient model;
- architectural ambiguity, high-risk changes, or final release review may justify stronger reasoning or a paid fallback;
- keep a small paid seat or usage-based API option available if uninterrupted delivery matters;
- measure actual usage and correction cost through a representative pilot rather than assuming capacity.

This is not merely “downgrading Enterprise to Free.” It is a transition from exploratory architecture acquisition to constrained execution. The transition succeeds only if the repository remains current, the tasks remain bounded, and verification remains non-negotiable.

## 20. Standard task-sheet contract

Future product updates should use a task file resembling:

```markdown
# NARRATIVE-017 — Short outcome title

## Product and repository
- Product: Narrative Architect
- Repository/path: `consaas-core/narrative`

## Goal
One observable outcome.

## Client evidence
Sanitized feedback, reproduction steps, examples, screenshots, or measured failure.

## Existing contracts
Name the relevant architecture section, skill, ADR, schema, and invariant.

## In scope
- Exact behavior and components permitted to change.

## Protected boundaries
- Files, products, data contracts, privacy rules, or architecture that must not change.

## Acceptance criteria
- Concrete, observable conditions.
- Required negative cases and quality thresholds.

## Verification
- Focused tests.
- Regression suite.
- Lint/type/format checks.
- Browser or deployment verification when applicable.

## Deployment authority
State explicitly whether commit, push, and deployment are authorized.

## Stop condition
Stop when every acceptance criterion passes; report unresolved risks rather than expanding scope.

## Rollback
State the safe reversal path for consequential changes.
```

A mature invocation can then be concise:

> Implement `NARRATIVE-017` according to the existing contracts. Do not modify the protected boundaries. Run the specified tests and stop when the acceptance criteria are satisfied.

## 21. Final continuity statement

The enduring asset created through this work is not a collection of large prompts. It is a pair of explicit, governed product architectures:

- ThinkMath can feel humane because models perform genuine semantic work while deterministic pedagogy protects student agency, progression, and proof integrity.
- Narrative Architect can remain creative because models may generate meaningful story material while the immutable NKA, skill library, phase gates, evidence, scoring mechanics, and author approval protect coherence and authorship.

Future agents should preserve this principle:

> Keep domain intelligence explicit, versioned, testable, and inspectable. Use language models diligently where semantic or creative judgment improves the experience. Never make the model the sole owner of truth, progression, arithmetic, or canonical memory.

# UI Architecture

## Experience model

Conversation occupies the primary workspace; knowledge, scenes, characters, analysis, and evidence are contextual companions. This is not a generic chat transcript with tabs attached.

## Streamlit shell

```text
Sidebar: project, Create/Doctor mode, revision, model/runtime health
Main: expert conversation + contextual action/proposal cards
Inspector: Knowledge | Scenes | Characters | SDI | Evidence
Bottom/action rail: pending changes, compile/upload, stale-analysis status
```

On narrow screens the inspector becomes navigable panels. Session state holds presentation state and current IDs only; application services reload authoritative data.

## Required views

1. Mode/project selection with clear shared-NKA loop.
2. Conversational workspace with expert status, evidence citations, proposals, confirm/reject/undo.
3. Narrative Knowledge view grouped by fact/inference/proposal/open question.
4. Scene list/detail with objective, conflict, outcome, dialogue/subtext, provenance.
5. Character view with objective, motivation, relationships, arc evidence.
6. Compilation readiness, bounded/full compile, artifact history/download.
7. Local PDF upload, parse progress, uncertainty review, import confirmation.
8. SDI scorecard with four pillars and explicit scales.
9. Momentum graph with act/sequence bands and click-through.
10. Findings and prioritized recommendations.
11. Evidence drawer: finding -> score -> scene -> source page/block.
12. Conversational Script Doctor using the selected scene/finding as focus.

## Interaction states

Long local inference is cancellable and shows stage rather than fabricated progress. Analysis locks to a revision; edits display “analysis stale” and offer rerun. Model missing/slow states preserve deterministic editing and compilation.

## Trust language

Visual badges distinguish Extracted, Author-confirmed, Inferred, SDI score, Observation, Recommendation, and Beyond-SDI extension. Confidence appears only where meaningful. Every score label contains `0–5` or `/20`. The product boundary against success prediction appears in onboarding and diagnostic reports without dominating conversation.

## Authorial control

Material NKA changes render as a reviewable diff with Accept, Modify, Reject. Recommendations never expose a one-click silent rewrite. Generated screenplay text is visibly proposed until accepted.

## Accessibility and privacy

Keyboard-accessible navigation, non-color status cues, chart alternatives/table view, readable evidence excerpts, and local-processing indicators are mandatory. Upload screens state that screenplay content remains local. No analytics captures content.

## UI boundary

Streamlit calls typed application use cases and renders view models. It performs no parsing, model prompting, scoring, provenance traversal, or database mutation directly.

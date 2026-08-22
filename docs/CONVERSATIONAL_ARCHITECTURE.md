# Conversational Architecture

## Principle

Chat is the primary interface but not persistence. A conversation is an ordered interaction log linked to project revisions; the NKA head is the story truth.

## Turn pipeline

1. Persist the raw user message locally with conversation and project IDs.
2. Classify intent and requested authority: discuss, inspect, propose, mutate, compile, diagnose.
3. Load project head and detect whether the user’s base view is stale.
4. Build task context from NKA queries, active diagnostics, source evidence, and compact interaction summary.
5. Ask the local model for a schema-constrained `ExpertTurnPlan`.
6. Execute allowed read tools; validate returned claims and citations.
7. If mutation is proposed, build and validate a typed change set.
8. Auto-apply safe explicit edits or request confirmation for ambiguous/material changes.
9. Commit a new NKA revision atomically when authorized.
10. Render the response with “what changed,” evidence, open questions, and next action.

## Conversation state

Stored separately:

- immutable raw messages and attachments;
- derived interaction summary, replaceable and versioned;
- pending proposals/confirmations;
- conversation focus (entities/scenes currently discussed);
- user preferences and declared constraints;
- revision before/after each mutating turn;
- model/tool run manifests.

Deleting conversational history does not delete NKA revisions. Deleting a project follows a local secure-deletion policy across all artifacts.

## Tool surface

The VSE receives narrow tools: query entity/scene, search evidence, list contradictions/open questions, preview patch, apply confirmed patch, request analysis, explain score, compile revision, compare revisions, and navigate source. Tools return typed data with evidence IDs. There is no general filesystem, SQL, shell, or network tool.

## Context construction

Use deterministic budgets: system/SDI policy, user turn, focused entities, neighboring scenes, active findings, then retrieved evidence. Summaries identify their source revision and are never cited as screenplay evidence. If context is insufficient, the expert asks or retrieves rather than improvises.

## Confirmation levels

- **None:** read-only analysis, formatting, exact explicit field edits.
- **Recommended:** reversible inference acceptance, minor merge/normalization.
- **Required:** generated story content, deletion, scene split/merge/reorder, replacing confirmed facts, accepting parser ambiguity, applying doctor recommendations.

The user can undo by moving the project head to a descendant created from an earlier revision; history remains immutable.

## Streaming and interruption

Prose may stream only after tool-dependent factual claims are resolved. Structured mutations are never parsed from partially streamed text. Cancellation leaves no partial revision. A resumable turn records completed read tools but repeats no mutation without its idempotency key.

## Failure behavior

If the model is unavailable, users retain deterministic NKA navigation, editing, compilation, stored diagnostics, and exports. If structured planning fails validation, retry within policy, then provide a transparent degraded response without mutation.

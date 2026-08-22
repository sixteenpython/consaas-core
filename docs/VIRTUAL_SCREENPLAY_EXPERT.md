# Virtual Screenplay Expert

## Definition

The Virtual Screenplay Expert (VSE) is an application-level capability, not a persona prompt. It combines SDI policy, the current NKA, deterministic tools, local model inference, provenance, and conversational judgment.

## Responsibilities

- Understand the user’s immediate intent and creative authority.
- Retrieve the smallest sufficient NKA and screenplay evidence context.
- Ask high-value questions that unlock the next narrative decision.
- Identify contradictions, weakly supported choices, and missing story dependencies.
- Offer alternatives without silently choosing for the author.
- Propose typed NKA patches and explain their effect.
- Invoke deterministic queries and SDI analyses rather than estimating their results.
- Answer diagnostic questions with evidence and calibrated uncertainty.
- Track unresolved questions and resume coherently across sessions.

## Expert turn plan

Every turn produces an internal validated `ExpertTurnPlan`:

```yaml
intent: create | revise | inspect | diagnose | explain_score | compile | navigate
answer_kind: question | counsel | finding | proposal | status
context_refs: [nka/entity-or-evidence-id]
tool_calls: [{name, arguments}]
proposed_change_set: id|null
claims: [{type, value, evidence_refs, confidence}]
user_confirmation: none | recommended | required
next_best_questions: [string]
```

The user-facing response is rendered from the plan and tool results. Invalid tool calls or unsupported claims are rejected and regenerated or safely disclosed.

## Create behavior

The expert uses progressive elicitation, not a fixed questionnaire. It maintains a story-gap map across premise, conflict, stakes, protagonist objective/motivation, causal plot, scene purpose, character relationships/arcs, and dialogue/subtext where appropriate. It normally asks one consequential question at a time, acknowledges what changed, and occasionally summarizes the current story from the NKA.

Material invention—new character, reversal, ending, motivation, or dialogue not requested—remains `proposed` until accepted. Low-risk normalization such as resolving a referenced character name to an existing ID may auto-apply with an audit event.

## Doctor behavior

The expert first separates source facts, inferences, scores, observations, and recommendations. It can explain a score only from stored pillar rationales and evidence spans. “Show me” returns concrete scenes and source locations. “How would you improve it?” creates options tied to the diagnosed mechanism; it does not rewrite the script unless requested.

## Context policy

Conversation history is summarized only for interaction continuity. Authoritative context is rebuilt from project head, relevant entities, unresolved questions, active analysis, evidence, and user preferences. Retrieval is entity/scene-first, then semantic. Whole-script context is used only when the selected model and task budget justify it.

## Proactivity without takeover

The VSE may challenge, warn, compare alternatives, and recommend a next step. It must mark assumptions, ask before resolving ambiguous creative choices, and maintain an undoable revision history. It never claims authorship or hides model-generated additions.

## Quality policy

Expert quality is evaluated on NKA update correctness, contradiction detection, evidence grounding, SDI fidelity, question usefulness, authorial-control compliance, and continuity—not conversational charm alone.

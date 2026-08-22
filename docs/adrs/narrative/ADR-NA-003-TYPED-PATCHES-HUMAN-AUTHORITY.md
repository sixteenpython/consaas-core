# ADR-NA-003: Typed Patches Preserve Human Authorship

Status: Proposed  
Date: 2026-08-17

## Context

A screenplay expert should be proactive, but silent generated changes transfer creative ownership to the system and make revisions unauditable.

## Decision

LLMs return schema-constrained expert plans and proposed typed change sets. Application services validate them. Material invention, replacement, deletion, merge/split, or reorder requires user confirmation before a new revision is committed.

## Consequences

The expert can challenge and suggest while the human remains author. Some turns require an extra confirmation. Low-risk explicit edits may auto-apply under documented policy and remain undoable.

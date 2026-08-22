"""Canonical Narrative Knowledge Asset contracts."""

from narrative_architect.knowledge.nka import (
    Character,
    InMemoryProjectRepository,
    NarrativeState,
    NKARevision,
    NKAValidationError,
    Scene,
    StaleRevisionError,
)
from narrative_architect.knowledge.statements import (
    EpistemicStatus,
    EvidenceRef,
    NarrativeStatement,
    StatementValidationError,
    create_user_statement,
    validate_model_statement,
)

__all__ = [
    "Character",
    "EpistemicStatus",
    "EvidenceRef",
    "InMemoryProjectRepository",
    "NKARevision",
    "NKAValidationError",
    "NarrativeState",
    "NarrativeStatement",
    "Scene",
    "StaleRevisionError",
    "StatementValidationError",
    "create_user_statement",
    "validate_model_statement",
]

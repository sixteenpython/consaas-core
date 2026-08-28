from dataclasses import replace

import pytest
from narrative_architect.application.projects import StoryProjectService, demo_repository
from narrative_architect.conversation.guide import apply_guided_answer, next_guidance_step
from narrative_architect.create.compiler import assess_readiness, compile_bounded_fountain
from narrative_architect.knowledge.nka import (
    InMemoryProjectRepository,
    NKAValidationError,
    StaleRevisionError,
)


def test_revision_is_immutable_and_stale_write_fails() -> None:
    repository = InMemoryProjectRepository.create("A Story")
    original = repository.head
    changed_state = replace(original.state, premise="A pilot must land without instruments.")

    current = repository.commit(original.revision_id, changed_state, "Establish premise")

    assert repository.get(original.revision_id).state.premise == ""
    assert current.state.premise.startswith("A pilot")
    with pytest.raises(StaleRevisionError):
        repository.commit(original.revision_id, changed_state, "Stale edit")


def test_undo_creates_descendant_without_erasing_history() -> None:
    repository = InMemoryProjectRepository.create("A Story")
    service = StoryProjectService(repository)
    original_id = repository.head_revision_id
    service.update_story("Add premise", premise="A promise is broken.")
    changed_id = repository.head_revision_id

    restored = service.restore(original_id)

    assert restored.parent_revision_id == changed_id
    assert restored.state.premise == ""
    assert len(repository.history) == 3
    assert repository.get(changed_id).state.premise == "A promise is broken."


def test_project_bundle_round_trips_all_revisions() -> None:
    repository = demo_repository()

    imported = InMemoryProjectRepository.import_json(repository.export_json())

    assert imported.project_id == repository.project_id
    assert imported.head_revision_id == repository.head_revision_id
    assert imported.history == repository.history
    assert imported.head.state.locked_phases == (1, 2, 3, 4, 5)
    assert imported.head.state.scenes[2].outcome


def test_project_bundle_rejects_tampered_revision() -> None:
    bundle = demo_repository().export_json().replace("The Last Signal", "Changed Signal", 1)

    with pytest.raises(NKAValidationError, match="content hash"):
        InMemoryProjectRepository.import_json(bundle)


def test_guidance_reads_nka_and_preserves_answer() -> None:
    service = StoryProjectService(InMemoryProjectRepository.create("A Story"))
    first = next_guidance_step(service.head.state)
    assert first is not None and first.key == "premise"

    message = apply_guided_answer(service, first, "A dancer loses her sense of rhythm.")
    second = next_guidance_step(service.head.state)

    assert "canonical Narrative Knowledge Asset" in message
    assert service.head.state.premise.startswith("A dancer")
    assert second is not None and second.key == "protagonist"


def test_demo_compiler_is_deterministic_and_source_bound() -> None:
    repository = demo_repository()
    report = assess_readiness(repository.head.state)

    first = compile_bounded_fountain(repository.head)
    second = compile_bounded_fountain(repository.head)

    assert report.can_compile
    assert first == second
    assert "INT. LIGHTHOUSE LANTERN ROOM - DAY" in first
    assert "Mira Sen" in first
    assert repository.head_revision_id in first
    assert "accepted Narrative Knowledge Asset" in first


def test_empty_project_cannot_compile() -> None:
    repository = InMemoryProjectRepository.create()
    report = assess_readiness(repository.head.state)

    assert not report.can_compile
    assert "Lock the one-line centre knot." in report.blockers
    with pytest.raises(ValueError, match="Compilation blocked"):
        compile_bounded_fountain(repository.head)

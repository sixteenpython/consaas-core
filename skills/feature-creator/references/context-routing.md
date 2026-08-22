# Context Routing

## Always read

`README.md`, `docs/CONSAAS_CONSTITUTION.md`, `AGENTS.md`, `docs/DEFINITION_OF_DONE.md`, and the relevant task/feature conventions.

## Product routes

- Narrative: `narrative/README.md`, `narrative/AGENTS.md`, `docs/NARRATIVE_*`, `docs/VIRTUAL_SCREENPLAY_EXPERT.md`, `docs/SDI_*`, `docs/SIS_ENGINE.md`, `docs/SCREENPLAY_*`, Narrative ADRs, related backlog/tests/evals.
- Vriddhi: `vriddhi/README.md`, `vriddhi/AGENTS.md`, `docs/VRIDDHI_MODULE_INVENTORY.md`, Core/Vriddhi roadmap and related backlog. Inspect the external production repository only when in task scope.
- HouseWise/CareerSim: product README/scaffold, relevant planned specs/backlog. If product meaning is not defined, remain DRAFT and ask the minimum product question.
- Core/AI/EVAL/Foundation: Constitution, Core architecture/SDK, relevant governance docs, model registry/eval docs, ADRs, implementation/tests.

## Search order

1. `rg -n "<user terms>" backlog docs <product> tests evals core factory`
2. Search exact feature IDs/titles and synonyms.
3. List relevant module/test filenames.
4. Open only matching architecture, code, tests, and backlog files.

Do not load source papers, generated artifacts, whole repositories, or unrelated product documents unless a match/dependency requires them.

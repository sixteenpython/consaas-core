# ConSaaS Factory Status

**Bootstrap state:** implementation complete locally; human and GitLab review pending.

**Continuity checkpoint:** `Endpoint_Codex_ConSaaS.md` is the authoritative cold-start handoff for
free-tier Codex and junior-developer execution across the product family. It supplies orientation;
current tasks, code, ADRs, `AGENTS.md` files and tests remain implementation authority.

## Operational capabilities

- Constitution, factory lifecycle, Definition of Done, standards, and scoped agent instructions
- Feature Creator skill with DRAFT, READY, and BACKLOG modes
- Feature, task, and product templates
- Provider-neutral local LLM contract, loopback-only Ollama adapter, and licensed model registry
- Architecture guardrails, unit tests, offline AI evaluation, and GitLab CI definition
- Dependency-ordered backlog and one end-to-end Narrative implementation demonstration
- Decision Studio v0.3 free-form consultation, epistemic Case Knowledge, a live Decision Position,
  and optional provider-free browser inference behind a typed validation gate
- Decision Studio v0.4 scenario/Pareto education and property engines, India Problem Observatory,
  and deterministic 70/30 Horse/Jockey startup adjudication

## Deliberate limits

- Narrative Architect now has a deployable deterministic Foundation Alpha for Create mode. It is
  deliberately smaller than Vertical Slice 1: local LLM proposals, durable SQLite storage,
  screenplay PDF output, full NKA v1, and Doctor mode remain unbuilt.
- CareerSim and HouseWise are bounded Foundation applications; exact programme and property
  diligence connectors remain future work.
- Vriddhi has not been rewritten or moved.
- No Core abstraction is promoted solely from one product.
- No GitLab pipeline or merge request is claimed: the configured repository currently has only a GitHub remote.
- Browser inference remains device-dependent and opt-in; the deterministic consultation remains
  complete when WebGPU or model inference is unavailable.

See `factory/status.json` for machine-readable state and `docs/REMAINING_GAPS.md` for activation work.

# Feature Specification Output Contract

Start with YAML-like metadata: `id`, `mode`, `status`, `product`, `type`, `owner`, `created`, `dependencies`, and `readiness`.

Then include exactly these headings:

1. Feature ID
2. Title
3. Product
4. Feature Type
5. User Story
6. User Problem
7. Business / Product Objective
8. Context
9. Existing Capability
10. Proposed Capability
11. Knowledge Asset Impact
12. Decision Intelligence Impact
13. Deterministic Components
14. LLM / AI Components
15. Inputs
16. Outputs
17. Provenance Requirements
18. Versioning Requirements
19. Dependencies
20. Architecture Impact
21. Core Reuse Candidates
22. Acceptance Criteria
23. Test Requirements
24. AI Evaluation Requirements
25. Security / Privacy Considerations
26. Observability Requirements
27. Explicitly Out of Scope
28. Definition of Done
29. Implementation Notes
30. Suggested Task Breakdown
31. Dependency Graph
32. Risks / Open Questions

Acceptance criteria must be observable and numbered. Tasks must be independently executable, dependency ordered, and leave the product runnable. Explicitly say “Not applicable” with rationale instead of omitting AI, security, provenance, or rollback considerations.

# Feature Creator

Feature Creator is the controlled intake mechanism for ConSaaS product ideas. It converts an idea into an inspectable feature specification; it does not bypass architecture, invent missing decision semantics, or start implementation implicitly.

## Invocation

Use `$feature-creator`, `/feature`, or explicitly ask to use Feature Creator. Choose one mode:

- `DRAFT`: explore and expose unresolved questions.
- `READY`: produce a complete, implementation-ready specification without changing the backlog.
- `BACKLOG`: produce a ready specification, allocate an ID, and add it to the backlog.

## Required behaviour

The skill reads only relevant product and platform context, checks for duplication, separates domain intelligence from platform capability, records deterministic and AI responsibilities, and asks only the minimum blocking clarification. It stops if the request conflicts with the Constitution.

Feature IDs use the owning namespace, such as `CORE-001`, `AI-001`, `NARRATIVE-001`, `VRIDDHI-001`, `HOUSEWISE-001`, or `CAREERSIM-001`. Executable tasks extend the feature ID, for example `NARRATIVE-001-T01`.

## Output

Every ready feature contains the problem, user outcome, scope, non-goals, acceptance criteria, architecture impact, data and provenance impact, security/privacy implications, deterministic/AI boundary, tests, evaluations, dependencies, rollout, observability, and unresolved risks.

Feature Creator proposes work. The normal factory lifecycle and human review still govern execution.

# ConSaaS Factory Mode

## Operating model

The factory turns human product intent into controlled, reviewable implementation work. It is not an autonomous coding swarm.

`Idea -> Feature Creator -> Feature Specification -> Backlog -> Task -> Developer + Agent -> Code -> Tests/Evals -> CI -> MR -> Review -> Deploy -> Feedback`

## Work-item hierarchy

- **Feature:** user/business capability and its architecture-aware vertical slices.
- **Task:** independently executable implementation increment with one owner and verifiable output.
- **ADR:** required when a consequential architectural choice is new or conflicts with accepted design.
- **Evaluation case:** versioned behavioral expectation for probabilistic components.

## Lifecycle

`BACKLOG -> READY -> IN_PROGRESS -> TESTING -> REVIEW -> DONE`

- BACKLOG: valuable but missing readiness or scheduled dependencies.
- READY: decisions resolved, dependencies available, acceptance/tests defined.
- IN_PROGRESS: assigned branch and owner.
- TESTING: implementation complete; gates executing.
- REVIEW: CI/evals pass and MR evidence is complete.
- DONE: reviewed, merged/deployed as applicable, status/docs updated.

Transitions are explicit in the task front matter and `factory/status.json`. A feature can contain tasks in different states.

## IDs

Use monotonically increasing, never-reused IDs per namespace: `FOUNDATION-xxx`, `CORE-xxx`, `AI-xxx`, `EVAL-xxx`, `VRIDDHI-xxx`, `NARRATIVE-xxx`, `HOUSEWISE-xxx`, `CAREERSIM-xxx`. Feature Creator scans specifications, tasks, and status before allocating the next number.

## Ready policy

A task is READY only when objective, scope/out-of-scope, architecture context, dependencies, inputs/outputs, acceptance criteria, tests, AI evaluations, privacy/security, rollback, and Definition of Done are actionable. Unresolved product judgment remains BACKLOG/DRAFT.

## Branch and review policy

Use a short-lived branch such as `codex/<task-id>-slug` or team convention. One task may produce multiple commits but one coherent MR. The MR links feature/task/ADRs, summarizes diff, contains commands/results, risks, rollback, and screenshots/artifacts where relevant.

## Founder and developer roles

The Founder/Product Owner owns vision, prioritization, product acceptance, architectural exceptions, security/business decisions, and usefulness. Junior developers implement READY tasks and escalate architectural ambiguity. Agents accelerate implementation within the same authority.

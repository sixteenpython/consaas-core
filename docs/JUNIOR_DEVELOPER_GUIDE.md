# Junior Developer Guide

## Execute a READY task

1. Select a READY task from `backlog/tasks/` and confirm dependencies/status in `factory/status.json`.
2. Read `README.md`, the Constitution, root/product `AGENTS.md`, task, linked architecture, ADRs, tests, and evaluations.
3. Create a short-lived task branch.
4. Ask the coding agent: “Execute `TASK-ID` according to the ConSaaS Factory.”
5. Review the agent’s scope statement before accepting edits. You remain responsible for the branch.
6. Implement in small increments; do not redesign or broaden scope.
7. Run local factory checks: format, lint, types, tests, architecture guardrails, security/dependency scans, and applicable AI evaluations.
8. Inspect the full diff, generated artifacts, logs, and dependency changes.
9. Update task status, documentation, and factory status.
10. Open an MR using the task ID; include commands/results, risks, limitations, screenshots/evidence, and rollback.
11. Respond to CI/review by fixing causes, not weakening gates.
12. After approval/merge/deploy, verify the outcome and mark DONE.

## Escalate instead of guessing

Stop when product meaning is undefined, acceptance criteria conflict, canonical data/architecture must change, security/privacy is uncertain, a Core promotion is proposed, production Vriddhi is at risk, or the required model/license is not approved. Record the question and owner; do not invent the decision.

## Review checklist

- Can you explain every changed file?
- Is the feature still the smallest useful slice?
- Are deterministic and model responsibilities separated?
- Can an important output be traced to inputs and versions?
- Do tests fail when the implementation is deliberately broken?
- Does the product still run without hidden local state?
- Is rollback practical?

Junior developers are implementers and active reviewers, not uncontrolled architects. Asking the correct blocking question is successful execution.

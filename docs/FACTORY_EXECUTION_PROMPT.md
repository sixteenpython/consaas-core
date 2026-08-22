# Factory execution prompt

Use this prompt for a bounded implementation task:

> Execute task `<TASK-ID>` from `backlog/tasks`. Read the root and nearest product `AGENTS.md`, the Constitution, the linked feature, and only the architecture documents named by the task. Confirm the task is READY and has no unresolved blocker. Implement only its stated scope. Preserve deterministic/AI boundaries and provenance. Add or update tests and evaluations, run every listed verification command, inspect the diff, update task status and documentation, then report changed files, evidence, risks, and remaining work. Stop rather than silently resolving an architectural conflict.

This prompt delegates execution, not product authority. A human still reviews consequential architectural, privacy, and product decisions.


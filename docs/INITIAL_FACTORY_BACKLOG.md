# Initial dependency-ordered factory backlog

| Order | ID | Outcome | Depends on | Status |
|---:|---|---|---|---|
| 1 | FOUNDATION-001 | Constitution and authority hierarchy | — | REVIEW |
| 2 | FOUNDATION-002 | Root/product agent operating contracts | FOUNDATION-001 | REVIEW |
| 3 | FOUNDATION-003 | Feature Creator skill | FOUNDATION-001 | REVIEW |
| 4 | FOUNDATION-004 | Feature/task/product templates | FOUNDATION-002 | REVIEW |
| 5 | CORE-001 | GitLab quality-gate pipeline | FOUNDATION-001 | REVIEW |
| 6 | CORE-002 | Executable architecture guardrails | CORE-001 | REVIEW |
| 7 | AI-001 | Provider-neutral local AI abstraction | FOUNDATION-001 | REVIEW |
| 8 | AI-002 | Licensed model registry and selection | AI-001 | REVIEW |
| 9 | EVAL-001 | Offline AI evaluation convention | AI-001 | REVIEW |
| 10 | FOUNDATION-005 | Factory index and machine-readable status | FOUNDATION-001 | REVIEW |
| 11 | NARRATIVE-001 | Validated AI-to-NKA statement gate | AI-001, EVAL-001 | REVIEW |
| 12 | NARRATIVE-002 | Narrative Knowledge Asset domain spine | NARRATIVE-001 | READY |
| 13 | NARRATIVE-003 | Compare two immutable scene versions | NARRATIVE-002 | BACKLOG |
| 14 | CORE-003 | Extract a proven artifact lifecycle from two products | NARRATIVE-002, Vriddhi evidence | BACKLOG |

`REVIEW` means implemented locally but not yet accepted through an actual GitLab merge request. GitLab repository and runner configuration remain an external prerequisite.


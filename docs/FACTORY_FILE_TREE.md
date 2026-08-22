# Factory file tree

```text
consaas-core/
├── AGENTS.md
├── FACTORY_STATUS.md
├── README.md
├── pyproject.toml
├── .gitlab-ci.yml
├── backlog/
│   ├── README.md
│   ├── index.json
│   ├── features/
│   │   ├── NARRATIVE-001_VALIDATED_NKA_STATEMENT_INGESTION.md
│   │   └── NARRATIVE-003_SCENE_VERSION_COMPARISON.md
│   └── tasks/
│       ├── NARRATIVE-001-T01_VALIDATED_NKA_STATEMENT_GATE.md
│       └── NARRATIVE-002-T01_NKA_DOMAIN_SPINE.md
├── core/ai/
│   ├── contracts.py
│   ├── registry.py
│   └── adapters/ollama.py
├── factory/
│   ├── guardrails.py
│   ├── model_registry.json
│   └── status.json
├── skills/feature-creator/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/{context-routing.md,output-contract.md}
│   └── scripts/next_feature_id.py
├── templates/
│   ├── feature/FEATURE_TEMPLATE.md
│   ├── task/TASK_TEMPLATE.md
│   └── consaas-product/
│       ├── {README.md,AGENTS.md}
│       ├── docs/{PRODUCT_SPEC,ARCHITECTURE,KNOWLEDGE_ASSET,INTELLIGENCE,EVALUATION,ROADMAP}.md
│       └── {src,tests,evals}/
├── evals/
│   ├── README.md
│   ├── run_nka_statement_eval.py
│   └── narrative/nka_statement_validation_cases.json
├── narrative/
│   ├── {README.md,AGENTS.md}
│   ├── src/narrative_architect/knowledge/statements.py
│   └── tests/test_narrative_statements.py
├── {vriddhi,housewise,careersim}/
│   └── product boundary/readme files
├── tests/
│   ├── core/
│   ├── factory/
│   └── integration/
└── docs/
    ├── CONSAAS_CONSTITUTION.md
    ├── {FACTORY_MODE,FEATURE_CREATOR,FACTORY_EXECUTION_PROMPT}.md
    ├── {DEFINITION_OF_DONE,JUNIOR_DEVELOPER_GUIDE}.md
    ├── {QUALITY_GATES,ARCHITECTURE_GUARDRAILS,AI_EVALUATION}.md
    ├── {SECURITY,PRIVACY,SECRETS_MANAGEMENT,OBSERVABILITY,REPRODUCIBILITY}.md
    ├── {INITIAL_FACTORY_BACKLOG,REMAINING_GAPS}.md
    ├── demonstrations/
    └── existing Core and Narrative architecture/ADR documents
```

The tree intentionally omits generated caches, the local virtual environment, and individual pre-existing architecture documents already indexed by the root README.

# AI evaluations

Evaluations test probabilistic boundaries and their deterministic validation gates. They run offline, use versioned fixtures, and must never require a paid or remote model service.

`python evals/run_nka_statement_eval.py` exercises the first Narrative boundary: model-proposed statements cannot enter the canonical Narrative Knowledge Asset without valid epistemic status and provenance.

`python evals/run_dialogue_action_eval.py` exercises Decision Studio's provider-free dialogue
fallback across natural answers, uncertainty, confusion, explanation and deferral. Browser-model
outputs pass the same typed domain validator before any case update.

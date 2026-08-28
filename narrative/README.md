# Narrative Architect

Narrative Architect is the first greenfield product proving the ConSaaS factory. Its primary experience is a Virtual Screenplay Expert conversation backed by a canonical Narrative Knowledge Asset, local AI, deterministic creation/diagnostic engines, and source-level provenance.

The **Screenplay Builder 0.3** is a six-phase construction studio: centre knot, characters, full plot,
structure, engineered scenes, and final build/score. A versioned skill library supplies the screenplay
craft procedure; deterministic services own phase gates, revision history, structural coverage, iMaSc
construction arithmetic, and compilation. The author's approved Narrative Knowledge Asset remains
canonical.

Phase 5 now generates editable, story-grounded scene proposals from the approved beats, cast,
objectives, stakes, character behavior, locations/props and adjacent causal events. Its scorecard
reports **completion coverage** separately from **craft quality**. Generic instructions, placeholder
locations and archetypal cast names are detected and cannot receive a high craft score.

## Run locally

```powershell
python -m pip install -r narrative/requirements.txt
$env:NARRATIVE_PROFILE="local_private"
streamlit run narrative/streamlit_app.py
```

To enable optional local creative generation, install Ollama and a lightweight instruction model, then
set:

```powershell
$env:NARRATIVE_ENABLE_OLLAMA="1"
$env:NARRATIVE_OLLAMA_MODEL="qwen2.5:7b-instruct"
```

The adapter rejects non-loopback endpoints. If Ollama is unavailable, the same workflow remains usable
through deterministic skill blueprints and editable proposals.

The public hosted profile is a non-confidential demonstration with temporary session storage. It uses
no external LLM and accepts no screenplay PDF uploads. Download the project JSON before ending a
hosted session. The deterministic scorecard is a revision aid, not an IMDb score or a prediction of
commercial success. Generated scene proposals remain editable scaffolds until the author completes
a craft pass; the public demo does not claim that deterministic generation replaces bespoke writing.

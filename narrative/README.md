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

The current deterministic calibration is intentionally conservative:

- a fully populated scene can reach **5/5 completion** without receiving a high craft score;
- known boilerplate or structural placeholders cap craft at **2/5** and keep the Phase 5 gate open;
- story-grounded Architect scaffolds cap craft at the **3/5 revision-ready floor** until an author or
  approved local model performs the craft pass;
- a 5/5 craft score therefore requires story-specific evidence rather than field population alone.

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

## Release verification

Builder 0.3.0 is covered by Narrative domain, workflow, compiler, migration, privacy-boundary and
headless Streamlit tests, including regressions for story-grounded scene generation and populated
boilerplate receiving full completion but low craft. The release was also exercised through the live
hosted demonstration with completion, craft and structural coverage displayed independently.

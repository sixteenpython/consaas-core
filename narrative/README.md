# Narrative Architect

Narrative Architect is the first greenfield product proving the ConSaaS factory. Its primary experience is a Virtual Screenplay Expert conversation backed by a canonical Narrative Knowledge Asset, local AI, deterministic creation/diagnostic engines, and source-level provenance.

The **Foundation Alpha** implements the first complete Create-first slice: deterministic guided
conversation, a versioned canonical NKA, story/character/scene inspectors, immutable history and undo,
portable project bundles, and bounded Fountain compilation. Doctor mode and local-model intelligence
remain curated backlog increments.

## Run locally

```powershell
python -m pip install -r narrative/requirements.txt
$env:NARRATIVE_PROFILE="local_private"
streamlit run narrative/streamlit_app.py
```

The public hosted profile is a non-confidential demonstration with temporary session storage. It uses
no external LLM and accepts no screenplay PDF uploads. Download the project JSON before ending a
hosted session.

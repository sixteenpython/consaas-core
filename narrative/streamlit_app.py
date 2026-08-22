"""Streamlit Community Cloud entrypoint for Narrative Architect."""

from __future__ import annotations

import sys
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parent / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from narrative_architect.ui.app import main  # noqa: E402

main()

"""Content-addressed artifact helpers shared by ConSaaS products."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


def content_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


@dataclass(frozen=True, slots=True)
class ArtifactManifest:
    artifact_id: str
    product_id: str
    schema_version: str
    methodology_version: str
    effective_date: str
    knowledge_cutoff: str
    created_at: str
    content_sha256: str
    row_count: int
    source_ids: tuple[str, ...]
    quality_state: str
    reproducibility: str = "deterministic"

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["source_ids"] = list(self.source_ids)
        return value

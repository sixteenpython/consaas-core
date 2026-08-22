"""Generic candidate-build, validation and atomic-promotion refresh workflow."""

from __future__ import annotations

import csv
import json
import shutil
import uuid
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from core.artifacts import ArtifactManifest, atomic_write, canonical_json, content_hash


class RefreshError(ValueError):
    """A candidate failed before promotion."""


@dataclass(frozen=True, slots=True)
class RefreshOutcome:
    product_id: str
    effective_date: str
    release_dir: Path
    row_count: int
    content_sha256: str
    status: str


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RefreshError(f"{path} must contain a JSON object")
    return value


def _validate_rows(rows: list[dict[str, str]], schema: dict[str, Any]) -> list[dict[str, Any]]:
    required = tuple(schema.get("required_columns", []))
    numeric = tuple(schema.get("numeric_columns", []))
    identifiers: set[str] = set()
    issues: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=2):
        missing = [column for column in required if not row.get(column, "").strip()]
        if missing:
            issues.append({"severity": "error", "row": index, "message": f"missing {missing}"})
        identifier = row.get("record_id", "")
        if identifier in identifiers:
            issues.append({"severity": "error", "row": index, "message": "duplicate record_id"})
        identifiers.add(identifier)
        for column in numeric:
            try:
                float(row.get(column, ""))
            except ValueError:
                issues.append(
                    {"severity": "error", "row": index, "message": f"{column} is not numeric"}
                )
    if not rows:
        issues.append({"severity": "error", "row": 0, "message": "asset has no rows"})
    return issues


def refresh_product(root: Path, product_id: str, effective_date: date) -> RefreshOutcome:
    product_root = root / product_id
    source_path = product_root / "data" / "seed.csv"
    schema_path = product_root / "schemas" / "gka.schema.json"
    sources_path = product_root / "sources.json"
    if not all(path.exists() for path in (source_path, schema_path, sources_path)):
        raise RefreshError(f"{product_id} refresh inputs are incomplete")

    source_bytes = source_path.read_bytes()
    with source_path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    schema = _read_json(schema_path)
    sources = _read_json(sources_path)
    issues = _validate_rows(rows, schema)
    errors = [issue for issue in issues if issue["severity"] == "error"]
    if errors:
        raise RefreshError(f"{product_id} candidate failed validation: {errors}")

    effective = effective_date.isoformat()
    artifact_hash = content_hash(source_bytes)
    artifact_id = f"{product_id}-gka-{effective}-{artifact_hash[:12]}"
    created = datetime.now(UTC).isoformat()
    manifest = ArtifactManifest(
        artifact_id=artifact_id,
        product_id=product_id,
        schema_version=str(schema["schema_version"]),
        methodology_version=str(schema["methodology_version"]),
        effective_date=effective,
        knowledge_cutoff=effective,
        created_at=created,
        content_sha256=artifact_hash,
        row_count=len(rows),
        source_ids=tuple(item["source_id"] for item in sources.get("sources", [])),
        quality_state="passed",
    )
    quality = {
        "state": "passed",
        "checked_at": created,
        "checks": [
            {"name": "required_fields", "status": "passed"},
            {"name": "unique_record_id", "status": "passed"},
            {"name": "numeric_types", "status": "passed"},
            {"name": "non_empty", "status": "passed", "observed": len(rows)},
        ],
        "issues": issues,
        "source_dispositions": [
            {
                "source_id": item["source_id"],
                "mode": item["mode"],
                "status": "ingested" if item["mode"] == "curated_snapshot" else "reference_only",
            }
            for item in sources.get("sources", [])
        ],
    }

    releases_root = root / "knowledge" / "releases" / product_id
    release_dir = releases_root / effective
    candidate = releases_root / ".candidates" / f"{effective}-{uuid.uuid4().hex}"
    candidate.mkdir(parents=True, exist_ok=False)
    try:
        (candidate / "grand_knowledge_asset.csv").write_bytes(source_bytes)
        (candidate / "manifest.json").write_bytes(canonical_json(manifest.to_dict()))
        (candidate / "quality.json").write_bytes(canonical_json(quality))
        if release_dir.exists():
            existing = _read_json(release_dir / "manifest.json")
            if existing.get("content_sha256") != artifact_hash:
                raise RefreshError(
                    f"{product_id} {effective} already exists with different content; "
                    "use a new date"
                )
            shutil.rmtree(candidate)
            status = "unchanged"
        else:
            release_dir.parent.mkdir(parents=True, exist_ok=True)
            candidate.replace(release_dir)
            status = "promoted"
        pointer = {
            "product_id": product_id,
            "effective_date": effective,
            "artifact_id": artifact_id,
            "content_sha256": artifact_hash,
            "release_path": str(release_dir.relative_to(root)).replace("\\", "/"),
        }
        atomic_write(releases_root / "current.json", canonical_json(pointer))
    except Exception:
        shutil.rmtree(candidate, ignore_errors=True)
        raise
    return RefreshOutcome(product_id, effective, release_dir, len(rows), artifact_hash, status)


def refresh_all(root: Path, effective_date: date) -> tuple[RefreshOutcome, ...]:
    return tuple(
        refresh_product(root, product_id, effective_date)
        for product_id in ("careersim", "housewise", "startup")
    )

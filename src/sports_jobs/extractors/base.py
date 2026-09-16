from __future__ import annotations

from pathlib import Path
from typing import Any

from sports_jobs.models import JobRecord


def extract_source(config: dict[str, Any], project_root: Path | None = None) -> list[JobRecord]:
    source_type = config.get("type")
    if source_type == "fixture":
        from sports_jobs.extractors.fixture import extract_fixture

        return extract_fixture(config, project_root=project_root)
    if source_type == "greenhouse":
        from sports_jobs.extractors.greenhouse import extract_greenhouse

        return extract_greenhouse(config)
    if source_type == "lever":
        from sports_jobs.extractors.lever import extract_lever

        return extract_lever(config)
    raise ValueError(f"Unsupported source type: {source_type!r}")


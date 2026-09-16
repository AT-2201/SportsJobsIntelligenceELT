from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sports_jobs.models import JobRecord, clean_text, parse_timestamp


def extract_fixture(
    config: dict[str, Any], project_root: Path | None = None
) -> list[JobRecord]:
    path = Path(config["path"])
    if not path.is_absolute() and project_root:
        path = project_root / path
    with path.open(encoding="utf-8") as handle:
        payloads = json.load(handle)
    return [_normalize(config["name"], payload) for payload in payloads]


def _normalize(source: str, payload: dict[str, Any]) -> JobRecord:
    return JobRecord(
        source=source,
        source_job_id=str(payload["id"]),
        title=clean_text(payload["title"]) or "Unknown role",
        company_name=clean_text(payload["company"]) or "Unknown company",
        location_text=clean_text(payload.get("location")),
        description=clean_text(payload.get("description")),
        employment_type=clean_text(payload.get("employment_type")),
        workplace_type=clean_text(payload.get("workplace_type")),
        salary_min=payload.get("salary_min"),
        salary_max=payload.get("salary_max"),
        salary_currency=payload.get("salary_currency", "USD"),
        salary_period=payload.get("salary_period", "year"),
        posted_at=parse_timestamp(payload.get("posted_at")),
        source_updated_at=parse_timestamp(payload.get("updated_at")),
        job_url=payload.get("url"),
        raw_payload=payload,
    )


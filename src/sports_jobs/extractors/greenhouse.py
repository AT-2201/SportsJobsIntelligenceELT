from __future__ import annotations

from html import unescape
from typing import Any

from sports_jobs.extractors.http import get_json
from sports_jobs.models import JobRecord, clean_text, parse_timestamp


def extract_greenhouse(config: dict[str, Any]) -> list[JobRecord]:
    board = config["board_token"]
    response = get_json(
        f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs",
        params={"content": "true"},
    )
    return [_normalize(config["name"], job) for job in response.get("jobs", [])]


def _normalize(source: str, payload: dict[str, Any]) -> JobRecord:
    location = (payload.get("location") or {}).get("name")
    description = clean_text(unescape(payload.get("content") or ""))
    return JobRecord(
        source=source,
        source_job_id=str(payload["id"]),
        title=clean_text(payload.get("title")) or "Unknown role",
        company_name=source.replace("_", " ").title(),
        location_text=clean_text(location),
        description=description,
        posted_at=parse_timestamp(payload.get("first_published")),
        source_updated_at=parse_timestamp(payload.get("updated_at")),
        job_url=payload.get("absolute_url"),
        raw_payload=payload,
    )


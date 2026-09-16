from __future__ import annotations

from typing import Any

from sports_jobs.extractors.http import get_json
from sports_jobs.models import JobRecord, clean_text, parse_timestamp


def extract_lever(config: dict[str, Any]) -> list[JobRecord]:
    site = config["site"]
    payloads = get_json(f"https://api.lever.co/v0/postings/{site}", params={"mode": "json"})
    return [_normalize(config["name"], job) for job in payloads]


def _normalize(source: str, payload: dict[str, Any]) -> JobRecord:
    categories = payload.get("categories") or {}
    description_parts = [
        payload.get("descriptionPlain"),
        *(item.get("content") for item in payload.get("lists", [])),
        payload.get("additionalPlain"),
    ]
    return JobRecord(
        source=source,
        source_job_id=str(payload["id"]),
        title=clean_text(payload.get("text")) or "Unknown role",
        company_name=source.replace("_", " ").title(),
        location_text=clean_text(categories.get("location")),
        description=clean_text(" ".join(filter(None, description_parts))),
        employment_type=clean_text(categories.get("commitment")),
        workplace_type=clean_text(payload.get("workplaceType")),
        posted_at=parse_timestamp(payload.get("createdAt")),
        source_updated_at=parse_timestamp(payload.get("updatedAt") or payload.get("createdAt")),
        job_url=payload.get("hostedUrl"),
        raw_payload=payload,
    )

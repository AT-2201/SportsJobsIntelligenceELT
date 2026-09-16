from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class JobRecord:
    source: str
    source_job_id: str
    title: str
    company_name: str
    location_text: str | None = None
    description: str | None = None
    employment_type: str | None = None
    workplace_type: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: str | None = "USD"
    salary_period: str | None = "year"
    posted_at: datetime | None = None
    source_updated_at: datetime | None = None
    job_url: str | None = None
    raw_payload: dict[str, Any] = field(default_factory=dict)

    @property
    def content_hash(self) -> str:
        material = asdict(self)
        material.pop("raw_payload", None)
        encoded = json.dumps(material, sort_keys=True, default=str, separators=(",", ":"))
        return hashlib.sha256(encoded.encode()).hexdigest()


def parse_timestamp(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, int | float):
        # Greenhouse uses milliseconds while many APIs use seconds.
        seconds = value / 1000 if value > 10_000_000_000 else value
        parsed = datetime.fromtimestamp(seconds, tz=UTC)
    else:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    return parsed.replace(tzinfo=parsed.tzinfo or UTC).astimezone(UTC)


def clean_text(value: Any) -> str | None:
    if value is None:
        return None
    result = " ".join(str(value).split()).strip()
    return result or None

import json
from pathlib import Path

from sports_jobs.extractors.fixture import extract_fixture


def test_fixture_extractor_normalizes_record(tmp_path: Path) -> None:
    path = tmp_path / "jobs.json"
    path.write_text(
        json.dumps(
            [
                {
                    "id": 42,
                    "title": "  Analyst ",
                    "company": " Club ",
                    "posted_at": "2026-09-15T00:00:00Z",
                }
            ]
        ),
        encoding="utf-8",
    )
    records = extract_fixture({"name": "unit", "path": str(path)})
    assert len(records) == 1
    assert records[0].source_job_id == "42"
    assert records[0].title == "Analyst"
    assert records[0].company_name == "Club"


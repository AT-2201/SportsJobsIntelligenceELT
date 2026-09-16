from datetime import UTC

from sports_jobs.models import JobRecord, clean_text, parse_timestamp


def test_content_hash_is_stable_and_ignores_raw_payload() -> None:
    base = JobRecord(
        source="demo",
        source_job_id="1",
        title="Data Analyst",
        company_name="Team",
        raw_payload={"first": 1},
    )
    changed_raw = JobRecord(
        source="demo",
        source_job_id="1",
        title="Data Analyst",
        company_name="Team",
        raw_payload={"unmodeled_new_field": True},
    )
    changed_title = JobRecord(
        source="demo",
        source_job_id="1",
        title="Senior Data Analyst",
        company_name="Team",
    )
    assert base.content_hash == changed_raw.content_hash
    assert base.content_hash != changed_title.content_hash


def test_parse_timestamp_supports_iso_and_epoch_milliseconds() -> None:
    iso = parse_timestamp("2026-09-15T12:30:00Z")
    epoch = parse_timestamp(iso.timestamp() * 1000)
    assert iso == epoch
    assert iso.tzinfo == UTC


def test_clean_text_normalizes_whitespace() -> None:
    assert clean_text("  Data\n  Analyst  ") == "Data Analyst"
    assert clean_text("   ") is None


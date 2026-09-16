from __future__ import annotations

import json
import logging
import uuid
from collections.abc import Iterable
from datetime import UTC, datetime

import psycopg

from sports_jobs.models import JobRecord

LOGGER = logging.getLogger(__name__)

DDL = """
create schema if not exists raw;
create schema if not exists monitoring;

create table if not exists raw.job_posting_events (
    event_id bigserial primary key,
    source text not null,
    source_job_id text not null,
    title text not null,
    company_name text not null,
    location_text text,
    description text,
    employment_type text,
    workplace_type text,
    salary_min numeric,
    salary_max numeric,
    salary_currency text,
    salary_period text,
    posted_at timestamptz,
    source_updated_at timestamptz,
    job_url text,
    content_hash char(64) not null,
    raw_payload jsonb not null,
    ingested_at timestamptz not null default now(),
    run_id uuid not null,
    unique (source, source_job_id, content_hash)
);

create index if not exists ix_job_events_natural_key
    on raw.job_posting_events (source, source_job_id, ingested_at desc);

create table if not exists monitoring.pipeline_runs (
    run_id uuid primary key,
    started_at timestamptz not null,
    finished_at timestamptz,
    status text not null check (status in ('running', 'success', 'failed')),
    sources_attempted integer not null default 0,
    rows_extracted integer not null default 0,
    rows_inserted integer not null default 0,
    error_message text
);
"""

INSERT_JOB = """
insert into raw.job_posting_events (
    source, source_job_id, title, company_name, location_text, description,
    employment_type, workplace_type, salary_min, salary_max, salary_currency,
    salary_period, posted_at, source_updated_at, job_url, content_hash,
    raw_payload, run_id
) values (
    %(source)s, %(source_job_id)s, %(title)s, %(company_name)s, %(location_text)s,
    %(description)s, %(employment_type)s, %(workplace_type)s, %(salary_min)s,
    %(salary_max)s, %(salary_currency)s, %(salary_period)s, %(posted_at)s,
    %(source_updated_at)s, %(job_url)s, %(content_hash)s, %(raw_payload)s::jsonb,
    %(run_id)s
)
on conflict (source, source_job_id, content_hash) do nothing
returning event_id;
"""


class Warehouse:
    def __init__(self, dsn: str):
        self.dsn = dsn

    def initialize(self) -> None:
        with psycopg.connect(self.dsn) as connection:
            connection.execute(DDL)

    def start_run(self, sources_attempted: int) -> uuid.UUID:
        run_id = uuid.uuid4()
        with psycopg.connect(self.dsn) as connection:
            connection.execute(
                """insert into monitoring.pipeline_runs
                   (run_id, started_at, status, sources_attempted)
                   values (%s, %s, 'running', %s)""",
                (run_id, datetime.now(UTC), sources_attempted),
            )
        return run_id

    def load(self, records: Iterable[JobRecord], run_id: uuid.UUID) -> tuple[int, int]:
        extracted = inserted = 0
        with psycopg.connect(self.dsn) as connection:
            with connection.cursor() as cursor:
                for record in records:
                    extracted += 1
                    values = vars(record) | {
                        "content_hash": record.content_hash,
                        "raw_payload": json.dumps(record.raw_payload, default=str),
                        "run_id": run_id,
                    }
                    cursor.execute(INSERT_JOB, values)
                    inserted += int(cursor.fetchone() is not None)
        return extracted, inserted

    def finish_run(
        self,
        run_id: uuid.UUID,
        status: str,
        rows_extracted: int,
        rows_inserted: int,
        error_message: str | None = None,
    ) -> None:
        with psycopg.connect(self.dsn) as connection:
            connection.execute(
                """update monitoring.pipeline_runs
                   set finished_at = %s, status = %s, rows_extracted = %s,
                       rows_inserted = %s, error_message = %s
                   where run_id = %s""",
                (
                    datetime.now(UTC),
                    status,
                    rows_extracted,
                    rows_inserted,
                    error_message,
                    run_id,
                ),
            )

    def quality_summary(self) -> dict[str, int | str | None]:
        query = """
        select
            count(*) as total_events,
            count(distinct (source, source_job_id)) as distinct_jobs,
            count(*) filter (where title is null or trim(title) = '') as missing_titles,
            count(*) filter (where company_name is null or trim(company_name) = '')
                as missing_companies,
            max(ingested_at)::text as freshest_ingestion
        from raw.job_posting_events
        """
        with psycopg.connect(self.dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                row = cursor.fetchone()
        assert row is not None
        columns = [
            "total_events",
            "distinct_jobs",
            "missing_titles",
            "missing_companies",
            "freshest_ingestion",
        ]
        return dict(zip(columns, row, strict=True))

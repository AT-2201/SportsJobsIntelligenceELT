# Sports Jobs Intelligence ELT Pipeline

An end-to-end, production-style data project that collects sports-industry job postings,
preserves their history, models hiring activity, tests data quality, and exposes
BI-ready marts. It runs locally with included sample data and can ingest public
Greenhouse and Lever job-board APIs.

## What it demonstrates

- Resilient Python extraction with retries and source adapters
- Append-only raw history plus idempotent incremental loading
- PostgreSQL warehouse schemas and run monitoring
- dbt staging, enrichment, star schema, skill bridge, marts, and tests
- Prefect orchestration, Docker reproducibility, and GitHub Actions CI
- A no-credential demo path and configurable live-source path

## Architecture

```text
Public APIs / fixture
         ↓
Python extractors ───────→ monitoring.pipeline_runs
         ↓
raw.job_posting_events (immutable versions + original JSON)
         ↓
dbt: staging → enrichment → dimensions/fact/skill bridge
         ↓
Hiring overview / skill demand / company activity marts
         ↓
Metabase, Power BI, or Tableau
```

The warehouse model and design rationale are detailed in
[`docs/architecture.md`](docs/architecture.md).

## Five-minute local run

Requirements: Python 3.11+ and Docker Desktop.

```bash
cp .env.example .env
docker compose up -d postgres
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -e .
python -m sports_jobs.cli pipeline
python -m sports_jobs.cli quality
```

The first run ingests six fixture jobs and builds all dbt models. A second run reports
six extracted and zero inserted rows, proving idempotency.

To execute the same flow entirely in containers:

```bash
docker compose --profile pipeline run --build --rm pipeline
```

## Query the results

```sql
select * from analytics_marts.mart_skill_demand;
select * from analytics_marts.mart_company_activity;
select * from analytics_core.fct_job_postings;
select * from monitoring.pipeline_runs order by started_at desc;
```

dbt prefixes the configured schemas with its target schema (`analytics`), producing
`analytics_staging`, `analytics_intermediate`, `analytics_core`, and `analytics_marts`.

## Use live sources

The included source configuration contains verified public boards for Hudl (Greenhouse)
and Veo (Lever). Fixture mode remains the default and makes no external requests. Run
the complete pipeline against the public boards with:

```bash
INGESTION_MODE=live sports-jobs pipeline
```

To add other organizations, edit `config/sources.yml` with their public board identifiers:

```yaml
sources:
  - name: a_sports_company
    type: greenhouse
    board_token: its-greenhouse-board-token
    enabled: true
  - name: another_sports_company
    type: lever
    site: its-lever-site-token
    enabled: true
```

Company career pages can move or change terms, so only enable boards you have verified
and whose access rules permit automated retrieval. Raw responses are retained for audit,
while general talent-community and resume-registration pages are excluded from curated
job analytics.

## Operate and test

```bash
pytest -q
ruff check src tests orchestration
dbt build --project-dir dbt --profiles-dir dbt
dbt source freshness --project-dir dbt --profiles-dir dbt
python orchestration/prefect_flow.py
```

The Prefect flow can be served or deployed on any schedule supported by Prefect. A
daily 6:00 AM deployment is a sensible production default. The included CI workflow
runs lint, unit tests, a real PostgreSQL ingestion, every dbt model, and every data test.

## Data quality controls

- Required and unique job identifiers
- Relationships from fact to company/location and from bridge to jobs/skills
- Accepted workplace types
- Nonnegative, ordered salary bounds
- Post dates cannot be more than one day in the future
- Source freshness thresholds
- API timeouts, retries, structured run status, and row counts

## Analytics outputs

- Hiring trends by month, role family, seniority, sport, and workplace type
- Skill demand and percentage of postings requesting each skill
- Employer activity, early-career openings, and technical-data openings
- Current posting detail for an opportunity explorer

See [`docs/dashboard.md`](docs/dashboard.md) for a four-page dashboard blueprint.

## Repository map

```text
src/sports_jobs/       ingestion, source adapters, loader, CLI
dbt/models/            staging, intermediate, core, and marts
orchestration/         Prefect flow
data/fixtures/         deterministic offline demo data
tests/                 unit tests
docs/                  architecture and dashboard guidance
.github/workflows/     end-to-end CI
```

## Security

Credentials come from environment variables. `.env` and local data outputs are ignored
by Git. Do not commit API keys or production database passwords.

## Resume-ready summary

> Built an automated sports-jobs ELT pipeline using Python, PostgreSQL, dbt, Prefect,
> and Docker, implementing append-only raw history, idempotent incremental loads,
> dimensional modeling, skill extraction, data-quality tests, monitoring, and BI-ready
> hiring-trend marts with end-to-end CI.

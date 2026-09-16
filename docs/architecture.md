# Architecture and design decisions

```text
Greenhouse / Lever / fixture JSON
                |
      Python source adapters
      (retry + normalization)
                |
      PostgreSQL raw schema
 (append-only JSON + typed fields)
                |
             dbt DAG
     staging -> intermediate
                |
  dimensions <-> fact <-> bridge
                |
       analytics data marts
                |
       Metabase / Power BI

Prefect schedules the flow; monitoring.pipeline_runs records operational outcomes;
dbt tests and CI guard data and code quality.
```

## Data grain

- `raw.job_posting_events`: one row per observed content version of a source posting.
- `fct_job_postings`: one row per latest-known source posting.
- `bridge_job_skills`: one row per job/skill pairing.
- `dim_company`, `dim_location`, `dim_skill`: one row per normalized entity.

## Idempotency and history

The loader's uniqueness key is `(source, source_job_id, content_hash)`. Re-running the
same payload creates no duplicate. A meaningful change creates a new immutable event,
while dbt selects the newest version for current-state reporting. This preserves source
history and makes transformations rebuildable.

## Production extension path

The local PostgreSQL boundary can be replaced by BigQuery and GCS without changing the
source contract or analytical model. For higher volume, land original responses in
object storage, partition raw tables by ingestion date, make facts incremental, and add
source-specific watermarks.


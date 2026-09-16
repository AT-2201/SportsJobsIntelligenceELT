select
    job_id,
    company_key,
    location_key,
    source,
    source_job_id,
    job_title,
    role_family,
    seniority,
    sport_segment,
    employment_type,
    workplace_type,
    is_remote,
    salary_min,
    salary_max,
    salary_currency,
    salary_period,
    posted_at,
    source_updated_at,
    extract(day from age_interval)::integer as days_open,
    job_url,
    ingested_at
from {{ ref('int_jobs_enriched') }}


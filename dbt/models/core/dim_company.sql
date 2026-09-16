select
    company_key,
    company_name,
    count(*) as current_openings,
    min(posted_at) as earliest_current_posting,
    max(posted_at) as latest_current_posting
from {{ ref('int_jobs_enriched') }}
group by 1, 2


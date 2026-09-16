select
    location_key,
    coalesce(location_text, 'Unknown') as location_name,
    bool_or(is_remote) as includes_remote_role
from {{ ref('int_jobs_enriched') }}
group by 1, 2


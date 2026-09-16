select *
from {{ ref('fct_job_postings') }}
where posted_at > current_timestamp + interval '1 day'

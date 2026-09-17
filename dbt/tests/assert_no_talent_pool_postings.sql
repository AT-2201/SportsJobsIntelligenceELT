select *
from {{ ref('stg_job_postings') }}
where lower(job_title) ~ '(talent community|candidate data base|register your cv)'

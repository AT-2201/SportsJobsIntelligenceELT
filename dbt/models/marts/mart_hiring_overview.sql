select
    date_trunc('month', posted_at)::date as posting_month,
    role_family,
    seniority,
    sport_segment,
    workplace_type,
    count(*) as job_count,
    count(*) filter (where is_remote) as remote_job_count,
    round(avg(salary_min) filter (where salary_period = 'year'), 2) as avg_min_salary,
    round(avg(salary_max) filter (where salary_period = 'year'), 2) as avg_max_salary
from {{ ref('fct_job_postings') }}
group by 1, 2, 3, 4, 5


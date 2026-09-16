select
    skills.skill_name,
    count(distinct bridge.job_id) as job_count,
    round(
        100.0 * count(distinct bridge.job_id)
        / nullif((select count(*) from {{ ref('fct_job_postings') }}), 0),
        1
    ) as pct_of_jobs
from {{ ref('bridge_job_skills') }} bridge
join {{ ref('dim_skill') }} skills using (skill_key)
group by 1
order by job_count desc, skill_name


select
    company.company_name,
    count(*) as current_openings,
    count(*) filter (where jobs.seniority in ('Intern', 'Entry')) as early_career_openings,
    count(*) filter (where jobs.role_family in ('Analytics', 'Business Intelligence'))
        as analytics_openings,
    count(*) filter (where jobs.role_family in ('Data Engineering', 'Data Science / ML'))
        as technical_data_openings,
    max(jobs.posted_at) as latest_posting_at
from {{ ref('fct_job_postings') }} jobs
join {{ ref('dim_company') }} company using (company_key)
group by 1
order by current_openings desc, company_name


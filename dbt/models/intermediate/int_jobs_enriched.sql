select
    *,
    md5(lower(company_name)) as company_key,
    md5(lower(coalesce(location_text, 'unknown'))) as location_key,
    case
        when lower(job_title) ~ '(intern|internship)' then 'Internship'
        when lower(job_title) ~ '(data engineer|analytics engineer)' then 'Data Engineering'
        when lower(job_title) ~ '(machine learning|ml engineer|data scientist)' then 'Data Science / ML'
        when lower(job_title) ~ '(business intelligence|bi analyst)' then 'Business Intelligence'
        when lower(job_title) ~ '(analyst|analytics)' then 'Analytics'
        else 'Other'
    end as role_family,
    case
        when lower(job_title) ~ '(intern|internship)' then 'Intern'
        when lower(job_title) ~ '(junior|entry|associate|coordinator)' then 'Entry'
        when lower(job_title) ~ '(senior|sr\.|lead|principal|staff|manager|director|head|vp)' then 'Senior'
        else 'Mid / Unspecified'
    end as seniority,
    case
        when lower(coalesce(location_text, '')) like '%remote%'
          or lower(workplace_type) = 'remote' then true
        else false
    end as is_remote,
    case
        when lower(job_title || ' ' || coalesce(description, '')) ~ '(basketball|nba|wnba)' then 'Basketball'
        when lower(job_title || ' ' || coalesce(description, '')) ~ '(soccer|football|mls)' then 'Soccer'
        when lower(job_title || ' ' || coalesce(description, '')) ~ '(baseball|mlb)' then 'Baseball'
        when lower(job_title || ' ' || coalesce(description, '')) ~ '(hockey|nhl)' then 'Hockey'
        else 'Multi-sport / Other'
    end as sport_segment,
    current_timestamp - posted_at as age_interval
from {{ ref('stg_job_postings') }}


select
    *,
    md5(lower(company_name)) as company_key,
    md5(lower(coalesce(location_text, 'unknown'))) as location_key,
    case
        when lower(job_title) ~ '(data engineer|analytics engineer|mlops)' then 'Data Engineering'
        when lower(job_title) ~ '(machine learning|ml engineer|data scientist)' then 'Data Science / ML'
        when lower(job_title) ~ '(business intelligence|bi analyst)' then 'Business Intelligence'
        when lower(job_title) ~ '(analyst|analytics|insights)' then 'Analytics'
        when lower(job_title) ~ '(hardware|mechanical|embedded|firmware|camera|optics)'
            then 'Hardware / Embedded'
        when lower(job_title) ~ '(security|corporate it|global it|systems analyst|network)'
            then 'IT / Security'
        when lower(job_title) ~ '(product manager|product management|product design)'
            then 'Product'
        when lower(job_title) ~ '(software|engineer|engineering|android|quality assurance)'
            then 'Software Engineering'
        when lower(job_title) ~ '(account executive|account manager|business development|sales|partnerships|market director)'
            then 'Sales / Business Development'
        when lower(job_title) ~ '(customer success|consultant|customer support)'
            then 'Customer Success / Consulting'
        when lower(job_title) ~ '(operations|procurement|vendor)' then 'Operations / Supply Chain'
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

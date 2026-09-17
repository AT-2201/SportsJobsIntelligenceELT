with ranked as (
    select
        *,
        row_number() over (
            partition by source, source_job_id
            order by coalesce(source_updated_at, posted_at, ingested_at) desc, ingested_at desc
        ) as recency_rank
    from {{ source('raw', 'job_posting_events') }}
),

cleaned as (
    select
        source || ':' || source_job_id as job_id,
        source,
        source_job_id,
        trim(title) as job_title,
        trim(company_name) as company_name,
        nullif(trim(location_text), '') as location_text,
        nullif(trim(description), '') as description,
        coalesce(nullif(trim(employment_type), ''), 'Unknown') as employment_type,
        case
            when lower(trim(workplace_type)) = 'remote' then 'Remote'
            when lower(trim(workplace_type)) = 'hybrid' then 'Hybrid'
            when regexp_replace(lower(trim(workplace_type)), '[^a-z]', '', 'g') = 'onsite'
                then 'On-site'
            when lower(coalesce(location_text, '')) like '%remote%' then 'Remote'
            else 'Unknown'
        end as workplace_type,
        salary_min,
        salary_max,
        coalesce(salary_currency, 'USD') as salary_currency,
        coalesce(salary_period, 'year') as salary_period,
        posted_at,
        source_updated_at,
        job_url,
        content_hash,
        ingested_at
    from ranked
    where recency_rank = 1
      and lower(trim(title)) !~ '(talent community|candidate data base|register your cv)'
)

select * from cleaned

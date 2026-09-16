with skills(skill_name, pattern) as (
    values
        ('SQL', '\msql\M'),
        ('Python', '\mpython\M'),
        ('R', '\mR\M'),
        ('Excel', '\mexcel\M'),
        ('Tableau', '\mtableau\M'),
        ('Power BI', '\mpower bi\M'),
        ('dbt', '\mdbt\M'),
        ('Airflow', '\mairflow\M'),
        ('AWS', '\maws\M'),
        ('GCP', '\mgcp\M|google cloud'),
        ('Snowflake', '\msnowflake\M'),
        ('Kafka', '\mkafka\M'),
        ('Docker', '\mdocker\M'),
        ('Kubernetes', '\mkubernetes\M'),
        ('PyTorch', '\mpytorch\M'),
        ('Computer Vision', 'computer vision'),
        ('Salesforce', '\msalesforce\M')
)

select
    jobs.job_id,
    skills.skill_name,
    md5(lower(skills.skill_name)) as skill_key
from {{ ref('stg_job_postings') }} jobs
cross join skills
where coalesce(jobs.job_title, '') || ' ' || coalesce(jobs.description, '') ~* skills.pattern


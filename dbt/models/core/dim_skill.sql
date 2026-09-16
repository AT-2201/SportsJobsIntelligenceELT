select distinct skill_key, skill_name
from {{ ref('int_job_skills') }}


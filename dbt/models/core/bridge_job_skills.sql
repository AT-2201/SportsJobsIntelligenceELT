select job_id, skill_key
from {{ ref('int_job_skills') }}


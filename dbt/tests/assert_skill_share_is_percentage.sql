select *
from {{ ref('mart_skill_demand') }}
where pct_of_jobs < 0 or pct_of_jobs > 100

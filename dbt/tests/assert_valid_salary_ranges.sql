select *
from {{ ref('fct_job_postings') }}
where salary_min < 0
   or salary_max < 0
   or (salary_min is not null and salary_max is not null and salary_min > salary_max)


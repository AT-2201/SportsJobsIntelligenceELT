# Dashboard blueprint

Connect Power BI, Tableau, or Metabase to the `analytics_marts` schema and build these
pages:

1. **Hiring overview** — open roles, early-career share, remote share, median salary,
   role family and sports segment filters.
2. **Skill demand** — top requested skills, percent of postings, skill combinations.
3. **Employer activity** — current openings by employer, latest post date, technical
   data roles versus analytics roles.
4. **Opportunity explorer** — searchable job table linked to the application URL.

Recommended model usage:

- `mart_hiring_overview` for trend and segmentation visuals.
- `mart_skill_demand` for skill bars and KPI cards.
- `mart_company_activity` for employer rankings.
- `fct_job_postings` joined to dimensions for the detailed explorer.


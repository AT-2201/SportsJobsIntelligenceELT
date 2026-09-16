FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir .
COPY config ./config
COPY data ./data
COPY dbt ./dbt
COPY orchestration ./orchestration

ENV PYTHONUNBUFFERED=1 DBT_PROFILES_DIR=/app/dbt
CMD ["python", "-m", "sports_jobs.cli", "pipeline"]


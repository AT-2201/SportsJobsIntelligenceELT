.PHONY: setup up down ingest transform test pipeline quality lint clean

setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements-dev.txt
	.venv/bin/pip install --no-build-isolation -e .

up:
	docker compose up -d postgres

down:
	docker compose down

ingest:
	python -m sports_jobs.cli ingest

transform:
	dbt build --project-dir dbt --profiles-dir dbt

test:
	pytest -q

pipeline:
	python -m sports_jobs.cli pipeline

quality:
	python -m sports_jobs.cli quality

lint:
	ruff check src tests orchestration

clean:
	dbt clean --project-dir dbt --profiles-dir dbt

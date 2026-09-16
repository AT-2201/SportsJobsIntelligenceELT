from __future__ import annotations

import logging
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any

from sports_jobs.config import Settings
from sports_jobs.extractors import extract_source
from sports_jobs.warehouse import Warehouse

LOGGER = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def ingest(settings: Settings | None = None, *, finalize_run: bool = True) -> dict[str, Any]:
    settings = settings or Settings.from_env()
    sources = settings.sources()
    if not sources:
        raise ValueError(f"No enabled sources for ingestion mode {settings.ingestion_mode!r}")

    warehouse = Warehouse(settings.dsn)
    warehouse.initialize()
    run_id = warehouse.start_run(len(sources))
    extracted_total = inserted_total = 0
    try:
        for source in sources:
            LOGGER.info("Extracting source=%s type=%s", source["name"], source["type"])
            records = extract_source(source, project_root=PROJECT_ROOT)
            extracted, inserted = warehouse.load(records, run_id)
            extracted_total += extracted
            inserted_total += inserted
            LOGGER.info(
                "Loaded source=%s extracted=%d inserted=%d",
                source["name"],
                extracted,
                inserted,
            )
        if finalize_run:
            warehouse.finish_run(run_id, "success", extracted_total, inserted_total)
    except Exception as exc:
        warehouse.finish_run(
            run_id, "failed", extracted_total, inserted_total, error_message=str(exc)[:2000]
        )
        raise
    return {
        "run_id": str(run_id),
        "sources": len(sources),
        "rows_extracted": extracted_total,
        "rows_inserted": inserted_total,
    }


def transform() -> None:
    adjacent_dbt = Path(sys.executable).with_name("dbt")
    dbt_executable = str(adjacent_dbt) if adjacent_dbt.exists() else shutil.which("dbt")
    if not dbt_executable:
        raise FileNotFoundError("dbt executable not found; install the project dependencies first")
    subprocess.run(
        [
            dbt_executable,
            "build",
            "--project-dir",
            str(PROJECT_ROOT / "dbt"),
            "--profiles-dir",
            str(PROJECT_ROOT / "dbt"),
        ],
        check=True,
    )


def run_pipeline(settings: Settings | None = None) -> dict[str, Any]:
    settings = settings or Settings.from_env()
    result = ingest(settings, finalize_run=False)
    warehouse = Warehouse(settings.dsn)
    run_id = uuid.UUID(result["run_id"])
    try:
        transform()
    except Exception as exc:
        warehouse.finish_run(
            run_id,
            "failed",
            result["rows_extracted"],
            result["rows_inserted"],
            error_message=str(exc)[:2000],
        )
        raise
    warehouse.finish_run(
        run_id,
        "success",
        result["rows_extracted"],
        result["rows_inserted"],
    )
    return result

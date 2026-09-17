from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "sports_jobs"
    postgres_user: str = "sports"
    postgres_password: str = "sports"
    sources_file: Path = Path("config/sources.yml")
    ingestion_mode: str = "fixture"

    @classmethod
    def from_env(cls) -> Settings:
        load_dotenv()
        return cls(
            postgres_host=os.getenv("POSTGRES_HOST", "localhost"),
            postgres_port=int(os.getenv("POSTGRES_PORT", "5432")),
            postgres_db=os.getenv("POSTGRES_DB", "sports_jobs"),
            postgres_user=os.getenv("POSTGRES_USER", "sports"),
            postgres_password=os.getenv("POSTGRES_PASSWORD", "sports"),
            sources_file=Path(os.getenv("JOB_SOURCES_FILE", "config/sources.yml")),
            ingestion_mode=os.getenv("INGESTION_MODE", "fixture").lower(),
        )

    @property
    def dsn(self) -> str:
        return (
            f"host={self.postgres_host} port={self.postgres_port} dbname={self.postgres_db} "
            f"user={self.postgres_user} password={self.postgres_password}"
        )

    def sources(self) -> list[dict[str, Any]]:
        with self.sources_file.open(encoding="utf-8") as handle:
            values = yaml.safe_load(handle) or {}
        sources = [source for source in values.get("sources", []) if source.get("enabled", True)]
        if self.ingestion_mode == "fixture":
            return [source for source in sources if source.get("type") == "fixture"]
        if self.ingestion_mode == "live":
            return [
                source
                for source in sources
                if source.get("type") in {"greenhouse", "lever"}
            ]
        raise ValueError(f"Unsupported INGESTION_MODE: {self.ingestion_mode}")

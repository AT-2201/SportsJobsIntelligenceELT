from __future__ import annotations

import argparse
import json
import logging

from sports_jobs.config import Settings
from sports_jobs.pipeline import ingest, run_pipeline, transform
from sports_jobs.warehouse import Warehouse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sports Jobs Intelligence ELT")
    parser.add_argument("command", choices=("ingest", "transform", "pipeline", "quality"))
    return parser


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    args = build_parser().parse_args()
    settings = Settings.from_env()
    if args.command == "ingest":
        print(json.dumps(ingest(settings), indent=2))
    elif args.command == "transform":
        transform()
    elif args.command == "pipeline":
        print(json.dumps(run_pipeline(settings), indent=2))
    else:
        print(json.dumps(Warehouse(settings.dsn).quality_summary(), indent=2, default=str))


if __name__ == "__main__":
    main()


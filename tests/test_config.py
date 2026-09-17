from pathlib import Path

import pytest

from sports_jobs.config import Settings


def _write_sources(path: Path) -> None:
    path.write_text(
        """
sources:
  - name: demo
    type: fixture
    path: jobs.json
    enabled: true
  - name: hudl
    type: greenhouse
    board_token: hudl
    enabled: true
  - name: veo
    type: lever
    site: veo
    enabled: true
  - name: disabled_board
    type: greenhouse
    board_token: disabled
    enabled: false
""",
        encoding="utf-8",
    )


def test_sources_separate_fixture_and_live_modes(tmp_path: Path) -> None:
    sources_file = tmp_path / "sources.yml"
    _write_sources(sources_file)

    fixture_sources = Settings(
        sources_file=sources_file,
        ingestion_mode="fixture",
    ).sources()
    live_sources = Settings(
        sources_file=sources_file,
        ingestion_mode="live",
    ).sources()

    assert [source["name"] for source in fixture_sources] == ["demo"]
    assert [source["name"] for source in live_sources] == ["hudl", "veo"]


def test_sources_reject_unknown_ingestion_mode(tmp_path: Path) -> None:
    sources_file = tmp_path / "sources.yml"
    _write_sources(sources_file)

    with pytest.raises(ValueError, match="Unsupported INGESTION_MODE"):
        Settings(sources_file=sources_file, ingestion_mode="unknown").sources()

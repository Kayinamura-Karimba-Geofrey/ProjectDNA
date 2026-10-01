"""Unit tests for ProjectDNA CLI commands."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from projectdna import __version__
from projectdna.cli import main


def test_cli_version(capsys: pytest.CaptureFixture[str]) -> None:
    """Verify version subcommand outputs current version."""
    exit_code = main(["version"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert f"ProjectDNA {__version__}" in captured.out


def test_cli_analyze_success(temp_repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Verify analyze subcommand successfully runs on test repository."""
    exit_code = main(["analyze", str(temp_repo)])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "PROJECTDNA" in captured.out
    assert "sample_project" in captured.out
    assert "Files" in captured.out
    assert "Directories" in captured.out


def test_cli_analyze_json(temp_repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Verify analyze with --format json outputs valid JSON schema."""
    exit_code = main(["analyze", str(temp_repo), "--format", "json"])
    assert exit_code == 0
    captured = capsys.readouterr()

    data = json.loads(captured.out)
    assert data["schema_version"] == "1.0"
    assert data["project"]["name"] == "sample_project"
    assert data["project"]["file_count"] == 5
    assert data["scan_stats"]["file_count"] == 5


def test_cli_analyze_output_file(temp_repo: Path, tmp_path: Path) -> None:
    """Verify analyze with -o writes to destination file."""
    output_file = tmp_path / "report.txt"
    exit_code = main(["analyze", str(temp_repo), "-o", str(output_file)])
    assert exit_code == 0
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "PROJECTDNA" in content
    assert "sample_project" in content


def test_cli_analyze_invalid_path(capsys: pytest.CaptureFixture[str]) -> None:
    """Verify analyze returns error code 1 when path does not exist."""
    exit_code = main(["analyze", "/path/nonexistent/xyz/999"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.out

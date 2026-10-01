"""Unit tests for data models."""

from __future__ import annotations

from pathlib import Path

from projectdna.analyzer.result import ProjectDNAResult
from projectdna.models.project import ProjectInfo
from projectdna.scanners.filesystem import ScanStats


def test_project_info_to_dict() -> None:
    """Verify ProjectInfo serialization."""
    info = ProjectInfo(
        name="test-repo",
        path=Path("/tmp/test-repo"),
        is_git_repo=True,
        file_count=10,
        dir_count=2,
        total_size_bytes=1024,
        formatted_size="1.0 KB",
    )
    d = info.to_dict()
    assert d["name"] == "test-repo"
    assert d["path"] == "/tmp/test-repo"
    assert d["is_git_repo"] is True
    assert d["file_count"] == 10
    assert d["dir_count"] == 2
    assert d["total_size_bytes"] == 1024
    assert d["formatted_size"] == "1.0 KB"


def test_project_dna_result_to_dict() -> None:
    """Verify ProjectDNAResult serialization to dictionary."""
    info = ProjectInfo(
        name="test-repo",
        path=Path("/tmp/test-repo"),
        is_git_repo=False,
        file_count=1,
        dir_count=1,
        total_size_bytes=50,
        formatted_size="50 B",
    )
    stats = ScanStats(file_count=1, dir_count=1, total_size_bytes=50)
    result = ProjectDNAResult(project=info, scan_stats=stats)

    d = result.to_dict()
    assert d["schema_version"] == "1.0"
    assert d["project"]["name"] == "test-repo"
    assert d["scan_stats"]["file_count"] == 1
    assert d["detectors"] == {}

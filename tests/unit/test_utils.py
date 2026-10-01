"""Unit tests for utility functions."""

from __future__ import annotations

from pathlib import Path

import pytest

from projectdna.utils.filesystem import format_bytes, is_git_repository, safe_resolve_path


def test_format_bytes() -> None:
    """Verify byte formatting handles various magnitudes correctly."""
    assert format_bytes(0) == "0 B"
    assert format_bytes(512) == "512 B"
    assert format_bytes(1024) == "1.0 KB"
    assert format_bytes(1536) == "1.5 KB"
    assert format_bytes(1024 * 1024) == "1.0 MB"
    assert format_bytes(1024 * 1024 * 1024) == "1.0 GB"
    assert format_bytes(1024 * 1024 * 1024 * 1024) == "1.0 TB"

    with pytest.raises(ValueError, match="negative"):
        format_bytes(-1)


def test_safe_resolve_path(tmp_path: Path) -> None:
    """Verify safe_resolve_path expands and resolves cleanly."""
    resolved = safe_resolve_path(str(tmp_path))
    assert resolved == tmp_path.resolve()


def test_is_git_repository(temp_repo: Path, tmp_path: Path) -> None:
    """Verify git repository detection via presence of .git."""
    assert is_git_repository(temp_repo) is True

    # Empty folder without .git
    non_git = tmp_path / "plain_dir"
    non_git.mkdir()
    assert is_git_repository(non_git) is False

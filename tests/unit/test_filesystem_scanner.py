"""Unit tests for FileSystemScanner."""

from __future__ import annotations

from pathlib import Path
import pytest

from projectdna.config import ScannerConfig
from projectdna.scanners.filesystem import FileSystemScanner


def test_scanner_scans_valid_directory(temp_repo: Path) -> None:
    """Verify scanner finds non-excluded files in repo."""
    scanner = FileSystemScanner()
    files, stats = scanner.scan(temp_repo)

    relative_paths = {str(f.relative_path) for f in files}

    assert "README.md" in relative_paths
    assert "app.py" in relative_paths
    assert "config.json" in relative_paths
    assert "src/main.py" in relative_paths
    assert "src/helper.py" in relative_paths

    # Excluded directories must NOT be in files
    assert not any(".git" in str(f.relative_path) for f in files)
    assert not any("node_modules" in str(f.relative_path) for f in files)
    assert not any("__pycache__" in str(f.relative_path) for f in files)

    assert stats.file_count == 5
    assert stats.dir_count >= 1
    assert stats.total_size_bytes > 0
    assert stats.skipped_dirs_count >= 3


def test_scanner_custom_excludes(temp_repo: Path) -> None:
    """Verify custom exclude patterns are honored."""
    config = ScannerConfig(custom_excludes=["src", "config.json"])
    scanner = FileSystemScanner(config=config)
    files, stats = scanner.scan(temp_repo)

    relative_paths = {str(f.relative_path) for f in files}
    assert "README.md" in relative_paths
    assert "app.py" in relative_paths
    assert "config.json" not in relative_paths
    assert not any(str(f.relative_path).startswith("src") for f in files)


def test_scanner_nonexistent_path() -> None:
    """Verify scanner raises FileNotFoundError on non-existent path."""
    scanner = FileSystemScanner()
    with pytest.raises(FileNotFoundError):
        scanner.scan(Path("/non/existent/path/for/sure/12345"))


def test_scanner_file_as_project_path(temp_repo: Path) -> None:
    """Verify scanner raises NotADirectoryError when given a file path."""
    scanner = FileSystemScanner()
    file_path = temp_repo / "README.md"
    with pytest.raises(NotADirectoryError):
        scanner.scan(file_path)


def test_scanner_include_hidden(temp_repo: Path) -> None:
    """Verify include_hidden flag allows dot-directories and dot-files when not in excluded_dirs."""
    # Create custom hidden file and folder
    hidden_dir = temp_repo / ".custom_hidden"
    hidden_dir.mkdir()
    (hidden_dir / "secret.txt").write_text("hidden\n", encoding="utf-8")

    # With default include_hidden=False
    scanner_default = FileSystemScanner(ScannerConfig(include_hidden=False))
    files_default, _ = scanner_default.scan(temp_repo)
    assert not any(".custom_hidden" in str(f.relative_path) for f in files_default)

    # With include_hidden=True
    scanner_hidden = FileSystemScanner(
        ScannerConfig(include_hidden=True, excluded_dirs={".git"})
    )
    files_hidden, _ = scanner_hidden.scan(temp_repo)
    hidden_paths = {str(f.relative_path) for f in files_hidden}
    assert ".custom_hidden/secret.txt" in hidden_paths

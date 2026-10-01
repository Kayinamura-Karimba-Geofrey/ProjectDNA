"""Pytest fixtures for ProjectDNA test suite."""

from __future__ import annotations

from pathlib import Path
import pytest


@pytest.fixture
def temp_repo(tmp_path: Path) -> Path:
    """Create a temporary dummy repository structure for testing."""
    repo = tmp_path / "sample_project"
    repo.mkdir()

    # Create dummy files
    (repo / "README.md").write_text("# Sample Project\n", encoding="utf-8")
    (repo / "app.py").write_text("print('hello world')\n", encoding="utf-8")
    (repo / "config.json").write_text('{"env": "test"}\n', encoding="utf-8")

    # Create subdirectories
    src_dir = repo / "src"
    src_dir.mkdir()
    (src_dir / "main.py").write_text("def run(): pass\n", encoding="utf-8")
    (src_dir / "helper.py").write_text("def help(): pass\n", encoding="utf-8")

    # Create excluded directories
    git_dir = repo / ".git"
    git_dir.mkdir()
    (git_dir / "config").write_text("[core]\n", encoding="utf-8")

    node_modules = repo / "node_modules"
    node_modules.mkdir()
    (node_modules / "dummy.js").write_text("console.log();\n", encoding="utf-8")

    cache_dir = repo / "__pycache__"
    cache_dir.mkdir()
    (cache_dir / "main.cpython-314.pyc").write_bytes(b"\x00\x00")

    return repo

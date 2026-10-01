"""Filesystem utility functions for safe path handling and size formatting."""

from __future__ import annotations

from pathlib import Path


def format_bytes(size_bytes: int) -> str:
    """Format bytes into human-readable units (B, KB, MB, GB, TB)."""
    if size_bytes < 0:
        raise ValueError("File size cannot be negative")

    if size_bytes < 1024:
        return f"{size_bytes} B"

    units = ["KB", "MB", "GB", "TB", "PB"]
    size = float(size_bytes)
    for unit in units:
        size /= 1024.0
        if size < 1024.0 or unit == units[-1]:
            return f"{size:.1f} {unit}"
    return f"{size:.1f} PB"


def safe_resolve_path(path_input: str | Path) -> Path:
    """Safely resolve an input path into an absolute Path."""
    p = Path(path_input).expanduser()
    try:
        return p.resolve()
    except (OSError, RuntimeError):
        return p.absolute()


def is_git_repository(project_path: Path) -> bool:
    """Check if the specified path is inside or is the root of a Git repository."""
    git_dir = project_path / ".git"
    if git_dir.exists():
        return True

    # Check parent hierarchy in case path is a sub-folder of a git repo
    try:
        curr = project_path
        while curr != curr.parent:
            if (curr / ".git").exists():
                return True
            curr = curr.parent
    except (PermissionError, OSError):
        pass

    return False

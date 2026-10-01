"""Configuration definitions and defaults for ProjectDNA."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_EXCLUDED_DIRS: frozenset[str] = frozenset({
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    ".env",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".nox",
    ".coverage",
    "htmlcov",
    "dist",
    "build",
    "target",
    ".idea",
    ".vscode",
    ".vs",
    ".next",
    ".nuxt",
    ".cache",
    ".gradle",
    "vendor",
    "Pods",
})

DEFAULT_EXCLUDED_EXTENSIONS: frozenset[str] = frozenset({
    ".pyc",
    ".pyo",
    ".pyd",
    ".so",
    ".dll",
    ".dylib",
    ".class",
    ".exe",
    ".o",
    ".a",
    ".obj",
    ".wasm",
    ".bin",
    ".iso",
    ".tar",
    ".gz",
    ".zip",
    ".7z",
    ".rar",
    ".lock",
    ".min.js",
    ".min.css",
})

DEFAULT_MAX_FILE_SIZE_BYTES: int = 15 * 1024 * 1024  # 15 MB


@dataclass(slots=True)
class ScannerConfig:
    """Configuration options for scanning and analyzing a repository."""

    excluded_dirs: set[str] = field(
        default_factory=lambda: set(DEFAULT_EXCLUDED_DIRS)
    )
    excluded_extensions: set[str] = field(
        default_factory=lambda: set(DEFAULT_EXCLUDED_EXTENSIONS)
    )
    custom_excludes: list[str] = field(default_factory=list)
    include_hidden: bool = False
    max_file_size_bytes: int = DEFAULT_MAX_FILE_SIZE_BYTES
    enable_git: bool = True
    enable_security: bool = True
    verbose: bool = False
    quiet: bool = False

    def is_directory_excluded(self, dir_name: str, rel_path: Path) -> bool:
        """Determine if a directory should be excluded from scanning."""
        if dir_name in self.excluded_dirs:
            return True
        if not self.include_hidden and dir_name.startswith("."):
            return True
        for pattern in self.custom_excludes:
            clean_pat = pattern.rstrip("/\\")
            if dir_name == clean_pat or clean_pat in str(rel_path):
                return True
        return False

    def is_file_excluded(self, file_name: str, file_suffix: str) -> bool:
        """Determine if a file should be excluded from scanning."""
        if not self.include_hidden and file_name.startswith("."):
            return True
        if file_suffix.lower() in self.excluded_extensions:
            return True
        return any(file_name == pattern for pattern in self.custom_excludes)

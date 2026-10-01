"""Context snapshot passed to detectors during project analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from projectdna.config import ScannerConfig
from projectdna.scanners.filesystem import ScannedFile, ScanStats
from projectdna.utils.logging import get_logger

logger = get_logger("analyzer.context")


@dataclass(slots=True)
class AnalysisContext:
    """Encapsulates all discovered filesystem assets and metadata for analysis."""

    project_path: Path
    config: ScannerConfig
    files: list[ScannedFile]
    stats: ScanStats
    is_git_repo: bool
    _files_by_name: dict[str, list[ScannedFile]] = field(
        init=False, default_factory=dict, repr=False
    )
    _files_by_ext: dict[str, list[ScannedFile]] = field(
        init=False, default_factory=dict, repr=False
    )

    def __post_init__(self) -> None:
        """Index scanned files by name and extension for O(1) lookups."""
        by_name: dict[str, list[ScannedFile]] = {}
        by_ext: dict[str, list[ScannedFile]] = {}

        for f in self.files:
            by_name.setdefault(f.name, []).append(f)
            by_ext.setdefault(f.extension, []).append(f)

        self._files_by_name = by_name
        self._files_by_ext = by_ext

    def has_file(self, filename: str) -> bool:
        """Check if any file with the given exact filename exists."""
        return filename in self._files_by_name

    def find_files_by_name(self, filename: str) -> list[ScannedFile]:
        """Return all scanned files matching the specified filename."""
        return self._files_by_name.get(filename, [])

    def find_files_by_extension(self, extension: str) -> list[ScannedFile]:
        """Return all scanned files with the given extension (e.g. '.py')."""
        clean_ext = extension.lower() if extension.startswith(".") else f".{extension.lower()}"
        return self._files_by_ext.get(clean_ext, [])

    def read_file_safely(
        self, scanned_file: ScannedFile, max_bytes: int | None = None
    ) -> str | None:
        """Safely read text from a scanned file, with encoding fallback and size protection."""
        limit = max_bytes or self.config.max_file_size_bytes
        if scanned_file.size_bytes > limit:
            logger.debug(
                "Skipping reading file %s: size %d exceeds limit %d",
                scanned_file.relative_path,
                scanned_file.size_bytes,
                limit,
            )
            return None

        for encoding in ("utf-8", "latin-1"):
            try:
                with open(scanned_file.path, encoding=encoding, errors="replace") as f:
                    return f.read(limit)
            except (OSError, PermissionError) as err:
                logger.debug(
                    "Error reading file %s: %s", scanned_file.relative_path, err
                )
                return None
        return None

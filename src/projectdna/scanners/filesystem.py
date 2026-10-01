"""Safe, high-performance filesystem scanner for repository analysis."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from projectdna.config import ScannerConfig
from projectdna.utils.logging import get_logger

logger = get_logger("scanner.filesystem")


@dataclass(slots=True)
class ScannedFile:
    """Metadata for an individual scanned file."""

    path: Path
    relative_path: Path
    name: str
    extension: str
    size_bytes: int
    is_symlink: bool = False


@dataclass(slots=True)
class ScanStats:
    """Aggregated statistics collected during a repository filesystem scan."""

    file_count: int = 0
    dir_count: int = 0
    total_size_bytes: int = 0
    skipped_files_count: int = 0
    skipped_dirs_count: int = 0
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, int | list[str]]:
        """Return serializable dictionary of scan statistics."""
        return {
            "file_count": self.file_count,
            "dir_count": self.dir_count,
            "total_size_bytes": self.total_size_bytes,
            "skipped_files_count": self.skipped_files_count,
            "skipped_dirs_count": self.skipped_dirs_count,
            "errors": list(self.errors),
        }


class FileSystemScanner:
    """Recursively and safely scans a repository's filesystem."""

    def __init__(self, config: ScannerConfig | None = None) -> None:
        self.config = config or ScannerConfig()

    def scan(self, root_path: Path) -> tuple[list[ScannedFile], ScanStats]:
        """Scan root_path and return all matching files alongside aggregated statistics.

        Safe against broken symlinks, permission denials, and deep directory trees.
        """
        scanned_files: list[ScannedFile] = []
        stats = ScanStats()

        root_resolved = root_path.resolve()
        if not root_resolved.exists():
            raise FileNotFoundError(f"Project path does not exist: {root_path}")
        if not root_resolved.is_dir():
            raise NotADirectoryError(f"Project path is not a directory: {root_path}")

        visited_dir_ids: set[tuple[int, int]] = set()

        for dirpath_str, dirnames, filenames in os.walk(
            str(root_resolved), topdown=True, followlinks=False
        ):
            current_dir = Path(dirpath_str)

            # Guard against circular directory symlink loops
            try:
                dir_stat = current_dir.stat()
                dir_id = (dir_stat.st_dev, dir_stat.st_ino)
                if dir_id in visited_dir_ids:
                    dirnames.clear()
                    continue
                visited_dir_ids.add(dir_id)
            except OSError as err:
                stats.errors.append(f"Cannot stat directory '{current_dir}': {err}")
                dirnames.clear()
                continue

            # Compute relative path from project root
            try:
                rel_dir = current_dir.relative_to(root_resolved)
            except ValueError:
                rel_dir = Path(".")

            # Filter directory traversal in-place (topdown=True)
            kept_dirnames: list[str] = []
            for d in dirnames:
                dir_rel_path = rel_dir / d if rel_dir != Path(".") else Path(d)
                if self.config.is_directory_excluded(d, dir_rel_path):
                    stats.skipped_dirs_count += 1
                    logger.debug("Skipping excluded directory: %s", dir_rel_path)
                else:
                    kept_dirnames.append(d)
                    stats.dir_count += 1

            dirnames[:] = kept_dirnames

            # Process files in current directory
            for f in filenames:
                file_path = current_dir / f
                try:
                    rel_file_path = file_path.relative_to(root_resolved)
                except ValueError:
                    rel_file_path = Path(f)

                suffix = file_path.suffix.lower()

                if self.config.is_file_excluded(f, suffix):
                    stats.skipped_files_count += 1
                    logger.debug("Skipping excluded file: %s", rel_file_path)
                    continue

                is_symlink = file_path.is_symlink()
                try:
                    # Use lstat or stat; stat follows symlink, catch if broken
                    st = file_path.stat()
                    file_size = st.st_size
                except (OSError, PermissionError) as err:
                    stats.errors.append(f"Cannot access file '{rel_file_path}': {err}")
                    stats.skipped_files_count += 1
                    continue

                stats.file_count += 1
                stats.total_size_bytes += file_size

                scanned_files.append(
                    ScannedFile(
                        path=file_path,
                        relative_path=rel_file_path,
                        name=f,
                        extension=suffix,
                        size_bytes=file_size,
                        is_symlink=is_symlink,
                    )
                )

        return scanned_files, stats

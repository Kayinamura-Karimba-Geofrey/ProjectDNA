"""Central analysis engine orchestrating the repository inspection pipeline."""

from __future__ import annotations

from pathlib import Path

from projectdna.analyzer.context import AnalysisContext
from projectdna.analyzer.result import ProjectDNAResult
from projectdna.config import ScannerConfig
from projectdna.detectors.base import DetectionResult, Detector
from projectdna.models.project import ProjectInfo
from projectdna.scanners.filesystem import FileSystemScanner
from projectdna.utils.filesystem import format_bytes, is_git_repository, safe_resolve_path
from projectdna.utils.logging import get_logger

logger = get_logger("analyzer.engine")


class AnalysisEngine:
    """Central engine that coordinates filesystem scanning and detector execution."""

    def __init__(self, config: ScannerConfig | None = None) -> None:
        self.config = config or ScannerConfig()
        self.scanner = FileSystemScanner(self.config)
        self._detectors: list[Detector] = []

    def register_detector(self, detector: Detector) -> None:
        """Register a detector to be executed during the analysis phase."""
        self._detectors.append(detector)

    def analyze(self, project_path: str | Path) -> ProjectDNAResult:
        """Execute full repository analysis on the specified path."""
        resolved_path = safe_resolve_path(project_path)

        if not resolved_path.exists():
            raise FileNotFoundError(f"Project directory does not exist: {project_path}")
        if not resolved_path.is_dir():
            raise NotADirectoryError(f"Specified path is not a directory: {project_path}")

        logger.info("Starting repository analysis on '%s'", resolved_path)

        # 1. Scan filesystem
        files, scan_stats = self.scanner.scan(resolved_path)
        logger.debug(
            "Scan complete: %d files, %d dirs, %d bytes",
            scan_stats.file_count,
            scan_stats.dir_count,
            scan_stats.total_size_bytes,
        )

        # 2. Check Git repository
        git_detected = False
        if self.config.enable_git:
            git_detected = is_git_repository(resolved_path)

        # 3. Build Analysis Context
        context = AnalysisContext(
            project_path=resolved_path,
            config=self.config,
            files=files,
            stats=scan_stats,
            is_git_repo=git_detected,
        )

        # 4. Run registered detectors
        detector_results: dict[str, DetectionResult] = {}
        for detector in self._detectors:
            try:
                res = detector.detect(context)
                detector_results[detector.name] = res
            except Exception as err:  # noqa: BLE001
                logger.warning("Detector '%s' failed: %s", detector.name, err)

        # 5. Build ProjectInfo model
        project_name = resolved_path.name or "repository"
        formatted_size = format_bytes(scan_stats.total_size_bytes)

        project_info = ProjectInfo(
            name=project_name,
            path=resolved_path,
            is_git_repo=git_detected,
            file_count=scan_stats.file_count,
            dir_count=scan_stats.dir_count,
            total_size_bytes=scan_stats.total_size_bytes,
            formatted_size=formatted_size,
        )

        # 6. Generate unified ProjectDNAResult
        return ProjectDNAResult(
            project=project_info,
            scan_stats=scan_stats,
            detector_results=detector_results,
        )

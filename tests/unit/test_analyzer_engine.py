"""Unit tests for AnalysisEngine and AnalysisContext."""

from __future__ import annotations

from pathlib import Path

import pytest

from projectdna.analyzer.context import AnalysisContext
from projectdna.analyzer.engine import AnalysisEngine
from projectdna.config import ScannerConfig
from projectdna.detectors.base import DetectionResult, Detector


class DummyDetector(Detector):
    """Test detector implementation."""

    @property
    def name(self) -> str:
        return "dummy_detector"

    def detect(self, context: AnalysisContext) -> DetectionResult:
        has_readme = context.has_file("README.md")
        return DetectionResult(
            detector_name=self.name,
            detected=has_readme,
            data={"readme_found": has_readme},
            evidence=["README.md found in project root"] if has_readme else [],
        )


def test_engine_analyzes_valid_repo(temp_repo: Path) -> None:
    """Verify engine returns complete ProjectDNAResult."""
    engine = AnalysisEngine()
    result = engine.analyze(temp_repo)

    assert result.project.name == "sample_project"
    assert result.project.path == temp_repo.resolve()
    assert result.project.is_git_repo is True
    assert result.project.file_count == 5
    assert result.project.dir_count >= 1
    assert result.project.total_size_bytes > 0
    assert result.project.formatted_size != ""


def test_engine_with_registered_detector(temp_repo: Path) -> None:
    """Verify detector registration and invocation during analysis."""
    engine = AnalysisEngine()
    dummy = DummyDetector()
    engine.register_detector(dummy)

    result = engine.analyze(temp_repo)

    assert "dummy_detector" in result.detector_results
    detection = result.detector_results["dummy_detector"]
    assert detection.detected is True
    assert detection.data == {"readme_found": True}
    assert len(detection.evidence) == 1


def test_engine_raises_on_invalid_path() -> None:
    """Verify engine raises when directory does not exist."""
    engine = AnalysisEngine()
    with pytest.raises(FileNotFoundError):
        engine.analyze("/path/that/does/not/exist/987654")


def test_context_lookups_and_safe_read(temp_repo: Path) -> None:
    """Verify context file search and reading helpers."""
    engine = AnalysisEngine()
    files, stats = engine.scanner.scan(temp_repo)
    ctx = AnalysisContext(
        project_path=temp_repo,
        config=ScannerConfig(),
        files=files,
        stats=stats,
        is_git_repo=True,
    )

    assert ctx.has_file("README.md") is True
    assert ctx.has_file("nonexistent.txt") is False

    py_files = ctx.find_files_by_extension("py")
    assert len(py_files) == 3  # app.py, src/main.py, src/helper.py

    readme_files = ctx.find_files_by_name("README.md")
    assert len(readme_files) == 1
    content = ctx.read_file_safely(readme_files[0])
    assert content is not None
    assert "Sample Project" in content

"""Unified ProjectDNA result model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from projectdna.detectors.base import DetectionResult
from projectdna.models.project import ProjectInfo
from projectdna.scanners.filesystem import ScanStats


@dataclass(slots=True)
class ProjectDNAResult:
    """Consolidated intelligence report produced by the analysis engine."""

    project: ProjectInfo
    scan_stats: ScanStats
    schema_version: str = "1.0"
    detector_results: dict[str, DetectionResult] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert entire result into a JSON-serializable dictionary."""
        return {
            "schema_version": self.schema_version,
            "project": self.project.to_dict(),
            "scan_stats": self.scan_stats.to_dict(),
            "detectors": {
                name: {
                    "detector_name": res.detector_name,
                    "detected": res.detected,
                    "confidence": res.confidence,
                    "data": res.data,
                    "evidence": res.evidence,
                }
                for name, res in self.detector_results.items()
            },
        }

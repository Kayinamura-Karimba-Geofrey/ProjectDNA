"""Base abstractions and interfaces for ProjectDNA detectors."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from projectdna.analyzer.context import AnalysisContext


@dataclass(slots=True)
class DetectionResult:
    """Standardized result produced by a detector."""

    detector_name: str
    detected: bool
    data: dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    evidence: list[str] = field(default_factory=list)


class Detector(ABC):
    """Abstract Base Class that every technology and pattern detector must implement."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier name of the detector."""
        ...

    @abstractmethod
    def detect(self, context: AnalysisContext) -> DetectionResult:
        """Execute detection logic against the gathered repository analysis context."""
        ...

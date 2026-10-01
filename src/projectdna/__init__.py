"""ProjectDNA - Professional Repository Intelligence & Project Analysis Tool."""

from __future__ import annotations

__version__ = "0.1.0"
__author__ = "Kayinamura Karimba Geofrey"
__license__ = "MIT"

from projectdna.analyzer.context import AnalysisContext
from projectdna.analyzer.engine import AnalysisEngine
from projectdna.analyzer.result import ProjectDNAResult
from projectdna.config import ScannerConfig
from projectdna.models.project import ProjectInfo

__all__ = [
    "AnalysisContext",
    "AnalysisEngine",
    "ProjectDNAResult",
    "ProjectInfo",
    "ScannerConfig",
    "__version__",
]

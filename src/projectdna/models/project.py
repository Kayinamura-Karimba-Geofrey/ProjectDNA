"""Project identification and high-level metadata model."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ProjectInfo:
    """Core high-level metadata for an analyzed repository."""

    name: str
    path: Path
    is_git_repo: bool
    file_count: int
    dir_count: int
    total_size_bytes: int
    formatted_size: str

    def to_dict(self) -> dict[str, Any]:
        """Convert the project information to a serializable dictionary."""
        data = asdict(self)
        data["path"] = str(self.path)
        return data

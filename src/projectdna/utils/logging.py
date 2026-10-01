"""Structured logging utility for ProjectDNA."""

from __future__ import annotations

import logging
import sys


def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """Configure logging based on CLI flags."""
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    root_logger = logging.getLogger("projectdna")
    root_logger.setLevel(level)

    # Avoid duplicate handlers if setup_logging is called multiple times
    if not root_logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
    else:
        for handler in root_logger.handlers:
            handler.setLevel(level)


def get_logger(name: str) -> logging.Logger:
    """Return a logger child of the projectdna root logger."""
    return logging.getLogger(f"projectdna.{name}")

"""Entrypoint for running ProjectDNA as a module: python -m projectdna."""

from __future__ import annotations

import sys

from projectdna.cli import main

if __name__ == "__main__":
    sys.exit(main())

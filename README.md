# ProjectDNA 🧬

**Professional Repository Intelligence & Project Analysis Tool**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type Checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy-lang.org/)

ProjectDNA is a repository intelligence tool that inspects local software projects and generates a structured "DNA profile" — discovering technologies, architecture patterns, dependencies, code statistics, security indicators, and overall project health.

---

## 🌟 Key Features (Phase 1 Foundation)

- **Fast & Safe Filesystem Inspection**: Recursively scans repositories while respecting ignore patterns (e.g. `.git`, `node_modules`, virtual environments, cache folders).
- **Core Repository Diagnostics**: Accurately counts files and directories, computes total repository footprint, and detects Git repository status.
- **Robust Error Handling**: Safely handles permission issues, broken symlinks, large files, and unsupported file encodings without crashing.
- **Rich Terminal UI**: Beautiful, human-readable terminal output powered by `rich`.
- **Extensible Architecture**: Clean layered architecture designed for pluggable language, framework, database, Docker, CI/CD, and security detectors.
- **Strict Code Quality**: Built with 100% type annotations (`mypy --strict`), PEP 8 standards (`ruff`), and comprehensive unit/integration test coverage (`pytest`).

---

## 🚀 Quick Start

### Installation

Clone the repository and install in editable mode:

```bash
git clone https://github.com/Kayinamura-Karimba-Geofrey/ProjectDNA.git
cd ProjectDNA
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Usage

Analyze the current directory:

```bash
projectdna analyze .
```

Analyze a specific project directory:

```bash
projectdna analyze /path/to/project
```

Check the version:

```bash
projectdna version
```

View all options:

```bash
projectdna --help
```

---

## 💻 CLI Options

```text
usage: projectdna [-h] [-V] {analyze,version} ...

ProjectDNA - Professional Repository Intelligence & Project Analysis Tool

positional arguments:
  {analyze,version}
    analyze          Analyze a project repository and generate intelligence report
    version          Show version information

options:
  -h, --help         show this help message and exit
  -V, --version      show program's version number and exit
```

### `projectdna analyze` Options

```text
usage: projectdna analyze [-h] [--format {terminal,json,markdown,html}]
                          [--output OUTPUT] [--exclude EXCLUDE]
                          [--include-hidden] [--verbose] [--quiet]
                          [--no-git] [--no-security]
                          path

positional arguments:
  path                  Path to the project repository to analyze

options:
  -h, --help            show this help message and exit
  --format {terminal,json,markdown,html}
                        Output format (default: terminal)
  --output OUTPUT, -o OUTPUT
                        Save output report to specified file path
  --exclude EXCLUDE, -e EXCLUDE
                        Additional directories or file patterns to exclude
  --include-hidden      Include hidden files and folders in analysis
  --verbose, -v         Enable verbose diagnostic logging
  --quiet, -q           Suppress all output except errors
  --no-git              Disable Git repository inspection
  --no-security         Disable security and secret scanning
```

---

## 🧩 Architecture Overview

```text
src/projectdna/
├── __init__.py           # Package initialization & version metadata
├── __main__.py           # Support for `python -m projectdna`
├── cli.py                # Command-line interface & argument parsing
├── config.py             # Global defaults and scanner configurations
│
├── analyzer/
│   ├── engine.py         # Central AnalysisEngine orchestrating pipeline
│   ├── context.py        # AnalysisContext holding discovered files & metadata
│   └── result.py         # Unified ProjectDNAResult data models
│
├── detectors/
│   └── base.py           # Abstract Base Class for pluggable detectors
│
├── scanners/
│   └── filesystem.py     # Resilient directory traverser & metadata collector
│
├── models/
│   └── project.py        # Core project information data models
│
├── reporters/
│   └── terminal.py       # Rich terminal reporter and dashboard
│
└── utils/
    ├── filesystem.py     # Safe filesystem helpers (size formatting, permissions)
    └── logging.py        # Structured logging configuration
```

---

## 🧪 Development & Quality Checks

Run test suite:
```bash
pytest
```

Run linter:
```bash
ruff check .
```

Run static type checker:
```bash
mypy src
```

---

## 🗺️ Project Roadmap

- [x] **Phase 1: Foundation** — Architecture, CLI, Filesystem Scanner, Context, Rich Terminal Output
- [ ] **Phase 2: Core Detection** — Languages, Frameworks, Databases, Dependencies
- [ ] **Phase 3: Infrastructure Detection** — Docker, CI/CD, Testing Frameworks, Git Insights
- [ ] **Phase 4: Architecture & Stats** — Heuristics, Pattern Classification, Code Statistics
- [ ] **Phase 5: Security** — Non-destructive Secret & Misconfiguration Scanner
- [ ] **Phase 6: Multi-format Reporting** — JSON, Markdown, Standalone HTML
- [ ] **Phase 7: Comprehensive Test Suites** — Fixture repositories and edge cases
- [ ] **Phase 8: Packaging & Release** — PyPI distribution and wheel builds

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

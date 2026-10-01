# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-10-01

### Added
- Phase 1 Foundation:
  - Central `AnalysisEngine` orchestrating project discovery.
  - `AnalysisContext` for gathering filesystem snapshot and metadata.
  - `FileSystemScanner` with safe traversal, exclusion filters, and error recovery.
  - `ProjectInfo` and `ProjectDNAResult` typed data models.
  - Pluggable `Detector` abstract base class for Phase 2+ detectors.
  - Rich-powered terminal reporter displaying repository profile banner and stats.
  - Robust CLI with `analyze`, `version`, `--format`, `--output`, `--exclude`, `--verbose`, `--quiet`, `--no-git`, and `--no-security`.
  - Type-safe utilities for file size formatting, path checks, and logging.
  - Strict type checking with `mypy`, linting with `ruff`, and test suite with `pytest`.

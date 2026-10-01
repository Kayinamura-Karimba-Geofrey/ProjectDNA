# Contributing to ProjectDNA

Thank you for your interest in contributing to **ProjectDNA**!

## Code Quality Standards

Before submitting changes, make sure your code adheres to:

1. **Python 3.11+** modern syntax and typing.
2. **Strict type hints** (`mypy src --strict` must pass with 0 errors).
3. **PEP 8 compliance & linting** (`ruff check .` must pass with 0 errors).
4. **Automated tests** (`pytest` must pass with all unit/integration tests).
5. **Safe, read-only filesystem operations**: ProjectDNA must never mutate the analyzed repository.

## Development Workflow

1. Fork and clone the repository.
2. Set up virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```
3. Run tests and linters:
   ```bash
   pytest
   ruff check .
   mypy src
   ```
4. Submit your pull request with a descriptive title and commit message following [Conventional Commits](https://www.conventionalcommits.org/).

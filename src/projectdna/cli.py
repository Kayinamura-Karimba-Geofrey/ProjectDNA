"""Command-line interface (CLI) for ProjectDNA."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from rich.console import Console

from projectdna import __version__
from projectdna.analyzer.engine import AnalysisEngine
from projectdna.config import ScannerConfig
from projectdna.reporters.terminal import TerminalReporter
from projectdna.utils.logging import setup_logging


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level argument parser for the ProjectDNA CLI."""
    parser = argparse.ArgumentParser(
        prog="projectdna",
        description="ProjectDNA - Professional Repository Intelligence & Project Analysis Tool",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"ProjectDNA {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Subcommand to execute")

    # Command: analyze
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a project repository and generate an intelligence report",
    )
    analyze_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to the repository to inspect (default: current directory)",
    )
    analyze_parser.add_argument(
        "--format",
        choices=["terminal", "json", "markdown", "html"],
        default="terminal",
        help="Output format (default: terminal)",
    )
    analyze_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="File path to write the generated report",
    )
    analyze_parser.add_argument(
        "-e",
        "--exclude",
        action="append",
        default=[],
        help="Directory or file pattern to exclude (can be specified multiple times)",
    )
    analyze_parser.add_argument(
        "--include-hidden",
        action="store_true",
        default=False,
        help="Include hidden files and directories in scanning",
    )
    analyze_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Enable detailed diagnostic logging",
    )
    analyze_parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="Suppress console output except for errors",
    )
    analyze_parser.add_argument(
        "--no-git",
        action="store_true",
        default=False,
        help="Disable Git repository inspection",
    )
    analyze_parser.add_argument(
        "--no-security",
        action="store_true",
        default=False,
        help="Disable security scanning (for Phase 5+)",
    )

    # Command: version
    subparsers.add_parser("version", help="Show ProjectDNA version information")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point for ProjectDNA."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "version":
        print(f"ProjectDNA {__version__}")
        return 0

    if args.command == "analyze":
        setup_logging(verbose=args.verbose, quiet=args.quiet)
        console = Console(quiet=args.quiet)

        # Parse custom excludes (allow comma-separated or multiple flags)
        custom_excludes: list[str] = []
        for exc in args.exclude:
            custom_excludes.extend([p.strip() for p in exc.split(",") if p.strip()])

        config = ScannerConfig(
            custom_excludes=custom_excludes,
            include_hidden=args.include_hidden,
            enable_git=not args.no_git,
            enable_security=not args.no_security,
            verbose=args.verbose,
            quiet=args.quiet,
        )

        target_path = Path(args.path)

        try:
            engine = AnalysisEngine(config=config)
            result = engine.analyze(target_path)
        except (FileNotFoundError, NotADirectoryError) as err:
            console.print(f"[bold red]Error:[/bold red] {err}", style="red")
            return 1
        except Exception as err:  # noqa: BLE001
            console.print(
                f"[bold red]Unexpected analysis error:[/bold red] {err}", style="red"
            )
            return 2

        # Format and output report
        reporter = TerminalReporter(console=console)
        if args.format == "terminal":
            reporter.render(result)
            if args.output:
                output_str = reporter.render_to_string(result)
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(output_str, encoding="utf-8")
        elif args.format == "json":
            import json

            json_str = json.dumps(result.to_dict(), indent=2)
            if args.output:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(json_str, encoding="utf-8")
            else:
                print(json_str)
        else:
            console.print(
                f"[bold yellow]Note:[/bold yellow] Format '{args.format}' will be "
                "fully implemented in Phase 6. Falling back to terminal display."
            )
            reporter.render(result)

        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())

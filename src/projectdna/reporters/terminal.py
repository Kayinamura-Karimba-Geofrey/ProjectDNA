"""Rich terminal reporter for formatting ProjectDNA repository intelligence."""

from __future__ import annotations

import io
from typing import TextIO

from rich.console import Console
from rich.table import Table

from projectdna.analyzer.result import ProjectDNAResult


class TerminalReporter:
    """Renders formatted ProjectDNA analysis results to the terminal using rich."""

    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()

    def render(self, result: ProjectDNAResult) -> None:
        """Render the full project intelligence report directly to stdout/console."""
        proj = result.project

        # Header Banner
        banner = (
            "[bold cyan]╔════════════════════════════════════════════════════╗\n"
            "║                  [bold white]PROJECTDNA[/bold white]                        ║\n"
            "║            [dim]Repository Intelligence[/dim]                 ║\n"
            "╚════════════════════════════════════════════════════╝[/bold cyan]"
        )
        self.console.print(banner)
        self.console.print()

        # Project Section Table
        table = Table(
            title="[bold white]Project[/bold white]",
            title_justify="left",
            show_header=False,
            box=None,
            pad_edge=False,
            padding=(0, 2),
        )
        table.add_column("Field", style="bold cyan", min_width=18)
        table.add_column("Separator", style="dim", width=1)
        table.add_column("Value", style="white")

        table.add_row("Name", ":", proj.name)
        table.add_row("Path", ":", str(proj.path))
        table.add_row(
            "Git Repository",
            ":",
            "[green]Yes[/green]" if proj.is_git_repo else "[yellow]No[/yellow]",
        )
        table.add_row("Files", ":", f"{proj.file_count:,}")
        table.add_row("Directories", ":", f"{proj.dir_count:,}")
        table.add_row("Total Size", ":", f"{proj.formatted_size} ({proj.total_size_bytes:,} bytes)")

        # Print horizontal divider and table
        self.console.rule("[bold cyan]Repository Overview[/bold cyan]", align="left")
        self.console.print(table)
        self.console.print()

        # Display any scanning warnings/errors if encountered
        if result.scan_stats.errors:
            self.console.rule("[bold red]Scan Warnings / Errors[/bold red]", align="left")
            for err in result.scan_stats.errors:
                self.console.print(f" [bold red]•[/bold red] [yellow]{err}[/yellow]")
            self.console.print()

    def render_to_string(self, result: ProjectDNAResult) -> str:
        """Render the report to an ANSI-stripped or plain text string."""
        buffer = io.StringIO()
        capture_console = Console(file=buffer, force_terminal=False, color_system=None)
        old_console = self.console
        self.console = capture_console
        try:
            self.render(result)
            return buffer.getvalue()
        finally:
            self.console = old_console

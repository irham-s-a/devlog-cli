"""Terminal display formatting using Rich."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .models import Entry

import sys
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

console = Console(force_terminal=True)


def show_entry_table(entries: list[Entry], title: str = "📋 Log Dev") -> None:
    """Display a list of entries in a Rich table.

    Args:
        entries: List of Entry objects to display.
        title: Title for the table.
    """
    if not entries:
        console.print("[yellow]Tidak ada entri ditemukan.[/yellow]")
        return

    table = Table(title=title, show_lines=True)
    table.add_column("ID", style="cyan", justify="center", width=5)
    table.add_column("Waktu", style="green", width=20)
    table.add_column("Tag", style="magenta", width=12)
    table.add_column("Catatan", style="white", min_width=30)

    for entry in entries:
        tag_display = f"\\[{entry.tag}]" if entry.tag else "-"
        waktu = _format_datetime(entry.created_at) if entry.created_at else "-"
        table.add_row(str(entry.id), waktu, tag_display, entry.message)

    console.print(table)


def show_add_success(entry: Entry) -> None:
    """Display a success panel after adding an entry.

    Args:
        entry: The newly created Entry object.
    """
    tag_info = f" [magenta]\\[{entry.tag}][/magenta]" if entry.tag else ""
    message = f"✅ Log berhasil ditambahkan!{tag_info}\n\n[dim]{entry.message}[/dim]"
    console.print(Panel(message, title="DevLog", border_style="green"))


def show_delete_success(entry_id: int) -> None:
    """Display a success message after deleting an entry.

    Args:
        entry_id: The ID of the deleted entry.
    """
    console.print(f"[green]✅ Entri #{entry_id} berhasil dihapus![/green]")


def show_entry_not_found(entry_id: int) -> None:
    """Display an error when an entry is not found.

    Args:
        entry_id: The ID that was not found.
    """
    console.print(f"[red]❌ Entri #{entry_id} tidak ditemukan.[/red]")


def show_export_success(filepath: str, count: int) -> None:
    """Display a success message after exporting entries.

    Args:
        filepath: Path to the exported file.
        count: Number of entries exported.
    """
    console.print(
        f"[green]✅ {count} entri berhasil diekspor ke [cyan]{filepath}[/cyan][/green]"
    )


def show_stats(stats: dict) -> None:
    """Display statistics in a formatted panel.

    Args:
        stats: Dictionary with keys: total_entries, week_entries, longest_streak, top_tags.
    """
    table = Table(title="📊 Statistik DevLog", show_lines=True)
    table.add_column("Metrik", style="cyan", width=25)
    table.add_column("Nilai", style="green", width=30)

    table.add_row("Total Entri", str(stats["total_entries"]))
    table.add_row("Entri Minggu Ini", str(stats["week_entries"]))
    table.add_row("Streak Terpanjang", f"{stats['longest_streak']} hari")

    if stats["top_tags"]:
        tags_str = ", ".join(
            f"[{tag}] ({count})" for tag, count in stats["top_tags"]
        )
        table.add_row("Tag Teratas", tags_str)
    else:
        table.add_row("Tag Teratas", "-")

    console.print(table)


def _format_datetime(dt_str: str) -> str:
    """Format a datetime string for display.

    Args:
        dt_str: Datetime string from the database.

    Returns:
        Formatted datetime string.
    """
    try:
        from datetime import datetime

        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d %b %Y %H:%M")
    except (ValueError, TypeError):
        return dt_str

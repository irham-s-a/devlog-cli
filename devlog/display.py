"""Terminal display formatting using Rich — bilingual (EN default, -idn for ID)."""

import sys
import io
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .models import Entry

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

console = Console(force_terminal=True)

MSG = {
    "en": {
        "no_entries": "No entries found.",
        "col_id": "ID",
        "col_time": "Time",
        "col_tag": "Tag",
        "col_note": "Note",
        "add_success": "Log added successfully!",
        "delete_success": "Entry #{id} deleted successfully!",
        "not_found": "Entry #{id} not found.",
        "export_success": "{count} entries exported to {path}",
        "stats_title": "📊 DevLog Statistics",
        "stats_metric": "Metric",
        "stats_value": "Value",
        "stats_total": "Total Entries",
        "stats_week": "Entries This Week",
        "stats_streak": "Longest Streak",
        "stats_days": "days",
        "stats_top_tags": "Top Tags",
        "title_today": "📋 Today's Log",
        "title_week": "📋 This Week's Log",
        "title_all": "📋 All Logs",
        "title_tag": "📋 Log — Tag: {tag}",
        "confirm_delete": "Are you sure you want to delete entry #{id}? \"{msg}\"",
        "no_export": "No entries to export.",
    },
    "idn": {
        "no_entries": "Tidak ada entri ditemukan.",
        "col_id": "ID",
        "col_time": "Waktu",
        "col_tag": "Tag",
        "col_note": "Catatan",
        "add_success": "Log berhasil ditambahkan!",
        "delete_success": "Entri #{id} berhasil dihapus!",
        "not_found": "Entri #{id} tidak ditemukan.",
        "export_success": "{count} entri berhasil diekspor ke {path}",
        "stats_title": "📊 Statistik DevLog",
        "stats_metric": "Metrik",
        "stats_value": "Nilai",
        "stats_total": "Total Entri",
        "stats_week": "Entri Minggu Ini",
        "stats_streak": "Streak Terpanjang",
        "stats_days": "hari",
        "stats_top_tags": "Tag Teratas",
        "title_today": "📋 Log Hari Ini",
        "title_week": "📋 Log Minggu Ini",
        "title_all": "📋 Semua Log",
        "title_tag": "📋 Log — Tag: {tag}",
        "confirm_delete": "Yakin ingin menghapus entri #{id}? \"{msg}\"",
        "no_export": "Tidak ada entri untuk diekspor.",
    },
}


def t(key: str, lang: str = "en", **kwargs) -> str:
    """Translate a message key to the selected language.

    Args:
        key: Message key from MSG dict.
        lang: Language code ('en' or 'idn').
        **kwargs: Format parameters for the message.

    Returns:
        Translated and formatted string.
    """
    text = MSG.get(lang, MSG["en"]).get(key, MSG["en"].get(key, key))
    if kwargs:
        text = text.format(**kwargs)
    return text


def show_entry_table(
    entries: list[Entry],
    lang: str = "en",
    title: Optional[str] = None,
    title_key: str = "title_today",
    tag_filter: Optional[str] = None,
) -> None:
    """Display a list of entries in a Rich table.

    Args:
        entries: List of Entry objects to display.
        lang: Language code ('en' or 'idn').
        title: Override title string. If None, uses title_key.
        title_key: Key for the default title.
        tag_filter: Tag filter value for title formatting.
    """
    if not entries:
        console.print(f"[yellow]{t('no_entries', lang)}[/yellow]")
        return

    if title is None:
        if tag_filter:
            title = t("title_tag", lang, tag=tag_filter)
        else:
            title = t(title_key, lang)

    table = Table(title=title, show_lines=True)
    table.add_column(t("col_id", lang), style="cyan", justify="center", width=5)
    table.add_column(t("col_time", lang), style="green", width=20)
    table.add_column(t("col_tag", lang), style="magenta", width=12)
    table.add_column(t("col_note", lang), style="white", min_width=30)

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
    message = f"✅ {t('add_success', 'en')}{tag_info}\n\n[dim]{entry.message}[/dim]"
    console.print(Panel(message, title="DevLog", border_style="green"))


def show_delete_success(entry_id: int, lang: str = "en") -> None:
    """Display a success message after deleting an entry.

    Args:
        entry_id: The ID of the deleted entry.
        lang: Language code ('en' or 'idn').
    """
    console.print(f"[green]✅ {t('delete_success', lang, id=entry_id)}[/green]")


def show_entry_not_found(entry_id: int, lang: str = "en") -> None:
    """Display an error when an entry is not found.

    Args:
        entry_id: The ID that was not found.
        lang: Language code ('en' or 'idn').
    """
    console.print(f"[red]❌ {t('not_found', lang, id=entry_id)}[/red]")


def show_export_success(filepath: str, count: int, lang: str = "en") -> None:
    """Display a success message after exporting entries.

    Args:
        filepath: Path to the exported file.
        count: Number of entries exported.
        lang: Language code ('en' or 'idn').
    """
    msg = t("export_success", lang, count=count, path=filepath)
    console.print(f"[green]✅ {msg}[/green]")


def show_stats(stats: dict, lang: str = "en") -> None:
    """Display statistics in a formatted panel.

    Args:
        stats: Dictionary with keys: total_entries, week_entries, longest_streak, top_tags.
        lang: Language code ('en' or 'idn').
    """
    table = Table(title=t("stats_title", lang), show_lines=True)
    table.add_column(t("stats_metric", lang), style="cyan", width=25)
    table.add_column(t("stats_value", lang), style="green", width=30)

    table.add_row(t("stats_total", lang), str(stats["total_entries"]))
    table.add_row(t("stats_week", lang), str(stats["week_entries"]))
    table.add_row(
        t("stats_streak", lang),
        f"{stats['longest_streak']} {t('stats_days', lang)}",
    )

    if stats["top_tags"]:
        tags_str = ", ".join(
            f"\\[{tag}] ({count})" for tag, count in stats["top_tags"]
        )
        table.add_row(t("stats_top_tags", lang), tags_str)
    else:
        table.add_row(t("stats_top_tags", lang), "-")

    console.print(table)


def get_confirm_delete(entry_id: int, message: str, lang: str = "en") -> str:
    """Return the confirmation prompt string for delete.

    Args:
        entry_id: The entry ID.
        message: The entry message.
        lang: Language code ('en' or 'idn').

    Returns:
        Confirmation prompt string.
    """
    return t("confirm_delete", lang, id=entry_id, msg=message)


def get_no_export_msg(lang: str = "en") -> str:
    """Return the 'no entries to export' message.

    Args:
        lang: Language code ('en' or 'idn').

    Returns:
        Message string.
    """
    return t("no_export", lang)


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

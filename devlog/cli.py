"""CLI commands for devlog using Click — bilingual (EN default, -idn for ID)."""

import click
from datetime import datetime

from . import __version__
from .db import (
    add_entry,
    get_entries_today,
    get_entries_week,
    get_entries_all,
    get_entries_by_tag,
    get_entry_by_id,
    delete_entry,
    get_stats,
)
from .display import (
    show_entry_table,
    show_add_success,
    show_delete_success,
    show_entry_not_found,
    show_export_success,
    show_stats,
    get_confirm_delete,
    get_no_export_msg,
)


def _lang(idn: bool) -> str:
    """Return language code based on flag."""
    return "idn" if idn else "en"


@click.group()
@click.version_option(version=__version__, prog_name="devlog-cli")
def cli():
    """Track your daily dev progress from the terminal. / Catat progress harianmu dari terminal."""
    pass


@cli.command()
@click.argument("message")
@click.option("--tag", "-t", default=None, help="Tag for entry category")
def add(message: str, tag: str) -> None:
    """Add a new log entry."""
    entry = add_entry(message, tag)
    show_add_success(entry)


@cli.command()
@click.argument("message")
@click.option("--tag", "-t", default=None, help="Tag untuk kategori entri")
def tambah(message: str, tag: str) -> None:
    """Tambah entri log baru."""
    entry = add_entry(message, tag)
    show_add_success(entry)


@cli.command("list")
@click.option("--week", "-w", is_flag=True, help="Show this week's log")
@click.option("--all", "-a", "all_entries", is_flag=True, help="Show all logs")
@click.option("--tag", "-t", default=None, help="Filter by tag")
@click.option("-idn", is_flag=True, help="Tampilkan dalam Bahasa Indonesia")
def list_entries(week: bool, all_entries: bool, tag: str, idn: bool) -> None:
    """List log entries. Use -idn for Indonesian."""
    lang = _lang(idn)
    if tag:
        entries = get_entries_by_tag(tag)
        show_entry_table(entries, lang=lang, title_key="title_tag", tag_filter=tag)
    elif all_entries:
        entries = get_entries_all()
        show_entry_table(entries, lang=lang, title_key="title_all")
    elif week:
        entries = get_entries_week()
        show_entry_table(entries, lang=lang, title_key="title_week")
    else:
        entries = get_entries_today()
        show_entry_table(entries, lang=lang, title_key="title_today")


@cli.command()
@click.argument("entry_id", type=int)
def delete(entry_id: int) -> None:
    """Delete an entry by ID."""
    entry = get_entry_by_id(entry_id)
    if entry is None:
        show_entry_not_found(entry_id)
        return

    click.confirm(
        f'Are you sure you want to delete entry #{entry_id}? "{entry.message}"',
        abort=True,
    )
    delete_entry(entry_id)
    show_delete_success(entry_id)


@cli.command()
@click.argument("entry_id", type=int)
def hapus(entry_id: int) -> None:
    """Hapus entri berdasarkan ID."""
    entry = get_entry_by_id(entry_id)
    if entry is None:
        show_entry_not_found(entry_id, lang="idn")
        return

    click.confirm(
        f'Yakin ingin menghapus entri #{entry_id}? "{entry.message}"',
        abort=True,
    )
    delete_entry(entry_id)
    show_delete_success(entry_id, lang="idn")


@cli.command()
@click.option("--period", "-p", type=click.Choice(["day", "week"]),
              default="day", help="Export period: day or week")
@click.option("--output", "-o", default=None, help="Output filename")
@click.option("-idn", is_flag=True, help="Tampilkan dalam Bahasa Indonesia")
def export(period: str, output: str, idn: bool) -> None:
    """Export logs to a Markdown file. Use -idn for Indonesian."""
    lang = _lang(idn)

    if period == "week":
        entries = get_entries_week()
    else:
        entries = get_entries_today()

    if not entries:
        click.echo(get_no_export_msg(lang))
        return

    if output is None:
        today = datetime.now().strftime("%Y-%m-%d")
        output = f"devlog-{today}.md"

    period_label = period.title()
    content = _generate_markdown(entries, period_label)
    with open(output, "w", encoding="utf-8") as f:
        f.write(content)

    show_export_success(output, len(entries), lang=lang)


@cli.command()
@click.option("-idn", is_flag=True, help="Tampilkan dalam Bahasa Indonesia")
def stats(idn: bool) -> None:
    """Show dev log statistics. Use -idn for Indonesian."""
    show_stats(get_stats(), lang=_lang(idn))


@cli.command()
@click.option("-idn", is_flag=True, help="Tampilkan dalam Bahasa Indonesia")
def statistik(idn: bool) -> None:
    """Tampilkan statistik dev log. Gunakan -idn untuk Bahasa Indonesia."""
    show_stats(get_stats(), lang=_lang(idn))


def _generate_markdown(entries, period_label: str) -> str:
    """Generate markdown content from entries.

    Args:
        entries: List of Entry objects.
        period_label: Label for the time period.

    Returns:
        Markdown formatted string.
    """
    lines = [f"# DevLog — {period_label}\n"]
    for entry in entries:
        tag_str = f" [{entry.tag}]" if entry.tag else ""
        waktu = entry.created_at if entry.created_at else ""
        lines.append(f"- **{waktu}**{tag_str}: {entry.message}")
    lines.append("")
    return "\n".join(lines)

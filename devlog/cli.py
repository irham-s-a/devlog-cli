"""CLI commands for devlog using Click."""

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
)


@click.group()
@click.version_option(version=__version__, prog_name="devlog-cli")
def cli():
    """Catat progress harianmu langsung dari terminal."""
    pass


@cli.command()
@click.argument("message")
@click.option("--tag", "-t", default=None, help="Tag untuk kategori entri")
def tambah(message: str, tag: str) -> None:
    """Tambah entri log baru."""
    entry = add_entry(message, tag)
    show_add_success(entry)


@cli.command("list")
@click.option("--minggu", "-m", is_flag=True, help="Tampilkan log minggu ini")
@click.option("--semua", "-s", is_flag=True, help="Tampilkan semua log")
@click.option("--tag", "-t", default=None, help="Filter berdasarkan tag")
def list_entries(minggu: bool, semua: bool, tag: str) -> None:
    """Tampilkan daftar log."""
    if tag:
        entries = get_entries_by_tag(tag)
        show_entry_table(entries, title=f"📋 Log — Tag: {tag}")
    elif semua:
        entries = get_entries_all()
        show_entry_table(entries, title="📋 Semua Log")
    elif minggu:
        entries = get_entries_week()
        show_entry_table(entries, title="📋 Log Minggu Ini")
    else:
        entries = get_entries_today()
        show_entry_table(entries, title="📋 Log Hari Ini")


@cli.command()
@click.argument("entry_id", type=int)
def hapus(entry_id: int) -> None:
    """Hapus entri berdasarkan ID."""
    entry = get_entry_by_id(entry_id)
    if entry is None:
        show_entry_not_found(entry_id)
        return

    click.confirm(
        f"Yakin ingin menghapus entri #{entry_id}? "
        f'"{entry.message}"',
        abort=True,
    )
    delete_entry(entry_id)
    show_delete_success(entry_id)


@cli.command()
@click.option("--periode", "-p", type=click.Choice(["hari", "minggu"]), default="hari",
              help="Periode export (hari/minggu)")
@click.option("--output", "-o", default=None, help="Nama file output")
def export(periode: str, output: str) -> None:
    """Export log ke file Markdown."""
    if periode == "minggu":
        entries = get_entries_week()
        period_label = "minggu ini"
    else:
        entries = get_entries_today()
        period_label = "hari ini"

    if not entries:
        click.echo("Tidak ada entri untuk diekspor.")
        return

    if output is None:
        today = datetime.now().strftime("%Y-%m-%d")
        output = f"devlog-{today}.md"

    content = _generate_markdown(entries, period_label)
    with open(output, "w", encoding="utf-8") as f:
        f.write(content)

    show_export_success(output, len(entries))


@cli.command()
def statistik() -> None:
    """Tampilkan statistik dev log."""
    stats = get_stats()
    show_stats(stats)


def _generate_markdown(entries, period_label: str) -> str:
    """Generate markdown content from entries.

    Args:
        entries: List of Entry objects.
        period_label: Label for the time period.

    Returns:
        Markdown formatted string.
    """
    lines = [f"# DevLog — {period_label.title()}\n"]
    for entry in entries:
        tag_str = f" [{entry.tag}]" if entry.tag else ""
        waktu = entry.created_at if entry.created_at else ""
        lines.append(f"- **{waktu}**{tag_str}: {entry.message}")
    lines.append("")
    return "\n".join(lines)

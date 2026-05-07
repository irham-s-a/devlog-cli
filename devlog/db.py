"""Database operations for devlog entries using SQLite."""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from .models import Entry

DEFAULT_DB_DIR = Path.home() / ".devlog"
DEFAULT_DB_PATH = DEFAULT_DB_DIR / "devlog.db"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS entries (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    message     TEXT NOT NULL,
    tag         TEXT DEFAULT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""


def _get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Return a connection to the SQLite database.

    Args:
        db_path: Path to the database file. If None, uses the default path.

    Returns:
        A sqlite3.Connection object.
    """
    if db_path is None:
        DEFAULT_DB_DIR.mkdir(parents=True, exist_ok=True)
        db_path = str(DEFAULT_DB_PATH)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute(CREATE_TABLE_SQL)
    conn.commit()
    return conn


def add_entry(message: str, tag: Optional[str] = None, db_path: Optional[str] = None) -> Entry:
    """Add a new entry to the database.

    Args:
        message: The log message.
        tag: Optional tag for categorization.
        db_path: Optional database file path.

    Returns:
        The created Entry object.
    """
    with _get_connection(db_path) as conn:
        cursor = conn.execute(
            "INSERT INTO entries (message, tag) VALUES (?, ?)",
            (message, tag),
        )
        entry_id = cursor.lastrowid
        row = conn.execute(
            "SELECT * FROM entries WHERE id = ?",
            (entry_id,),
        ).fetchone()
        return Entry(
            id=row["id"],
            message=row["message"],
            tag=row["tag"],
            created_at=row["created_at"],
        )


def get_entries_today(db_path: Optional[str] = None) -> list[Entry]:
    """Retrieve entries created today.

    Args:
        db_path: Optional database file path.

    Returns:
        List of Entry objects created today.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    with _get_connection(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM entries WHERE DATE(created_at) = ? ORDER BY created_at DESC",
            (today,),
        ).fetchall()
        return [_row_to_entry(row) for row in rows]


def get_entries_week(db_path: Optional[str] = None) -> list[Entry]:
    """Retrieve entries from the current week (last 7 days).

    Args:
        db_path: Optional database file path.

    Returns:
        List of Entry objects from this week.
    """
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    with _get_connection(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM entries WHERE DATE(created_at) >= ? ORDER BY created_at DESC",
            (week_ago,),
        ).fetchall()
        return [_row_to_entry(row) for row in rows]


def get_entries_all(db_path: Optional[str] = None) -> list[Entry]:
    """Retrieve all entries.

    Args:
        db_path: Optional database file path.

    Returns:
        List of all Entry objects.
    """
    with _get_connection(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM entries ORDER BY created_at DESC"
        ).fetchall()
        return [_row_to_entry(row) for row in rows]


def get_entries_by_tag(tag: str, db_path: Optional[str] = None) -> list[Entry]:
    """Retrieve entries filtered by tag.

    Args:
        tag: The tag to filter by.
        db_path: Optional database file path.

    Returns:
        List of Entry objects matching the tag.
    """
    with _get_connection(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM entries WHERE tag = ? ORDER BY created_at DESC",
            (tag,),
        ).fetchall()
        return [_row_to_entry(row) for row in rows]


def get_entry_by_id(entry_id: int, db_path: Optional[str] = None) -> Optional[Entry]:
    """Retrieve a single entry by its ID.

    Args:
        entry_id: The entry ID.
        db_path: Optional database file path.

    Returns:
        The Entry object if found, None otherwise.
    """
    with _get_connection(db_path) as conn:
        row = conn.execute(
            "SELECT * FROM entries WHERE id = ?",
            (entry_id,),
        ).fetchone()
        if row is None:
            return None
        return _row_to_entry(row)


def delete_entry(entry_id: int, db_path: Optional[str] = None) -> bool:
    """Delete an entry by its ID.

    Args:
        entry_id: The entry ID to delete.
        db_path: Optional database file path.

    Returns:
        True if the entry was deleted, False if not found.
    """
    with _get_connection(db_path) as conn:
        cursor = conn.execute(
            "DELETE FROM entries WHERE id = ?",
            (entry_id,),
        )
        return cursor.rowcount > 0


def get_stats(db_path: Optional[str] = None) -> dict:
    """Calculate statistics from the entries.

    Args:
        db_path: Optional database file path.

    Returns:
        Dictionary with keys: total_entries, week_entries, longest_streak, top_tags.
    """
    with _get_connection(db_path) as conn:
        total = conn.execute("SELECT COUNT(*) FROM entries").fetchone()[0]

        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        week_entries = conn.execute(
            "SELECT COUNT(*) FROM entries WHERE DATE(created_at) >= ?",
            (week_ago,),
        ).fetchone()[0]

        streak = _calculate_streak(conn)

        tag_rows = conn.execute(
            "SELECT tag, COUNT(*) as count FROM entries WHERE tag IS NOT NULL "
            "GROUP BY tag ORDER BY count DESC LIMIT 3"
        ).fetchall()
        top_tags = [(row["tag"], row["count"]) for row in tag_rows]

        return {
            "total_entries": total,
            "week_entries": week_entries,
            "longest_streak": streak,
            "top_tags": top_tags,
        }


def _calculate_streak(conn: sqlite3.Connection) -> int:
    """Calculate the longest streak of consecutive days with entries.

    Args:
        conn: Active database connection.

    Returns:
        The longest streak in days.
    """
    rows = conn.execute(
        "SELECT DISTINCT DATE(created_at) as day FROM entries ORDER BY day"
    ).fetchall()

    if not rows:
        return 0

    dates = [datetime.strptime(row["day"], "%Y-%m-%d").date() for row in rows]
    longest = 1
    current = 1

    for i in range(1, len(dates)):
        if dates[i] - dates[i - 1] == timedelta(days=1):
            current += 1
            longest = max(longest, current)
        else:
            current = 1

    return longest


def _row_to_entry(row: sqlite3.Row) -> Entry:
    """Convert a database row to an Entry object.

    Args:
        row: A sqlite3.Row object.

    Returns:
        An Entry instance.
    """
    return Entry(
        id=row["id"],
        message=row["message"],
        tag=row["tag"],
        created_at=row["created_at"],
    )

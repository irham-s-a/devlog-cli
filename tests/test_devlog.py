"""Tests for devlog database operations using in-memory SQLite."""

import pytest
from devlog.db import (
    add_entry,
    get_entries_today,
    get_entries_all,
    get_entries_by_tag,
    get_entry_by_id,
    delete_entry,
    get_stats,
    _get_connection,
)


@pytest.fixture
def db_path(tmp_path):
    """Provide a temporary database path for each test."""
    return str(tmp_path / "test.db")


def _init_db(db_path):
    """Initialize the database schema for testing."""
    conn = _get_connection(db_path)
    conn.close()


def test_add_entry(db_path):
    """Test that an entry is successfully created."""
    _init_db(db_path)
    entry = add_entry("Selesai modul auth", tag="feature", db_path=db_path)
    assert entry.id is not None
    assert entry.message == "Selesai modul auth"
    assert entry.tag == "feature"
    assert entry.created_at is not None


def test_add_entry_without_tag(db_path):
    """Test that an entry can be created without a tag."""
    _init_db(db_path)
    entry = add_entry("Log tanpa tag", db_path=db_path)
    assert entry.tag is None


def test_get_entries_today(db_path):
    """Test that only today's entries are returned."""
    _init_db(db_path)
    add_entry("Entri hari ini 1", db_path=db_path)
    add_entry("Entri hari ini 2", tag="bug", db_path=db_path)

    entries = get_entries_today(db_path=db_path)
    assert len(entries) == 2
    assert entries[0].message in ("Entri hari ini 1", "Entri hari ini 2")


def test_get_entries_all(db_path):
    """Test that all entries are returned."""
    _init_db(db_path)
    add_entry("Entri pertama", db_path=db_path)
    add_entry("Entri kedua", db_path=db_path)

    entries = get_entries_all(db_path=db_path)
    assert len(entries) == 2


def test_get_entries_by_tag(db_path):
    """Test filtering entries by tag."""
    _init_db(db_path)
    add_entry("Fix bug login", tag="bug", db_path=db_path)
    add_entry("Tambah fitur", tag="feature", db_path=db_path)
    add_entry("Fix crash", tag="bug", db_path=db_path)

    bug_entries = get_entries_by_tag("bug", db_path=db_path)
    assert len(bug_entries) == 2
    assert all(e.tag == "bug" for e in bug_entries)


def test_get_entry_by_id(db_path):
    """Test retrieving a single entry by ID."""
    _init_db(db_path)
    created = add_entry("Cari by ID", db_path=db_path)
    found = get_entry_by_id(created.id, db_path=db_path)
    assert found is not None
    assert found.message == "Cari by ID"


def test_get_entry_by_id_not_found(db_path):
    """Test that None is returned for a non-existent ID."""
    _init_db(db_path)
    found = get_entry_by_id(999, db_path=db_path)
    assert found is None


def test_delete_entry(db_path):
    """Test that an entry is correctly deleted."""
    _init_db(db_path)
    entry = add_entry("Akan dihapus", db_path=db_path)
    result = delete_entry(entry.id, db_path=db_path)
    assert result is True

    found = get_entry_by_id(entry.id, db_path=db_path)
    assert found is None


def test_delete_entry_not_found(db_path):
    """Test deleting a non-existent entry returns False."""
    _init_db(db_path)
    result = delete_entry(999, db_path=db_path)
    assert result is False


def test_get_stats(db_path):
    """Test that stats return the correct keys and values."""
    _init_db(db_path)
    add_entry("Entri 1", tag="bug", db_path=db_path)
    add_entry("Entri 2", tag="feature", db_path=db_path)
    add_entry("Entri 3", tag="bug", db_path=db_path)
    add_entry("Entri 4", db_path=db_path)

    stats = get_stats(db_path=db_path)
    assert "total_entries" in stats
    assert "week_entries" in stats
    assert "longest_streak" in stats
    assert "top_tags" in stats
    assert stats["total_entries"] == 4
    assert stats["week_entries"] == 4
    assert isinstance(stats["top_tags"], list)
    assert stats["top_tags"][0][0] == "bug"
    assert stats["top_tags"][0][1] == 2

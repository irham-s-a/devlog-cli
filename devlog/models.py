"""Data models for devlog entries."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Entry:
    """Represents a single dev log entry.

    Attributes:
        id: Unique identifier (auto-incremented by SQLite).
        message: The log message content.
        tag: Optional tag for categorization.
        created_at: Timestamp when the entry was created.
    """

    message: str
    tag: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[str] = None

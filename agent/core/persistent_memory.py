from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Dict, Optional


class PersistentMemory:
    """Simple key-value store backed by SQLite."""

    def __init__(self, db_path: str | Path = "memory.db") -> None:
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS memory (key TEXT PRIMARY KEY, value TEXT)"
        )
        self.conn.commit()

    def set(self, key: str, value: str) -> None:
        """Store ``value`` under ``key``."""
        with self.conn:
            self.conn.execute(
                "INSERT INTO memory(key, value) VALUES(?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (key, value),
            )

    def get(self, key: str) -> Optional[str]:
        """Return the value for ``key`` or ``None``."""
        cur = self.conn.execute("SELECT value FROM memory WHERE key=?", (key,))
        row = cur.fetchone()
        return row[0] if row else None

    def delete(self, key: str) -> None:
        """Remove ``key`` from the store."""
        with self.conn:
            self.conn.execute("DELETE FROM memory WHERE key=?", (key,))

    def all(self) -> Dict[str, str]:
        """Return all key-value pairs."""
        cur = self.conn.execute("SELECT key, value FROM memory")
        return {k: v for k, v in cur.fetchall()}

    def close(self) -> None:
        """Close the database connection."""
        self.conn.close()

    def __enter__(self) -> "PersistentMemory":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


__all__ = ["PersistentMemory"]

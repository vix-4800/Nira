from __future__ import annotations

from contextlib import contextmanager
from typing import List

from rich.console import Console


class StatusManager:
    """Handle displaying dynamic status messages."""

    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()
        self._status = None
        self._stack: List[str] = []

    def push(self, message: str) -> None:
        """Start or update the status message."""
        self._stack.append(message)
        if self._status is None:
            self._status = self.console.status(f"[cyan]{message}[/]", spinner="dots")
            self._status.start()
        else:
            self._status.update(f"[cyan]{message}[/]")

    def pop(self) -> None:
        """Revert to the previous status or clear."""
        if not self._stack:
            return
        self._stack.pop()
        if self._stack:
            if self._status:
                self._status.update(f"[cyan]{self._stack[-1]}[/]")
        else:
            self.stop()

    def stop(self) -> None:
        if self._status:
            self._status.stop()
            self._status = None

    @contextmanager
    def status(self, message: str):
        """Context manager to show a temporary status message."""
        self.push(message)
        try:
            yield
        finally:
            self.pop()


# Global manager and console to be reused across the project
console = Console()
status_manager = StatusManager(console)

__all__ = ["console", "status_manager"]

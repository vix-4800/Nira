import re
from pathlib import Path

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from ..env import get_obsidian_vault
from ..status import status_manager


def _vault_path() -> Path:
    vault = get_obsidian_vault()
    if not vault:
        raise RuntimeError("OBSIDIAN_VAULT not configured")
    return Path(vault)


def summarize_text(text: str, sentences: int = 3) -> str:
    parts = re.split(r"(?<=[.!?])\s+", text)
    return " ".join(parts[:sentences]).strip()


class ObsidianManagerInput(BaseModel):
    action: str = Field(..., description="create_note | summarize_note")
    title: str = Field(..., description="Note title")
    content: str | None = Field(None, description="Note content for 'create_note'")
    sentences: int = Field(3, description="Number of sentences for 'summarize_note'")


@tool("ObsidianManager", args_schema=ObsidianManagerInput)
def obsidian_manager(
    action: str,
    title: str,
    content: str | None = None,
    sentences: int = 3,
) -> str:
    """Unified tool for Obsidian vault operations."""
    match action:
        case "create_note":
            path = _vault_path() / f"{title}.md"
            if path.exists():
                return f"Note already exists: {path}"
            try:
                with status_manager.status("создаю заметку"):
                    path.write_text(content or "", encoding="utf-8")
                return f"Created {path}"
            except Exception as e:
                return f"Failed to create note: {e}"
        case "summarize_note":
            path = _vault_path() / f"{title}.md"
            if not path.is_file():
                return f"(File not found: {path})"
            try:
                with status_manager.status("читаю заметку"):
                    text = path.read_text(encoding="utf-8")
            except Exception as e:
                return f"Failed to read note: {e}"
            return summarize_text(text, sentences)
        case _:
            return f"Error: unknown action '{action}'"

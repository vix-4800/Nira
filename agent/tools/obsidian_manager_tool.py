from pathlib import Path

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from ..core.config import load_config
from ..core.metrics import track_tool
from ..core.status import status_manager
from .researcher.summarize_text_tool import summarize_text_tool


def _vault_path() -> Path:
    vault = load_config().obsidian_vault
    if not vault:
        raise RuntimeError("OBSIDIAN_VAULT not configured")
    return Path(vault)


class ObsidianManagerInput(BaseModel):
    action: str = Field(..., description="create_note | summarize_note")
    title: str = Field(..., description="Note title")
    content: str | None = Field(None, description="Note content for 'create_note'")
    sentences: int = Field(3, description="Number of sentences for 'summarize_note'")


@tool("ObsidianManager", args_schema=ObsidianManagerInput)
@track_tool
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
            return summarize_text_tool.func(text=text, sentences=sentences)  # type: ignore[attr-defined]
        case _:
            return f"Error: unknown action '{action}'"

from pydantic import BaseModel, Field
from langchain_core.tools import tool

from pathlib import Path
from ..env import get_obsidian_vault


def _vault_path() -> Path:
    vault = get_obsidian_vault()
    if not vault:
        raise RuntimeError("OBSIDIAN_VAULT not configured")
    return Path(vault)


def create_note(title: str, content: str = "") -> str:
    """Create a new markdown note in the Obsidian vault."""
    path = _vault_path() / f"{title}.md"
    if path.exists():
        return f"Note already exists: {path}"
    try:
        path.write_text(content, encoding="utf-8")
        return f"Created {path}"
    except Exception as e:
        return f"Failed to create note: {e}"

class CreateNoteInput(BaseModel):
    title: str = Field(..., description="Note title")
    content: str = Field(default="", description="Note content")

@tool("CreateNote", args_schema=CreateNoteInput)
def create_note_tool(title: str, content: str = "") -> str:
    """Create a new markdown note in the configured Obsidian vault."""
    return create_note(title, content)

from pydantic import BaseModel, Field
from langchain_core.tools import tool

from pathlib import Path
import re
from ..env import get_obsidian_vault


def _vault_path() -> Path:
    vault = get_obsidian_vault()
    if not vault:
        raise RuntimeError("OBSIDIAN_VAULT not configured")
    return Path(vault)


def summarize_text(text: str, sentences: int = 3) -> str:
    parts = re.split(r"(?<=[.!?])\s+", text)
    return " ".join(parts[:sentences]).strip()


def summarize_note(title: str, sentences: int = 3) -> str:
    path = _vault_path() / f"{title}.md"
    if not path.is_file():
        return f"(File not found: {path})"
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Failed to read note: {e}"
    return summarize_text(text, sentences)

class SummarizeNoteInput(BaseModel):
    title: str = Field(..., description="Note title")
    sentences: int = Field(default=3, description="Number of sentences")

@tool("SummarizeNote", args_schema=SummarizeNoteInput)
def summarize_note_tool(title: str, sentences: int = 3) -> str:
    """Summarize a markdown note from the Obsidian vault."""
    return summarize_note(title, sentences=sentences)

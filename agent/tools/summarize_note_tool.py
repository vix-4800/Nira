from pydantic import BaseModel, Field
from langchain_core.tools import tool

from .obsidian_tools import summarize_note

class SummarizeNoteInput(BaseModel):
    title: str = Field(..., description="Note title")
    sentences: int = Field(default=3, description="Number of sentences")

@tool("SummarizeNote", args_schema=SummarizeNoteInput)
def summarize_note_tool(title: str, sentences: int = 3) -> str:
    """Summarize a markdown note from the Obsidian vault."""
    return summarize_note(title, sentences=sentences)

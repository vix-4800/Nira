from pydantic import BaseModel, Field
from langchain_core.tools import tool

from .obsidian_tools import create_note

class CreateNoteInput(BaseModel):
    title: str = Field(..., description="Note title")
    content: str = Field(default="", description="Note content")

@tool("CreateNote", args_schema=CreateNoteInput)
def create_note_tool(title: str, content: str = "") -> str:
    """Create a new markdown note in the configured Obsidian vault."""
    return create_note(title, content)

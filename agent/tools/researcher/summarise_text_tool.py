import re

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from ...core.metrics import track_tool


class SummariseTextInput(BaseModel):
    text: str = Field(..., description="Text to summarise")
    sentences: int = Field(default=3, description="Number of sentences")


@tool("SummariseText", args_schema=SummariseTextInput)
@track_tool
def summarise_text_tool(text: str, sentences: int = 3) -> str:
    """Return a short summary of the provided text."""
    parts = re.split(r"(?<=[.!?])\s+", text)
    return " ".join(parts[:sentences]).strip()

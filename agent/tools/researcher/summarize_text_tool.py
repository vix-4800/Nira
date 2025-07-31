import re

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from ...core.metrics import track_tool


class SummarizeTextInput(BaseModel):
    text: str = Field(..., description="Text to summarize")
    sentences: int = Field(default=3, description="Number of sentences")


@tool("SummarizeText", args_schema=SummarizeTextInput)
@track_tool
def summarize_text_tool(text: str, sentences: int = 3) -> str:
    """Return a short summary of the provided text."""
    parts = re.split(r"(?<=[.!?])\s+", text)
    return " ".join(parts[:sentences]).strip()

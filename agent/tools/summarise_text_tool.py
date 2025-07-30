import re

from langchain_core.tools import tool
from pydantic import BaseModel, Field


def summarise_text(text: str, sentences: int = 3) -> str:
    parts = re.split(r"(?<=[.!?])\s+", text)
    return " ".join(parts[:sentences]).strip()


class SummariseTextInput(BaseModel):
    text: str = Field(..., description="Text to summarise")
    sentences: int = Field(default=3, description="Number of sentences")


@tool("SummariseText", args_schema=SummariseTextInput)
def summarise_text_tool(text: str, sentences: int = 3) -> str:
    """Return a short summary of the provided text."""
    return summarise_text(text, sentences)

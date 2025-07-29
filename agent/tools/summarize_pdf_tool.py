import re

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from .extract_text_from_pdf_tool import extract_text_from_pdf_tool


def summarize_text(text: str, sentences: int = 3) -> str:
    parts = re.split(r"(?<=[.!?])\s+", text)
    return " ".join(parts[:sentences]).strip()


class SummarizePDFInput(BaseModel):
    path: str = Field(..., description="Path to the PDF file")
    sentences: int = Field(default=3, description="Number of sentences")


@tool("SummarizePDF", args_schema=SummarizePDFInput)
def summarize_pdf_tool(path: str, sentences: int = 3) -> str:
    """Provide a short summary of a PDF document."""
    text = extract_text_from_pdf_tool(path)
    if text.startswith("(File not found"):
        return text
    return summarize_text(text, sentences)

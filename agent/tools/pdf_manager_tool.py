import os
import re
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from PyPDF2 import PdfReader

MAX_PAGES = 30
MAX_CHARS = 30_000


def summarize_text(text: str, sentences: int = 3) -> str:
    parts = re.split(r"(?<=[.!?])\s+", text)
    return " ".join(parts[:sentences]).strip()


class PDFManagerInput(BaseModel):
    action: str = Field(..., description="extract_text | summarize")
    path: str = Field(..., description="Path to the PDF file")
    max_pages: int = Field(default=30, description="Maximum pages to read")
    sentences: int = Field(default=3, description="Number of sentences for summarize")


@tool("PDFManager", args_schema=PDFManagerInput)
def pdf_manager(
    action: str,
    path: str,
    max_pages: int = 30,
    sentences: int = 3,
) -> str:
    """Unified tool for PDF operations."""
    if not os.path.isfile(path):
        return f"(File not found: {path})"

    reader = PdfReader(path)
    pages = reader.pages[:max_pages]
    text = []
    for p in pages:
        text.append(p.extract_text() or "")
    joined = "\n".join(text).strip()[:MAX_CHARS]

    match action:
        case "extract_text":
            return joined
        case "summarize":
            return summarize_text(joined, sentences)
        case _:
            return f"Error: unknown action '{action}'"

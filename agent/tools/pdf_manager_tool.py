from pathlib import Path

from langchain_core.tools import tool
from pydantic import BaseModel, Field
from PyPDF2 import PdfReader

from ..core.constants import MAX_PDF_CHARS
from ..core.metrics import track_tool
from ..core.status import status_manager
from .researcher.summarize_text_tool import summarize_text_tool


class PDFManagerInput(BaseModel):
    action: str = Field(..., description="extract_text | summarize")
    path: str = Field(..., description="Path to the PDF file")
    max_pages: int = Field(default=30, description="Maximum pages to read")
    sentences: int = Field(default=3, description="Number of sentences for summarize")


@tool("PDFManager", args_schema=PDFManagerInput)
@track_tool
def pdf_manager(
    action: str,
    path: str,
    max_pages: int = 30,
    sentences: int = 3,
) -> str:
    """Unified tool for PDF operations."""
    file_path = Path(path)
    if not file_path.is_file():
        return f"(File not found: {path})"
    with status_manager.status("читаю PDF"):
        reader = PdfReader(file_path)
        pages = reader.pages[:max_pages]
        text = []
        for p in pages:
            text.append(p.extract_text() or "")
        joined = "\n".join(text).strip()[:MAX_PDF_CHARS]

    match action:
        case "extract_text":
            return joined
        case "summarize":
            return summarize_text_tool.func(text=joined, sentences=sentences)
        case _:
            return f"Error: unknown action '{action}'"

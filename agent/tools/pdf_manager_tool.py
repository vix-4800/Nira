from pathlib import Path

from langchain_core.tools import tool
from pydantic import BaseModel, Field
from PyPDF2 import PdfReader

from ..constants import MAX_PDF_CHARS
from ..metrics import track_tool
from ..status import status_manager
from .summarise_text_tool import summarise_text_tool

MAX_PAGES = 30


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
        reader = PdfReader(str(file_path))
        pages = reader.pages[:max_pages]
        text = []
        for p in pages:
            text.append(p.extract_text() or "")
        joined = "\n".join(text).strip()[:MAX_PDF_CHARS]

    match action:
        case "extract_text":
            return joined
        case "summarize":
            return summarise_text_tool.func(text=joined, sentences=sentences)
        case _:
            return f"Error: unknown action '{action}'"

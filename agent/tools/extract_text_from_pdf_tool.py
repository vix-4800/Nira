import os

from langchain_core.tools import tool
from pydantic import BaseModel, Field
from PyPDF2 import PdfReader

MAX_PAGES = 30
MAX_CHARS = 30_000


def extract_text_from_pdf(path: str, max_pages: int = MAX_PAGES) -> str:
    if not os.path.isfile(path):
        return f"(File not found: {path})"
    reader = PdfReader(path)
    pages = reader.pages[:max_pages]
    text = []
    for p in pages:
        page_text = p.extract_text() or ""
        text.append(page_text)
    joined = "\n".join(text).strip()
    return joined[:MAX_CHARS]


class PDFPathInput(BaseModel):
    path: str = Field(..., description="Path to the PDF file")
    max_pages: int = Field(default=30, description="Maximum pages to read")


@tool("ExtractTextFromPDF", args_schema=PDFPathInput)
def extract_text_from_pdf_tool(path: str, max_pages: int = 30) -> str:
    """Extract the textual contents from a PDF file."""
    return extract_text_from_pdf(path, max_pages=max_pages)

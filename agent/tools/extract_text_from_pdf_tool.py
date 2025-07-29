from pydantic import BaseModel, Field
from langchain_core.tools import tool

from .pdf_tools import extract_text_from_pdf

class PDFPathInput(BaseModel):
    path: str = Field(..., description="Path to the PDF file")
    max_pages: int = Field(default=30, description="Maximum pages to read")

@tool("ExtractTextFromPDF", args_schema=PDFPathInput)
def extract_text_from_pdf_tool(path: str, max_pages: int = 30) -> str:
    """Extract the textual contents from a PDF file."""
    return extract_text_from_pdf(path, max_pages=max_pages)

from pydantic import BaseModel, Field
from langchain_core.tools import tool

from .pdf_tools import summarize_pdf

class SummarizePDFInput(BaseModel):
    path: str = Field(..., description="Path to the PDF file")
    sentences: int = Field(default=3, description="Number of sentences")

@tool("SummarizePDF", args_schema=SummarizePDFInput)
def summarize_pdf_tool(path: str, sentences: int = 3) -> str:
    """Provide a short summary of a PDF document."""
    return summarize_pdf(path, sentences=sentences)

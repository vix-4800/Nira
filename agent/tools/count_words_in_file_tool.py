from pydantic import BaseModel, Field
from langchain_core.tools import tool

from .pdf_tools import count_words_in_file

class CountWordsInput(BaseModel):
    path: str = Field(..., description="Path to the text file")

@tool("CountWordsInFile", args_schema=CountWordsInput)
def count_words_in_file_tool(path: str) -> str:
    """Return the number of words in a text file."""
    return count_words_in_file(path)

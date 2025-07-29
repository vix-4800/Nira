from langchain_core.tools import tool
from pydantic import BaseModel, Field


class CountWordsInput(BaseModel):
    path: str = Field(..., description="Path to the text file")


@tool("CountWordsInFile", args_schema=CountWordsInput)
def count_words_in_file_tool(path: str) -> str:
    """Return the number of words in a text file."""
    with open(path, "r", encoding="utf-8") as fh:
        words = fh.read().split()
    return str(len(words))

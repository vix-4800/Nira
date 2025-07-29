from pydantic import BaseModel, Field
from langchain_core.tools import tool

from .file_tools import find_file

class FindFileInput(BaseModel):
    pattern: str = Field(..., description="Filename or glob pattern")
    root: str = Field(default=".", description="Root search directory")

@tool("FindFile", args_schema=FindFileInput)
def find_file_tool(pattern: str, root: str = ".") -> list[str]:
    """Recursively search for files by name or glob pattern and return absolute paths."""
    return find_file(pattern, root)

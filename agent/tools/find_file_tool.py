import glob
import os

from langchain_core.tools import tool
from pydantic import BaseModel, Field


def find_file(pattern: str, root: str = ".") -> list[str]:
    """Recursively search for files matching the pattern under 'root'."""
    matches = glob.glob(os.path.join(root, "**", pattern), recursive=True)
    return [os.path.abspath(p) for p in matches]


class FindFileInput(BaseModel):
    pattern: str = Field(..., description="Filename or glob pattern")
    root: str = Field(default=".", description="Root search directory")


@tool("FindFile", args_schema=FindFileInput)
def find_file_tool(pattern: str, root: str = ".") -> list[str]:
    """Recursively search for files by name or glob pattern and return absolute paths."""
    return find_file(pattern, root)

from pathlib import Path
from typing import List

from langchain_core.tools import tool
from pydantic import BaseModel, Field, NonNegativeInt

from ..metrics import track_tool
from ..status import status_manager


class FileManagerInput(BaseModel):
    action: str = Field(..., description="find | read | count_words | write")
    pattern: str | None = Field(None, description="Filename/glob for 'find'")
    path: str | None = Field(
        None, description="Exact file path for 'read' / 'count_words' / 'write'"
    )
    text: str | None = Field(None, description="Text content for 'write'")
    append: bool = Field(False, description="Append to file for 'write'")
    root: str = Field(".", description="Root dir for 'find'")
    max_bytes: NonNegativeInt = Field(20_000, description="Limit read size (bytes)")


@tool("FileManager", args_schema=FileManagerInput)
@track_tool
def file_manager(
    action: str,
    pattern: str | None = None,
    path: str | None = None,
    text: str | None = None,
    append: bool = False,
    root: str = ".",
    max_bytes: int = 20_000,
) -> str | List[str]:
    """Unified tool for file operations: find, read, count words, or write."""

    match action:
        case "find":
            if not pattern:
                return "Error: 'pattern' is required for find"
            root_path = Path(root)
            glob_pattern = pattern if "**" in pattern else f"**/{pattern}"
            with status_manager.status("ищу файлы"):
                matches = list(root_path.glob(glob_pattern))
            return [str(p.resolve()) for p in matches]
        case "read":
            if not path:
                return "Error: 'path' is required for read"
            file_path = Path(path)
            try:
                with status_manager.status("читаю файл"):
                    return file_path.read_text(encoding="utf-8")[:max_bytes]
            except Exception as exc:
                return f"Error reading file: {exc}"
        case "count_words":
            if not path:
                return "Error: 'path' is required for count_words"
            file_path = Path(path)
            try:
                with status_manager.status("считаю слова"):
                    words = file_path.read_text(encoding="utf-8").split()
                return str(len(words))
            except Exception as exc:
                return f"Error reading file: {exc}"
        case "write":
            if not path:
                return "Error: 'path' is required for write"
            if text is None:
                return "Error: 'text' is required for write"
            file_path = Path(path)
            try:
                file_path.parent.mkdir(parents=True, exist_ok=True)
                mode = "a" if append else "w"
                with status_manager.status("записываю файл"):
                    with file_path.open(mode, encoding="utf-8") as f:
                        f.write(text)
                return f"Wrote to {file_path}"
            except Exception as exc:
                return f"Error writing file: {exc}"
        case _:
            return f"Error: unknown action '{action}'"

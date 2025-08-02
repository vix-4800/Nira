from __future__ import annotations

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from ..core.metrics import track_tool
from ..core.persistent_memory import PersistentMemory
from ..core.status import status_manager


class MemoryManagerInput(BaseModel):
    action: str = Field(..., description="get | set | delete | list")
    key: str | None = Field(None, description="Key for get/set/delete")
    value: str | None = Field(None, description="Value for set")


@tool("MemoryManager", args_schema=MemoryManagerInput)
@track_tool
def memory_manager(
    action: str,
    key: str | None = None,
    value: str | None = None,
) -> str | dict:
    """Manage persistent key-value memory."""
    mem = PersistentMemory()
    match action:
        case "get":
            if not key:
                return "Error: 'key' is required for get"
            val = mem.get(key)
            return val if val is not None else "(not found)"
        case "set":
            if not key or value is None:
                return "Error: 'key' and 'value' are required for set"
            with status_manager.status("сохраняю память"):
                mem.set(key, value)
            return "Saved"
        case "delete":
            if not key:
                return "Error: 'key' is required for delete"
            with status_manager.status("удаляю запись"):
                mem.delete(key)
            return "Deleted"
        case "list":
            return mem.all()
        case _:
            return f"Error: unknown action '{action}'"

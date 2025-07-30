import requests
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from ..env import get_todoist_token
from ..metrics import track_tool
from ..status import status_manager


class TodoistManagerInput(BaseModel):
    action: str = Field(..., description="list_tasks | get_task | create_task | complete_task")
    task_id: str | None = Field(None, description="ID for get_task/complete_task")
    content: str | None = Field(None, description="Task content for create_task")


_BASE_URL = "https://api.todoist.com/rest/v2"


@tool("TodoistManager", args_schema=TodoistManagerInput)
@track_tool
def todoist_manager(action: str, task_id: str | None = None, content: str | None = None) -> dict | list | str:
    """Unified tool for Todoist operations."""
    token = get_todoist_token()
    if not token:
        return "TODOIST_TOKEN not configured."
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    match action:
        case "list_tasks":
            url = f"{_BASE_URL}/tasks"
            try:
                with status_manager.status("получаю список задач"):
                    resp = requests.get(url, headers=headers, timeout=10)
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                return f"Failed to fetch tasks: {e}"
        case "get_task":
            if not task_id:
                return "Error: 'task_id' is required for get_task"
            url = f"{_BASE_URL}/tasks/{task_id}"
            try:
                with status_manager.status("получаю задачу"):
                    resp = requests.get(url, headers=headers, timeout=10)
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                return f"Failed to fetch task: {e}"
        case "create_task":
            if not content:
                return "Error: 'content' is required for create_task"
            url = f"{_BASE_URL}/tasks"
            try:
                with status_manager.status("создаю задачу"):
                    resp = requests.post(url, headers=headers, json={"content": content}, timeout=10)
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                return f"Failed to create task: {e}"
        case "complete_task":
            if not task_id:
                return "Error: 'task_id' is required for complete_task"
            url = f"{_BASE_URL}/tasks/{task_id}/close"
            try:
                with status_manager.status("завершаю задачу"):
                    resp = requests.post(url, headers=headers, timeout=10)
                resp.raise_for_status()
                return "Task completed."
            except Exception as e:
                return f"Failed to complete task: {e}"
        case _:
            return f"Error: unknown action '{action}'"

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from ..core.config import load_config
from ..core.metrics import track_tool
from .http_utils import request_json


class TodoistManagerInput(BaseModel):
    action: str = Field(
        ..., description="list_tasks | get_task | create_task | complete_task"
    )
    task_id: str | None = Field(None, description="ID for get_task/complete_task")
    content: str | None = Field(None, description="Task content for create_task")


_BASE_URL = "https://api.todoist.com/rest/v2"


@tool("TodoistManager", args_schema=TodoistManagerInput)
@track_tool
def todoist_manager(
    action: str, task_id: str | None = None, content: str | None = None
) -> dict | list | str:
    """Unified tool for Todoist operations."""
    token = load_config().todoist_token
    if not token:
        return "TODOIST_TOKEN not configured."
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    match action:
        case "list_tasks":
            url = f"{_BASE_URL}/tasks"
            return request_json(
                "get",
                url,
                headers=headers,
                status_msg="получаю список задач",
                error_msg="Failed to fetch tasks",
            )
        case "get_task":
            if not task_id:
                return "Error: 'task_id' is required for get_task"
            url = f"{_BASE_URL}/tasks/{task_id}"
            return request_json(
                "get",
                url,
                headers=headers,
                status_msg="получаю задачу",
                error_msg="Failed to fetch task",
            )
        case "create_task":
            if not content:
                return "Error: 'content' is required for create_task"
            url = f"{_BASE_URL}/tasks"
            return request_json(
                "post",
                url,
                headers=headers,
                json={"content": content},
                status_msg="создаю задачу",
                error_msg="Failed to create task",
            )
        case "complete_task":
            if not task_id:
                return "Error: 'task_id' is required for complete_task"
            url = f"{_BASE_URL}/tasks/{task_id}/close"
            result = request_json(
                "post",
                url,
                headers=headers,
                status_msg="завершаю задачу",
                error_msg="Failed to complete task",
            )
            if isinstance(result, str):
                return result
            return "Task completed."
        case _:
            return f"Error: unknown action '{action}'"

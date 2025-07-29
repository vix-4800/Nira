import requests
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from ..env import get_github_token
from ..status import status_manager


class GitHubManagerInput(BaseModel):
    action: str = Field(..., description="repo_info")
    repo: str | None = Field(None, description="Repository in owner/name format")


@tool("GitHubManager", args_schema=GitHubManagerInput)
def github_manager(action: str, repo: str | None = None) -> dict | str:
    """Unified tool for GitHub operations."""
    match action:
        case "repo_info":
            if not repo:
                return "Error: 'repo' is required for repo_info"
            token = get_github_token()
            headers = {"Authorization": f"token {token}"} if token else {}
            url = f"https://api.github.com/repos/{repo}"
            try:
                with status_manager.status("получаю данные репозитория"):
                    resp = requests.get(url, headers=headers, timeout=10)
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                return f"Failed to fetch repo info: {e}"
        case _:
            return f"Error: unknown action '{action}'"

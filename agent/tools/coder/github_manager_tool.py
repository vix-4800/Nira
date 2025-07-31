from langchain_core.tools import tool
from pydantic import BaseModel, Field

from ...core.config import load_config
from ...core.metrics import track_tool
from ..http_utils import request_json


class GitHubManagerInput(BaseModel):
    action: str = Field(
        ...,
        description="repo_info | create_repo | create_issue | create_pr",
    )
    repo: str | None = Field(None, description="Repository in owner/name format")
    title: str | None = Field(None, description="Title for issue/PR")
    body: str | None = Field(None, description="Body for issue/PR")
    head: str | None = Field(None, description="Source branch for PR")
    base: str | None = Field(None, description="Target branch for PR")


@tool("GitHubManager", args_schema=GitHubManagerInput)
@track_tool
def github_manager(
    action: str,
    repo: str | None = None,
    title: str | None = None,
    body: str | None = None,
    head: str | None = None,
    base: str | None = None,
) -> dict | str:
    """Unified tool for GitHub operations."""
    match action:
        case "repo_info":
            if not repo:
                return "Error: 'repo' is required for repo_info"
            token = load_config().github_token
            headers = {"Authorization": f"token {token}"} if token else {}
            url = f"https://api.github.com/repos/{repo}"
            return request_json(
                "get",
                url,
                headers=headers,
                status_msg="получаю данные репозитория",
                error_msg="Failed to fetch repo info",
            )
        case "create_repo":
            token = load_config().github_token
            if not token:
                return "GITHUB_TOKEN not configured."
            if not repo:
                return "Error: 'repo' is required for create_repo"
            headers = {"Authorization": f"token {token}"}
            url = "https://api.github.com/user/repos"
            return request_json(
                "post",
                url,
                headers=headers,
                json={"name": repo},
                status_msg="создаю репозиторий",
                error_msg="Failed to create repo",
            )
        case "create_issue":
            token = load_config().github_token
            if not token:
                return "GITHUB_TOKEN not configured."
            if not repo:
                return "Error: 'repo' is required for create_issue"
            if not title:
                return "Error: 'title' is required for create_issue"
            headers = {"Authorization": f"token {token}"}
            url = f"https://api.github.com/repos/{repo}/issues"
            payload = {"title": title}
            if body:
                payload["body"] = body
            return request_json(
                "post",
                url,
                headers=headers,
                json=payload,
                status_msg="создаю issue",
                error_msg="Failed to create issue",
            )
        case "create_pr":
            token = load_config().github_token
            if not token:
                return "GITHUB_TOKEN not configured."
            if not repo or not title or not head or not base:
                return "Error: 'repo', 'title', 'head' and 'base' are required for create_pr"
            headers = {"Authorization": f"token {token}"}
            url = f"https://api.github.com/repos/{repo}/pulls"
            payload = {"title": title, "head": head, "base": base}
            if body:
                payload["body"] = body
            return request_json(
                "post",
                url,
                headers=headers,
                json=payload,
                status_msg="создаю pull request",
                error_msg="Failed to create pr",
            )
        case _:
            return f"Error: unknown action '{action}'"

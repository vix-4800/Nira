import requests
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from ..env import get_github_token


def get_repo_info(repo: str) -> str:
    """Return basic information about a GitHub repository."""
    token = get_github_token()
    headers = {"Authorization": f"token {token}"} if token else {}
    url = f"https://api.github.com/repos/{repo}"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        full_name = data.get("full_name", repo)
        stars = data.get("stargazers_count", 0)
        forks = data.get("forks_count", 0)
        return f"{full_name}: ⭐{stars} forks:{forks}"
    except Exception as e:
        return f"Failed to fetch repo info: {e}"


class RepoInfoInput(BaseModel):
    repo: str = Field(..., description="Repository in owner/name format")


@tool("GetGitHubRepoInfo", args_schema=RepoInfoInput)
def get_repo_info_tool(repo: str) -> str:
    """Retrieve basic information about a GitHub repository."""
    return get_repo_info(repo)

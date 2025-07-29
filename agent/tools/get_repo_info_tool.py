from pydantic import BaseModel, Field
from langchain_core.tools import tool

from .github_tool import get_repo_info

class RepoInfoInput(BaseModel):
    repo: str = Field(..., description="Repository in owner/name format")

@tool("GetGitHubRepoInfo", args_schema=RepoInfoInput)
def get_repo_info_tool(repo: str) -> str:
    """Retrieve basic information about a GitHub repository."""
    return get_repo_info(repo)

import requests
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from ...core.metrics import track_tool


class CheckWebsiteInput(BaseModel):
    url: str = Field(..., description="Website URL")


@tool("CheckWebsite", args_schema=CheckWebsiteInput)
@track_tool
def check_website_tool(url: str) -> str:
    """Check if a website is reachable and return HTTP status code."""
    try:
        resp = requests.head(url, timeout=5)
        return f"{resp.status_code}"
    except Exception as e:
        return f"Error: {e}"

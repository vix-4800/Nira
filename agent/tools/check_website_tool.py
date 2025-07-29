import requests
from langchain_core.tools import tool
from pydantic import BaseModel, Field


def check_website(url: str) -> str:
    """Return HTTP status code for a website or an error message."""
    try:
        resp = requests.head(url, timeout=5)
        return f"{resp.status_code}"
    except Exception as e:
        return f"Error: {e}"


class CheckWebsiteInput(BaseModel):
    url: str = Field(..., description="Website URL")


@tool("CheckWebsite", args_schema=CheckWebsiteInput)
def check_website_tool(url: str) -> str:
    """Check if a website is reachable and return HTTP status code."""
    return check_website(url)

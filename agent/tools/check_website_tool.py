from pydantic import BaseModel, Field
from langchain_core.tools import tool

from .network_tools import check_website

class CheckWebsiteInput(BaseModel):
    url: str = Field(..., description="Website URL")

@tool("CheckWebsite", args_schema=CheckWebsiteInput)
def check_website_tool(url: str) -> str:
    """Check if a website is reachable and return HTTP status code."""
    return check_website(url)

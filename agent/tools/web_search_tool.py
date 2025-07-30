from ddgs import DDGS
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from ..metrics import track_tool
from ..status import status_manager


class WebSearchInput(BaseModel):
    query: str = Field(..., description="Search query")
    max_results: int = Field(default=5, description="Maximum number of results")


@tool("WebSearch", args_schema=WebSearchInput)
@track_tool
def web_search_tool(query: str, max_results: int = 5) -> str:
    """Search the web using DuckDuckGo and return top results."""
    try:
        with status_manager.status("ищу в интернете"):
            with DDGS() as ddgs:
                results = ddgs.text(query, safesearch="off", max_results=max_results)
    except Exception as e:
        return f"Search failed: {e}"

    if not results:
        return "(No results)"

    lines = []
    for r in results:
        title = r.get("title", "No title")
        url = r.get("href", "")
        lines.append(f"{title} - {url}".strip())
    return "\n".join(lines)

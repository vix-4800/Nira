import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from ..metrics import track_tool
from ..status import status_manager
from ..constants import MAX_TEXT_CHARS


def fetch_text_from_url(url: str, max_chars: int = MAX_TEXT_CHARS) -> str:
    """Fetch plain text content from a website URL."""
    try:
        with status_manager.status("читаю страницу"):
            resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        return f"Failed to fetch page: {e}"

    soup = BeautifulSoup(resp.text, "html.parser")
    # Remove script and style elements
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return text[:max_chars]


class ScrapeURLInput(BaseModel):
    url: str = Field(..., description="Website URL")


@tool("ScrapeURL", args_schema=ScrapeURLInput)
@track_tool
def scrape_url_tool(url: str) -> str:
    """Fetch and return textual content from a website."""
    return fetch_text_from_url(url)

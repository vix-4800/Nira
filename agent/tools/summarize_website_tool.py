import re
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from pydantic import BaseModel, Field


MAX_CHARS = 20000


def fetch_text_from_url(url: str, max_chars: int = MAX_CHARS) -> str:
    """Fetch text content from a website URL."""
    try:
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


def summarize_text(text: str, sentences: int = 3) -> str:
    parts = re.split(r"(?<=[.!?])\s+", text)
    return " ".join(parts[:sentences]).strip()




class SummarizeWebsiteInput(BaseModel):
    url: str = Field(..., description="Website URL")
    sentences: int = Field(default=3, description="Number of sentences")


@tool("SummarizeWebsite", args_schema=SummarizeWebsiteInput)
def summarize_website_tool(url: str, sentences: int = 3) -> str:
    """Provide a short summary of the textual content of a website."""
    text = fetch_text_from_url(url)
    if text.startswith("Failed to fetch"):
        return text
    return summarize_text(text, sentences)

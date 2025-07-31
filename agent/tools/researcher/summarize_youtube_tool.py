import re
from urllib.parse import parse_qs, urlparse

from langchain_core.tools import tool
from pydantic import BaseModel, Field
from youtube_transcript_api import YouTubeTranscriptApi

from ...core.constants import MAX_TEXT_CHARS
from ...core.metrics import track_tool
from ...core.status import status_manager
from .summarize_text_tool import summarize_text_tool


def extract_video_id(url_or_id: str) -> str:
    """Extract the video ID from a YouTube URL or return the ID."""
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url_or_id):
        return url_or_id
    parsed = urlparse(url_or_id)
    if parsed.hostname == "youtu.be":
        return parsed.path.lstrip("/")
    if parsed.hostname and "youtube" in parsed.hostname:
        qs = parse_qs(parsed.query)
        vid = qs.get("v", [""])[0]
        if vid:
            return vid
    return ""


def fetch_captions(video_id: str, languages: list[str] | None = None) -> str:
    """Fetch auto-generated captions text for a YouTube video."""
    languages = languages or ["en"]
    try:
        api = YouTubeTranscriptApi()
        parts = api.fetch(video_id, languages=languages)
    except Exception as e:
        return f"Failed to fetch transcript: {e}"
    text_parts = []
    for p in parts:
        if isinstance(p, dict):
            text_parts.append(p.get("text", ""))
        else:
            text_parts.append(getattr(p, "text", ""))
    text = " ".join(text_parts)
    return text[:MAX_TEXT_CHARS]


class SummarizeYouTubeInput(BaseModel):
    video: str = Field(..., description="YouTube video URL or ID")
    sentences: int = Field(default=3, description="Number of sentences")


@tool("SummarizeYouTube", args_schema=SummarizeYouTubeInput)
@track_tool
def summarize_youtube_tool(video: str, sentences: int = 3) -> str:
    """Provide a short summary of a YouTube video's auto-generated captions."""
    video_id = extract_video_id(video)
    if not video_id:
        return "Invalid YouTube URL or ID"
    with status_manager.status("Изучаю видео"):
        text = fetch_captions(video_id)
    if text.startswith("Failed to fetch"):
        return text
    return summarize_text_tool.func(text=text, sentences=sentences)

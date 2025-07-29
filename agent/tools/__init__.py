from __future__ import annotations

from pydantic import BaseModel, Field
from langchain_core.tools import tool

from .bash_tool import run_bash_command
from .telegram_tool import send_telegram_message
from .file_tools import transcribe_audio, find_file
from .obsidian_tools import create_note, summarize_note
from .pdf_tools import extract_text_from_pdf, summarize_pdf, count_words_in_file
from .github_tool import get_repo_info
from .network_tools import check_website, get_domain_info


class BashCommandInput(BaseModel):
    command: str = Field(..., description="Bash command to execute")


@tool("RunBashCommand", args_schema=BashCommandInput)
def run_bash_command_tool(command: str) -> str:
    """Execute a system bash command and returns the result."""
    return run_bash_command(command)


class PDFPathInput(BaseModel):
    path: str = Field(..., description="Path to the PDF file")
    max_pages: int = Field(default=30, description="Maximum pages to read")


@tool("ExtractTextFromPDF", args_schema=PDFPathInput)
def extract_text_from_pdf_tool(path: str, max_pages: int = 30) -> str:
    """Extract the textual contents from a PDF file."""
    return extract_text_from_pdf(path, max_pages=max_pages)


class SummarizePDFInput(BaseModel):
    path: str = Field(..., description="Path to the PDF file")
    sentences: int = Field(default=3, description="Number of sentences")


@tool("SummarizePDF", args_schema=SummarizePDFInput)
def summarize_pdf_tool(path: str, sentences: int = 3) -> str:
    """Provide a short summary of a PDF document."""
    return summarize_pdf(path, sentences=sentences)


class CountWordsInput(BaseModel):
    path: str = Field(..., description="Path to the text file")


@tool("CountWordsInFile", args_schema=CountWordsInput)
def count_words_in_file_tool(path: str) -> str:
    """Return the number of words in a text file."""
    return count_words_in_file(path)


class TranscribeAudioInput(BaseModel):
    path: str = Field(..., description="Path to the audio file")
    model_name: str = Field(default="base", description="Whisper model name")


@tool("TranscribeAudio", args_schema=TranscribeAudioInput)
def transcribe_audio_tool(path: str, model_name: str = "base") -> str:
    """Transcribe speech from an audio file using Whisper if available."""
    return transcribe_audio(path, model_name=model_name)


class CreateNoteInput(BaseModel):
    title: str = Field(..., description="Note title")
    content: str = Field(default="", description="Note content")


@tool("CreateNote", args_schema=CreateNoteInput)
def create_note_tool(title: str, content: str = "") -> str:
    """Create a new markdown note in the configured Obsidian vault."""
    return create_note(title, content)


class SummarizeNoteInput(BaseModel):
    title: str = Field(..., description="Note title")
    sentences: int = Field(default=3, description="Number of sentences")


@tool("SummarizeNote", args_schema=SummarizeNoteInput)
def summarize_note_tool(title: str, sentences: int = 3) -> str:
    """Summarize a markdown note from the Obsidian vault."""
    return summarize_note(title, sentences=sentences)


class FindFileInput(BaseModel):
    pattern: str = Field(..., description="Filename or glob pattern")
    root: str = Field(default=".", description="Root search directory")


@tool("FindFile", args_schema=FindFileInput)
def find_file_tool(pattern: str, root: str = ".") -> list[str]:
    """Recursively search for files by name or glob pattern and return absolute paths."""
    return find_file(pattern, root)


class RepoInfoInput(BaseModel):
    repo: str = Field(..., description="Repository in owner/name format")


@tool("GetGitHubRepoInfo", args_schema=RepoInfoInput)
def get_repo_info_tool(repo: str) -> str:
    """Retrieve basic information about a GitHub repository."""
    return get_repo_info(repo)


class TelegramInput(BaseModel):
    text: str = Field(..., description="Message text")


@tool("SendTelegramMessage", args_schema=TelegramInput)
def send_telegram_message_tool(text: str) -> str:
    """Send a text message via the configured Telegram bot."""
    return send_telegram_message(text)


class CheckWebsiteInput(BaseModel):
    url: str = Field(..., description="Website URL")


@tool("CheckWebsite", args_schema=CheckWebsiteInput)
def check_website_tool(url: str) -> str:
    """Check if a website is reachable and return HTTP status code."""
    return check_website(url)


class DomainInfoInput(BaseModel):
    domain: str = Field(..., description="Domain name")


@tool("GetDomainInfo", args_schema=DomainInfoInput)
def get_domain_info_tool(domain: str) -> str:
    """Get basic DNS information (A and MX records) for a domain."""
    return get_domain_info(domain)


tools = [
    run_bash_command_tool,
    extract_text_from_pdf_tool,
    summarize_pdf_tool,
    count_words_in_file_tool,
    transcribe_audio_tool,
    create_note_tool,
    summarize_note_tool,
    find_file_tool,
    get_repo_info_tool,
    send_telegram_message_tool,
    check_website_tool,
    get_domain_info_tool,
]

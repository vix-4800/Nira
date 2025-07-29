from __future__ import annotations

from .check_website_tool import check_website_tool
from .file_manager_tool import file_manager
from .get_domain_info_tool import get_domain_info_tool
from .github_manager_tool import github_manager
from .obsidian_manager_tool import obsidian_manager
from .pdf_manager_tool import pdf_manager
from .run_bash_command_tool import run_bash_command_tool
from .summarize_website_tool import summarize_website_tool
from .summarize_youtube_tool import summarize_youtube_tool
from .telegram_manager_tool import telegram_manager
from .transcribe_audio_tool import transcribe_audio_tool

# Export a list of tools for use by LangChain agents

tools = [
    run_bash_command_tool,
    pdf_manager,
    file_manager,
    transcribe_audio_tool,
    obsidian_manager,
    github_manager,
    telegram_manager,
    check_website_tool,
    get_domain_info_tool,
    summarize_website_tool,
    summarize_youtube_tool,
]

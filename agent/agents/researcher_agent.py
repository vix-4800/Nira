from ..core.nira_memory import NiraMemory
from ..core.prompt import load_prompt
from ..tools.file_manager_tool import file_manager
from ..tools.get_domain_info_tool import get_domain_info_tool
from ..tools.homeassistant_manager_tool import homeassistant_manager
from ..tools.memory_manager_tool import memory_manager
from ..tools.obsidian_manager_tool import obsidian_manager
from ..tools.pdf_manager_tool import pdf_manager
from ..tools.proxmox_manager_tool import proxmox_manager
from ..tools.researcher.summarize_text_tool import summarize_text_tool
from ..tools.researcher.summarize_youtube_tool import summarize_youtube_tool
from ..tools.researcher.web_search_tool import web_search_tool
from ..tools.scrape_url_tool import scrape_url_tool
from ..tools.telegram_manager_tool import telegram_manager
from ..tools.todoist_manager_tool import todoist_manager
from ..tools.transcribe_audio_tool import transcribe_audio_tool
from .base_agent import BaseAgent

RESEARCHER_TOOLS = [
    web_search_tool,
    summarize_text_tool,
    summarize_youtube_tool,
    obsidian_manager,
    todoist_manager,
    pdf_manager,
    file_manager,
    transcribe_audio_tool,
    homeassistant_manager,
    get_domain_info_tool,
    proxmox_manager,
    scrape_url_tool,
    telegram_manager,
    memory_manager,
]


class ResearcherAgent(BaseAgent):
    tool_list = RESEARCHER_TOOLS

    def __init__(self, memory: NiraMemory | None = None, **kwargs):
        config = load_prompt()
        super().__init__(
            system_prompt=config.get("researcher_system"),
            tool_list=self.tool_list,
            memory=memory,
            **kwargs,
        )

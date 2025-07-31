from .base_agent import BaseAgent
from .tools.summarise_text_tool import summarise_text_tool
from .tools.summarize_youtube_tool import summarize_youtube_tool
from .tools.web_search_tool import web_search_tool

RESEARCHER_SYSTEM = "You research information and summarise findings."
RESEARCHER_TOOLS = [web_search_tool, summarise_text_tool, summarize_youtube_tool]


class ResearcherAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            system_prompt=RESEARCHER_SYSTEM, tool_list=RESEARCHER_TOOLS, **kwargs
        )

from ..tools.researcher.summarise_text_tool import summarise_text_tool
from ..tools.researcher.summarize_youtube_tool import summarize_youtube_tool
from ..tools.researcher.web_search_tool import web_search_tool
from .base_agent import BaseAgent

RESEARCHER_SYSTEM = "You research information and summarise findings."
RESEARCHER_TOOLS = [web_search_tool, summarise_text_tool, summarize_youtube_tool]


class ResearcherAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            system_prompt=RESEARCHER_SYSTEM, tool_list=RESEARCHER_TOOLS, **kwargs
        )

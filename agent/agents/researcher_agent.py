from ..core.prompt import load_prompt
from ..core.nira_memory import NiraMemory
from ..tools.researcher.summarize_text_tool import summarize_text_tool
from ..tools.researcher.summarize_youtube_tool import summarize_youtube_tool
from ..tools.researcher.web_search_tool import web_search_tool
from .base_agent import BaseAgent

RESEARCHER_TOOLS = [web_search_tool, summarize_text_tool, summarize_youtube_tool]


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

from ..core.nira_memory import NiraMemory
from ..core.prompt import load_prompt
from ..tools.coder.github_manager_tool import github_manager
from ..tools.sysops.run_bash_command_tool import run_bash_command_tool
from .base_agent import BaseAgent

CODER_TOOLS = [run_bash_command_tool, github_manager]


class CoderAgent(BaseAgent):
    tool_list = CODER_TOOLS

    def __init__(self, memory: NiraMemory | None = None, **kwargs):
        config = load_prompt()
        super().__init__(
            system_prompt=config.get("coder_system"),
            tool_list=self.tool_list,
            memory=memory,
            **kwargs,
        )

from ..tools.coder.github_manager_tool import github_manager
from ..tools.sysops.run_bash_command_tool import run_bash_command_tool
from .base_agent import BaseAgent

CODER_SYSTEM = "You are a coding assistant helping with programming tasks."
CODER_TOOLS = [run_bash_command_tool, github_manager]


class CoderAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(system_prompt=CODER_SYSTEM, tool_list=CODER_TOOLS, **kwargs)

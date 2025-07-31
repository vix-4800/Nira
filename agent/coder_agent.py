from .base_agent import BaseAgent
from .tools.run_bash_command_tool import run_bash_command_tool
from .tools.github_manager_tool import github_manager


CODER_SYSTEM = "You are a coding assistant helping with programming tasks."
CODER_TOOLS = [run_bash_command_tool, github_manager]


class CoderAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(system_prompt=CODER_SYSTEM, tool_list=CODER_TOOLS, **kwargs)

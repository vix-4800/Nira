from ..tools.sysops.check_website_tool import check_website_tool
from ..tools.sysops.run_bash_command_tool import run_bash_command_tool
from .base_agent import BaseAgent

SYSOPS_SYSTEM = "You perform system administration and operational tasks."
SYSOPS_TOOLS = [run_bash_command_tool, check_website_tool]


class SysOpsAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(system_prompt=SYSOPS_SYSTEM, tool_list=SYSOPS_TOOLS, **kwargs)

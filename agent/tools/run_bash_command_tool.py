from pydantic import BaseModel, Field
from langchain_core.tools import tool

from .bash_tool import run_bash_command

class BashCommandInput(BaseModel):
    command: str = Field(..., description="Bash command to execute")

@tool("RunBashCommand", args_schema=BashCommandInput)
def run_bash_command_tool(command: str) -> str:
    """Execute a system bash command and returns the result."""
    return run_bash_command(command)

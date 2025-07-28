from langchain.agents import Tool
from .bash_tool import run_bash_command

tools = [
    Tool(
        name="RunBashCommand",
        func=run_bash_command,
        description="Executes a system bash command and returns the result. Use it for file searching, system management, and other terminal tasks."
    ),
    # ...
]

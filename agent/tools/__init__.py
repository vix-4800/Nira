from langchain.agents import Tool
from .bash_tool import run_bash_command
from .telegram_tool import send_telegram_message

tools = [
    Tool(
        name="RunBashCommand",
        func=run_bash_command,
        description="Executes a system bash command and returns the result. Use it for file searching, system management, and other terminal tasks."
    ),
    Tool(
        name="SendTelegramMessage",
        func=send_telegram_message,
        description="Sends a text message via the configured Telegram bot.",
    ),
    # ...
]

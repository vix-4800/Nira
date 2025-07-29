from pydantic import BaseModel, Field
from langchain_core.tools import tool

from .telegram_tool import send_telegram_message

class TelegramInput(BaseModel):
    text: str = Field(..., description="Message text")

@tool("SendTelegramMessage", args_schema=TelegramInput)
def send_telegram_message_tool(text: str) -> str:
    """Send a text message via the configured Telegram bot."""
    return send_telegram_message(text)

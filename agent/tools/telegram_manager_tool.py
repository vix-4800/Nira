import requests
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from ..metrics import track_tool

from ..env import get_telegram_bot_token, get_telegram_chat_id
from ..status import status_manager


class TelegramManagerInput(BaseModel):
    action: str = Field(..., description="send_message")
    text: str | None = Field(None, description="Message text for 'send_message'")


@tool("TelegramManager", args_schema=TelegramManagerInput)
@track_tool
def telegram_manager(action: str, text: str | None = None) -> str:
    """Unified tool for Telegram operations."""
    match action:
        case "send_message":
            token = get_telegram_bot_token()
            chat_id = get_telegram_chat_id()
            if not token or not chat_id:
                return "TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not configured."
            if not text:
                return "Error: 'text' is required for send_message"
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            try:
                with status_manager.status("отправляю сообщение"):
                    resp = requests.post(url, json={"chat_id": chat_id, "text": text})
                resp.raise_for_status()
                return "Message sent."
            except Exception as e:
                return f"Failed to send message: {e}"
        case _:
            return f"Error: unknown action '{action}'"

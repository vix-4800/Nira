from langchain_core.tools import tool
from pydantic import BaseModel, Field

from ..config import load_config
from ..metrics import track_tool
from .http_utils import request_json


class TelegramManagerInput(BaseModel):
    action: str = Field(..., description="send_message")
    text: str | None = Field(None, description="Message text for 'send_message'")


@tool("TelegramManager", args_schema=TelegramManagerInput)
@track_tool
def telegram_manager(action: str, text: str | None = None) -> str:
    """Unified tool for Telegram operations."""
    match action:
        case "send_message":
            cfg = load_config()
            token = cfg.telegram_bot_token
            chat_id = cfg.telegram_chat_id
            if not token or not chat_id:
                return "TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not configured."
            if not text:
                return "Error: 'text' is required for send_message"
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            result = request_json(
                "post",
                url,
                json={"chat_id": chat_id, "text": text},
                status_msg="отправляю сообщение",
                error_msg="Failed to send message",
            )
            if isinstance(result, str):
                return result
            return "Message sent."
        case _:
            return f"Error: unknown action '{action}'"

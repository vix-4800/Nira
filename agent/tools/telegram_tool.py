import requests
from ..env import get_telegram_bot_token, get_telegram_chat_id


def send_telegram_message(text: str) -> str:
    """Send a Telegram message using the configured bot."""
    token = get_telegram_bot_token()
    chat_id = get_telegram_chat_id()
    if not token or not chat_id:
        return "TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not configured."

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        resp = requests.post(url, json={"chat_id": chat_id, "text": text})
        resp.raise_for_status()
        return "Message sent."
    except Exception as e:
        return f"Failed to send message: {e}"

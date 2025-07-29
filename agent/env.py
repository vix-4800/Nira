from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

_TRUE_VALUES = {"1", "true", "yes", "y"}


def get_server(default: str = "http://localhost:11434") -> str:
    """Return the server URL from the environment."""
    return os.getenv("SERVER", default)


def get_model(default: str = "qwen3:4b") -> str:
    """Return the model name from the environment."""
    return os.getenv("MODEL", default)


def get_auto_confirm() -> bool:
    """Return True if AUTO_CONFIRM is truthy in the environment."""
    return os.getenv("AUTO_CONFIRM", "").lower() in _TRUE_VALUES


def get_telegram_bot_token() -> str:
    """Return the Telegram bot token from the environment."""
    return os.getenv("TELEGRAM_BOT_TOKEN", "")


def get_telegram_chat_id() -> str:
    """Return the Telegram chat ID from the environment."""
    return os.getenv("TELEGRAM_CHAT_ID", "")


def get_github_token() -> str:
    """Return the GitHub access token from the environment."""
    return os.getenv("GITHUB_TOKEN", "")


def get_obsidian_vault() -> str:
    """Return the path to the Obsidian vault."""
    return os.getenv("OBSIDIAN_VAULT", "")


def get_dns_server() -> str:
    """Return the DNS server to use for lookups if specified."""
    return os.getenv("DNS_SERVER", "")


def parse_env() -> tuple[str, str, bool]:
    """Return server, model and auto_confirm parsed from the environment."""
    return get_server(), get_model(), get_auto_confirm()


__all__ = [
    "get_server",
    "get_model",
    "get_auto_confirm",
    "get_telegram_bot_token",
    "get_telegram_chat_id",
    "get_obsidian_vault",
    "get_github_token",
    "parse_env",
    "get_dns_server",
]

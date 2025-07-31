from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

_TRUE_VALUES = {"1", "true", "yes", "y"}


@dataclass
class NiraConfig:
    server: str = "http://localhost:11434"
    model: str = "qwen3:4b"
    auto_confirm: bool = False
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None
    github_token: str | None = None
    todoist_token: str | None = None
    obsidian_vault: str | None = None
    dns_server: str | None = None
    proxmox_host: str | None = None
    proxmox_token_id: str | None = None
    proxmox_token_secret: str | None = None
    proxmox_verify_ssl: bool = True


def load_config() -> NiraConfig:
    """Load configuration from environment variables."""
    load_dotenv()
    return NiraConfig(
        server=os.getenv("SERVER", NiraConfig.server),
        model=os.getenv("MODEL", NiraConfig.model),
        auto_confirm=os.getenv("AUTO_CONFIRM", "").lower() in _TRUE_VALUES,
        telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN"),
        telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID"),
        github_token=os.getenv("GITHUB_TOKEN"),
        todoist_token=os.getenv("TODOIST_TOKEN"),
        obsidian_vault=os.getenv("OBSIDIAN_VAULT"),
        dns_server=os.getenv("DNS_SERVER"),
        proxmox_host=os.getenv("PROXMOX_HOST"),
        proxmox_token_id=os.getenv("PROXMOX_TOKEN_ID"),
        proxmox_token_secret=os.getenv("PROXMOX_TOKEN_SECRET"),
        proxmox_verify_ssl=os.getenv("PROXMOX_VERIFY_SSL", "true").lower()
        in _TRUE_VALUES,
    )


__all__ = ["NiraConfig", "load_config"]

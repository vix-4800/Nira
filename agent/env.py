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


def parse_env() -> tuple[str, str, bool]:
    """Return server, model and auto_confirm parsed from the environment."""
    return get_server(), get_model(), get_auto_confirm()

__all__ = ["get_server", "get_model", "get_auto_confirm", "parse_env"]

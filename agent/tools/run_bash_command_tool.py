import re
import subprocess

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from ..env import get_auto_confirm
from ..metrics import track_tool
from ..status import status_manager


class BashCommandInput(BaseModel):
    command: str = Field(..., description="Bash command to execute")


_DANGEROUS_PATTERNS = [
    r"\brm\b.*-rf",
    r"\bshutdown\b",
    r"\breboot\b",
    r"\bmkfs\b",
    r"\bdd\b.*\/dev\/sd",
]


def _is_dangerous(command: str) -> bool:
    for pat in _DANGEROUS_PATTERNS:
        if re.search(pat, command):
            return True
    return False


def _confirm(prompt: str) -> bool:
    reply = input(prompt).strip().lower()
    return reply in {"y", "yes"}


@tool("RunBashCommand", args_schema=BashCommandInput)
@track_tool
def run_bash_command_tool(command: str) -> str:
    """Execute a system bash command and returns the result."""
    auto_confirm = get_auto_confirm()
    dangerous = _is_dangerous(command)

    if not auto_confirm or dangerous:
        prompt = (
            f"Команда '{command}' выглядит опасной. Выполнить? [y/N]: "
            if dangerous
            else f"Выполнить команду '{command}'? [y/N]: "
        )
        if not _confirm(prompt):
            return "Команда отменена"

    try:
        with status_manager.status("выполняю команду"):
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
        output = result.stdout.strip() or result.stderr.strip()
        return output if output else "(Пустой вывод)"
    except Exception as e:
        return f"Ошибка запуска команды: {e}"

import re
import shlex
import subprocess

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from ...core.config import load_config
from ...core.metrics import track_tool
from ...core.status import status_manager


class BashCommandInput(BaseModel):
    command: str = Field(..., description="Bash command to execute")


_DANGEROUS_PATTERNS = [
    r"\brm\b.*-rf",
    r"\bshutdown\b",
    r"\breboot\b",
    r"\bmkfs\b",
    r"\bdd\b.*\/dev\/sd",
    r"\bpoweroff\b",
    r"\bhalt\b",
    r"^init\s+0$",
    r"\brm\b.*--no-preserve-root",
]

# Compile regexes once at module import for efficiency
_DANGEROUS_REGEXES = [re.compile(pat) for pat in _DANGEROUS_PATTERNS]


def _is_dangerous(command: str) -> bool:
    """Return True if command matches any dangerous pattern."""
    for regex in _DANGEROUS_REGEXES:
        if regex.search(command):
            return True
    return False


def _confirm(prompt: str) -> bool:
    reply = input(prompt).strip().lower()
    return reply in {"y", "yes"}


@tool("RunBashCommand", args_schema=BashCommandInput)
@track_tool
def run_bash_command_tool(command: str) -> str:
    """Execute a system bash command and returns the result."""
    auto_confirm = load_config().auto_confirm
    dangerous = _is_dangerous(command)

    if not auto_confirm or dangerous:
        prompt = (
            f"Команда '{command}' выглядит опасной. Выполнить? [y/N]: "
            if dangerous
            else f"Выполнить команду '{command}'? [y/N]: "
        )
        with status_manager.status("ожидаю подтверждения"):
            if not _confirm(prompt):
                return "Команда отменена"

    try:
        with status_manager.status("выполняю команду `" + command + "`"):
            result = subprocess.run(
                shlex.split(command),
                capture_output=True,
                text=True,
                timeout=30,
            )
        output = result.stdout.strip() or result.stderr.strip()
        return output if output else "(Пустой вывод)"
    except Exception as e:
        return f"Ошибка запуска команды: {e}"

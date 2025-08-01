"""Entrypoint to launch Nira in console or web mode."""

from __future__ import annotations

import importlib
from typing import Callable

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

console = Console()


LOGO = Text(
    r"""
 _    _    _____    ______
| \\ | || |_   _|| |   __ \\      /\\
|  \\| ||   | ||   | ||__) ||    /  \\
| ..`` ||   | ||   |  _   //    / /\ \\
| ||\  ||  _| ||_  | || \ \\   / ____ \\
|_|| \_|| |_____|| |_||  \_\\ /_/    \_\\
""",
    style="bold magenta",
)


def display_logo() -> None:
    """Print the NIRA ASCII art logo."""
    console.print(LOGO)


OPTIONS: dict[str, tuple[str, Callable[[], None]]] = {
    "1": ("Console", lambda: importlib.import_module("console").main()),
    "2": ("Web", lambda: importlib.import_module("web").main()),
}


def select_mode() -> Callable[[], None]:
    table = Table(title="Select Nira mode")
    table.add_column("Option")
    table.add_column("Mode")
    for key, (name, _) in OPTIONS.items():
        table.add_row(key, name)
    console.print(table)

    while True:
        choice = Prompt.ask(
            "Choose an option", choices=list(OPTIONS.keys()), default="1"
        )
        return OPTIONS[choice][1]


def main() -> None:
    try:
        display_logo()
        launcher = select_mode()
        launcher()
    except EOFError:
        console.print("")
    except KeyboardInterrupt:
        console.print("")


if __name__ == "__main__":
    main()

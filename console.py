import sys
from getpass import getuser
from typing import Optional

from rich.markdown import Markdown

from agent.agents.planner_executor import PlannerExecutor
from agent.core.config import load_config
from agent.core.metrics import init_metrics
from agent.core.prompt import ConfigError
from agent.core.status import console, status_manager

try:
    from agent.core.voice_recognizer import transcribe_whisper
    from agent.core.voice_synthesizer import VoiceSynthesizer
except Exception:
    transcribe_whisper = None  # type: ignore
    VoiceSynthesizer = None  # type: ignore

voice_modules_available = (
    transcribe_whisper is not None and VoiceSynthesizer is not None
)

voice_synthesizer: Optional["VoiceSynthesizer"] = None
USERNAME = getuser().capitalize()


def typewriter(text: str, delay=0.015, prefix="") -> None:
    if prefix:
        console.print(f"[bold magenta]{prefix}[/]", end="")
    console.print(Markdown(text))



def get_user_input(use_voice: bool) -> str:
    if use_voice:
        if transcribe_whisper is None:
            return ""
        user_input = transcribe_whisper()
        if not user_input:
            console.print("[yellow]Не удалось распознать речь. Попробуй ещё раз![/]")
    else:
        user_input = console.input(f"👤 [bold blue]{USERNAME}:[/] ")

    return user_input.strip()


def main() -> None:
    with status_manager.status("Загружаюсь..."):
        init_metrics()

        model = load_config().model
        try:
            planner = PlannerExecutor()
        except ConfigError as exc:
            console.print(f"[bold red]Configuration error:[/] {exc}")
            return

        use_voice = "--voice" in sys.argv
        speak = "--speak" in sys.argv

        if (use_voice or speak) and not voice_modules_available:
            console.print(
                "[yellow]Voice features requested but optional dependencies are not installed.[/]"
            )
            if use_voice:
                console.print("[yellow]Распознавание речи недоступно.[/]")
            if speak:
                console.print("[yellow]Синтез речи недоступен.[/]")
            use_voice = False
            speak = False

        if speak:
            global voice_synthesizer
            if VoiceSynthesizer is not None:
                voice_synthesizer = VoiceSynthesizer()

    console.print(
        "[bold magenta]👾 Nira:[/] Привет! Я готова отвечать на вопросы. Для выхода напиши /exit"
    )
    console.print(f"[dim]Я буду использовать модель: {model}[/]")
    console.rule("[bold blue]Nira Chat[/]")

    try:
        while True:
            user_input = get_user_input(use_voice)

            if user_input in ["/exit", "выход", "exit"]:
                console.print("[bold magenta]👾 Nira:[/] До встречи!")
                break

            with status_manager.status("Думаю..."):
                response = planner.run(user_input)

            typewriter(response, prefix="👾 Nira: ")

            if speak and voice_synthesizer is not None:
                voice_synthesizer.speak(response)
    except EOFError:
        console.print("\n[bold magenta]👾 Nira:[/] До встречи!")
    except KeyboardInterrupt:
        console.print("\n[bold magenta]👾 Nira:[/] До встречи!")
    except Exception as e:
        console.print(f"\n[bold red]👾 Nira:[/] Произошла ошибка: {e}")


if __name__ == "__main__":
    main()

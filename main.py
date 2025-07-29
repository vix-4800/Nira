import re
import sys
import time

from agent.status import console, status_manager

from agent.env import get_model, get_server
from agent.nira_agent import NiraAgent

try:
    from agent.voice_recognizer import transcribe_whisper
    from agent.voice_synthesizer import VoiceSynthesizer

    voice_modules_available = True
except Exception:
    transcribe_whisper = None
    VoiceSynthesizer = None
    voice_modules_available = False

voice_synthesizer = None


def prepare_response(text: str) -> str:
    response = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return response.strip()


def typewriter(text: str, delay=0.015, prefix="") -> None:
    if prefix:
        console.print(f"[bold magenta]{prefix}[/]", end="")
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print("\n")


def main() -> None:
    model = get_model()
    server = get_server()

    nira = NiraAgent(model_name=model, base_url=server)

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
        voice_synthesizer = VoiceSynthesizer()

    console.print(
        "[bold magenta]👾 Nira:[/] Привет! Я готова отвечать на вопросы. Для выхода напиши /exit"
    )
    console.print(f"[dim]Я буду использовать модель: {model}[/]")
    console.rule("[bold blue]Nira Chat[/]")

    try:
        while True:
            if use_voice:
                user_input = transcribe_whisper()
                if not user_input:
                    console.print(
                        "[yellow]Не удалось распознать речь. Попробуй ещё раз![/]"
                    )
                    continue
                console.print(f"[green]Ты (голос):[/] {user_input}")
            else:
                user_input = console.input("[green]Ты:[/] ")

            if user_input.strip() in ["/exit", "выход", "exit"]:
                console.print("[bold magenta]👾 Nira:[/] До встречи!")
                break

            with status_manager.status("Думаю..."):
                response = nira.ask(user_input)
                response = prepare_response(response)

            typewriter(response, prefix="👾 Nira: ")
            if speak:
                voice_synthesizer.speak(response)
    except EOFError:
        console.print("\n[bold magenta]👾 Nira:[/] До встречи!")
    except KeyboardInterrupt:
        console.print("\n[bold magenta]👾 Nira:[/] До встречи!")
    except Exception as e:
        console.print(f"\n[bold red]👾 Nira:[/] Произошла ошибка: {e}")


if __name__ == "__main__":
    main()

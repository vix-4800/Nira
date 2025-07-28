from rich.console import Console
from agent.nira_agent import NiraAgent
from dotenv import load_dotenv
from agent.tools.voice_tool import transcribe_whisper
from agent.voice_synthesizer import VoiceSynthesizer
import os
import re
import time
import sys

load_dotenv()
console = Console()
voice_synthesizer = VoiceSynthesizer()

def parse_env() -> tuple[str, str, bool]:
    server = os.getenv("SERVER", "http://localhost:11434")
    model = os.getenv("MODEL", "qwen3:4b")
    auto = os.getenv("AUTO_CONFIRM", "").lower() in {"1", "true", "yes", "y"}
    return server, model, auto

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
    server, model, auto = parse_env()

    nira = NiraAgent(model_name=model, base_url=server)

    use_voice = "--voice" in sys.argv
    speak = "--speak" in sys.argv

    console.print("[bold magenta]👾 Nira:[/] Привет! Я готова отвечать на вопросы. Для выхода напиши /exit")
    console.print(f"[dim]Я буду использовать модель: {model}[/]")
    console.rule("[bold blue]Nira Chat[/]")

    try:
        while True:
            if use_voice:
                user_input = transcribe_whisper()
                if not user_input:
                    console.print("[yellow]Не удалось распознать речь. Попробуй ещё раз![/]")
                    continue
                console.print(f"[green]Ты (голос):[/] {user_input}")
            else:
                user_input = console.input("[green]Ты:[/] ")

            if user_input.strip() in ["/exit", "выход", "exit"]:
                console.print("[bold magenta]👾 Nira:[/] До встречи!")
                break

            with console.status("[cyan]Думаю...[/]", spinner="dots"):
                response = nira.ask(user_input)
                response = prepare_response(response)

            typewriter(response, prefix="👾 Nira: ")
            if speak:
                voice_synthesizer.speak(response)
    except KeyboardInterrupt:
        console.print("\n[bold magenta]👾 Nira:[/] До встречи!")
    except Exception as e:
        console.print(f"\n[bold red]👾 Nira:[/] Произошла ошибка: {e}")

if __name__ == "__main__":
    main()

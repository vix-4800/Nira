from agent.nira_agent import NiraAgent
from dotenv import load_dotenv
import os
import re

load_dotenv()

def parse_env() -> tuple[str, str, bool]:
    server = os.getenv("SERVER", "http://localhost:11434")
    model = os.getenv("MODEL", "qwen3:4b")
    auto = os.getenv("AUTO_CONFIRM", "").lower() in {"1", "true", "yes", "y"}
    return server, model, auto

def prepare_response(text: str) -> str:
    response = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return response.strip()

def main() -> None:
    server, model, auto = parse_env()

    nira = NiraAgent(model, server)
    print("👾 Nira: Привет! Я готова выполнять твои команды. Для выхода напиши /exit")
    print(f"Я буду использовать модель {model}.\n")

    try:
        while True:
            user_input = input("Ты: ")

            if user_input.strip() in ["/exit", "выход", "exit"]:
                print("👾 Nira: До встречи!")
                break

            response = nira.ask(user_input)
            response = prepare_response(response)

            print(f"👾 Nira: {response}\n")
    except KeyboardInterrupt:
        print("\n👾 Nira: До встречи!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()

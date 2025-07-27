import subprocess
import requests
import re
import json
import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_SERVER = "http://localhost:11434"
DEFAULT_MODEL = "qwen3:4b"


def parse_env():
    server = os.getenv("SERVER", DEFAULT_SERVER)
    model = os.getenv("MODEL", DEFAULT_MODEL)
    return server, model


GOODBYE_PHRASES = ["bye", "goodbye", "nothing", "exit", "quit"]


def ask_llm(prompt, server_url, model):
    res = requests.post(
        f"{server_url}/api/generate",
        json={
            "model": model,  # llama3.2:3b / deepseek-r1:8b-0528-qwen3-q4_K_M
            "prompt": prompt,
            "stream": False,
        },
    )
    return res.json()["response"]


def build_prompt(system_prompt, examples, task, history=None):
    lines = [system_prompt]
    for ex in examples:
        user = ex.get("user")
        assistant = ex.get("assistant")
        if user is not None and assistant is not None:
            lines.append(f"User: {user}\nAssistant: {assistant}")
        elif "role" in ex and "content" in ex:
            lines.append(f"{ex['role'].capitalize()}: {ex['content']}")

    if history:
        for step in history:
            role = step.get("role", "User")
            content = step.get("content", "")
            lines.append(f"{role.capitalize()}: {content}")
    lines.append(f"User: {task}\nAssistant:")

    return "\n".join(lines)


def run_command(cmd):
    print(f"\n>> {cmd}")

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    out = result.stdout.strip()
    err = result.stderr.strip()

    if out:
        print(out)
    if err:
        print("stderr:", err)

    return out, err


def check_command_error(err):
    error_signatures = [
        "Syntax error",
        "syntax error",
        "unexpected EOF",
        "unterminated quoted string",
        "unmatched quote",
        "command not found",
        "not found",
        "invalid option",
        "No such file or directory",
    ]
    for sign in error_signatures:
        if sign in err:
            return True

    return False


def main():
    with open("prompt.json", "r", encoding="utf-8") as f:
        prompt_data = json.load(f)
    system_prompt = prompt_data["system"]
    examples = prompt_data.get("examples", [])

    server_url, model = parse_env()

    while True:
        task = input("\nЧто нужно сделать?\n")
        if task.lower() in GOODBYE_PHRASES:
            print("Bye!")
            break

        history = []
        prev_task = task
        step_count = 0

        while True:
            prompt = build_prompt(system_prompt, examples, prev_task, history)
            response = ask_llm(prompt, server_url, model)
            commands = re.findall(r"COMMAND:\s*(.+)", response)

            if not commands:
                print("\nLLM answer:", response)
                break

            for idx, cmd in enumerate(commands, 1):
                step_count += 1
                print(f"\n[Step {step_count}]\nCommand {idx}: {cmd}")

                confirm = input("Выполнить? (y/n/q): ")
                if confirm.lower() == "q":
                    print("Остановка задачи.")
                    return
                if confirm.lower() != "y":
                    print("Пропущено.")
                    continue

                out, err = run_command(cmd)

                if err and check_command_error(err):
                    print(
                        "❗️ Внимание: в команде обнаружена синтаксическая или критическая ошибка!"
                    )
                    print(f"Ошибка: {err}")
                    prev_task = f"Предыдущая команда завершилась ошибкой:\n{err}\nПожалуйста, исправь команду и повтори попытку."

                output_text = f"stdout:\n{out}\nstderr:\n{err}"
                history.append({"role": "system", "content": output_text})


if __name__ == "__main__":
    main()

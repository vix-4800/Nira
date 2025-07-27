import subprocess
import requests
import re
import json
from requests import exceptions as req_exc
import os
from datetime import datetime
import argparse
from dotenv import load_dotenv


class LLMServerUnavailable(Exception):
    """Raised when the local LLM server cannot be reached."""
    pass

load_dotenv()

DEFAULT_SERVER = "http://localhost:11434"
DEFAULT_MODEL = "qwen3:4b"
GOODBYE_PHRASES = ["bye", "goodbye", "nothing", "exit", "quit"]

LOG_FILE = None

def parse_env():
    server = os.getenv("SERVER", DEFAULT_SERVER)
    model = os.getenv("MODEL", DEFAULT_MODEL)
    return server, model

def ask_llm(prompt, server_url, model):
    """Send prompt to the local LLM server and return its response.

    Raises
    ------
    LLMServerUnavailable
        If the server cannot be reached or returns a non-200 status.
    """

    try:
        res = requests.post(
            f"{server_url}/api/generate",
            json={
                "model": model,  # llama3.2:3b / deepseek-r1:8b-0528-qwen3-q4_K_M
                "prompt": prompt,
                "stream": False,
            },
        )
        res.raise_for_status()
    except req_exc.RequestException as exc:
        raise LLMServerUnavailable("Failed to connect to the LLM server") from exc

    try:
        return res.json().get("response")
    except ValueError as exc:
        raise LLMServerUnavailable("Invalid response from LLM server") from exc

def build_prompt(system_prompt, examples, task, history=None):
    lines = [system_prompt]
    for ex in examples:
        user = ex.get("user")
        assistant = ex.get("assistant")
        if user is not None and assistant is not None:
            lines.append(f"User: {user}\nAssistant: {assistant}")
        elif "role" in ex and "content" in ex:
            lines.append(f"{ex["role"].capitalize()}: {ex["content"]}")

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

def log_step(cmd, out, err):
    if not LOG_FILE:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {cmd}\n")
        if out:
            f.write(f"stdout:\n{out}\n")
        if err:
            f.write(f"stderr:\n{err}\n")
        f.write("\n")

def log_interaction(prompt, response):
    """Log a prompt and the LLM's response with timestamp."""
    if not LOG_FILE:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] Prompt:\n{prompt}\n")
        f.write(f"Response:\n{response}\n\n")

def check_command_error(err):
    lower_err = err.lower()
    error_signatures = [
        "syntax error",
        "unexpected eof",
        "unterminated quoted string",
        "unmatched quote",
        "command not found",
        "not found",
        "invalid option",
        "no such file or directory",
    ]
    for sign in error_signatures:
        if sign in lower_err:
            return True

    return False

def parse_args():
    parser = argparse.ArgumentParser(description="Nexora assistant")
    parser.add_argument("--log-file", "-l", help="Path to log file")
    return parser.parse_args()

def main():
    args = parse_args()

    global LOG_FILE
    if args.log_file:
        LOG_FILE = args.log_file
    else:
        os.makedirs("logs", exist_ok=True)
        LOG_FILE = os.path.join(
            "logs",
            datetime.now().strftime("%Y%m%d_%H%M%S.log"),
        )

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
            while True:
                try:
                    response = ask_llm(prompt, server_url, model)
                    break
                except LLMServerUnavailable:
                    choice = input(
                        "LLM server is unavailable. Retry? (y to retry, q to quit): "
                    )
                    if choice.lower() == "y":
                        continue
                    print("Остановка задачи.")
                    return
            log_interaction(prompt, response)

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
                log_step(cmd, out, err)

                if err and check_command_error(err):
                    print("❗️ Внимание: в команде обнаружена синтаксическая или критическая ошибка!")
                    print(f"Ошибка: {err}")
                    prev_task = f"Предыдущая команда завершилась ошибкой:\n{err}\nПожалуйста, исправь команду и повтори попытку."

                output_text = f"stdout:\n{out}\nstderr:\n{err}"
                history.append({"role": "system", "content": output_text})

if __name__ == "__main__":
    main()

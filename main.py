import subprocess
import re
import json
import os
from datetime import datetime
import argparse
from dotenv import load_dotenv
import sys
from colorama import Fore, Style, init as colorama_init
import ollama
from history_agent import AgentHistory


class LLMServerUnavailable(Exception):
    """Raised when the local LLM server cannot be reached."""
    pass

load_dotenv()
colorama_init()

# Directory where this script resides
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_SERVER = "http://localhost:11434"
DEFAULT_MODEL = "qwen3:4b"
GOODBYE_PHRASES = ["bye", "goodbye", "nothing", "exit", "quit"]
LOG_FILE = None

def parse_env():
    server = os.getenv("SERVER", DEFAULT_SERVER)
    model = os.getenv("MODEL", DEFAULT_MODEL)
    auto = os.getenv("AUTO_CONFIRM", "").lower() in {"1", "true", "yes", "y"}
    return server, model, auto

def load_prompt_data(path="prompt.json"):
    """Load prompt configuration from JSON file.

    If the file is missing or contains invalid JSON, print a user friendly
    error message and exit with a non-zero code.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: prompt file '{path}' not found.")
    except json.JSONDecodeError as exc:
        print(f"Error: could not parse '{path}': {exc}")

    sys.exit(1)

def ask_llm(prompt, model, system_prompt):
    try:
        response = ollama.generate(model, prompt, system=system_prompt, stream=False)
    except (ollama.OllamaError, OSError, ConnectionError) as exc:
        raise LLMServerUnavailable("Failed to connect to the LLM server") from exc

    try:
        return response["response"]
    except KeyError:
        raise LLMServerUnavailable("Invalid response from LLM server")

def run_command(cmd):
    print(f"\n{Fore.CYAN}>> {cmd}{Style.RESET_ALL}")

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    out = result.stdout.strip()
    err = result.stderr.strip()

    if out:
        print(out)
    if err:
        print(f"{Fore.RED}stderr:{Style.RESET_ALL} {err}")

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

def is_command_safe(cmd):
    """Return ``True`` if the command doesn't look destructive."""
    unsafe_patterns = [
        r"\brm\s+-rf\s+/\s*$",
        r"\bshutdown\s+-h\s+now\b",
    ]
    for pat in unsafe_patterns:
        if re.search(pat, cmd, re.IGNORECASE):
            return False
    return True

def parse_args():
    parser = argparse.ArgumentParser(description="Nexora assistant")
    parser.add_argument("--log-file", "-l", help="Path to log file")
    return parser.parse_args()

def extract_commands(response):
    if '</think>' in response:
        response = response.split('</think>')[-1]

    return re.findall(r'^COMMAND:\s*(.+)', response, re.MULTILINE)

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

    prompt_data = load_prompt_data(os.path.join(SCRIPT_DIR, "prompt.json"))
    system_prompt = prompt_data["system"]
    examples = prompt_data.get("examples", [])

    server_url, model, auto_confirm = parse_env()

    try:
        while True:
            task = input("\nWhat needs to be done?\n")
            if task.lower() in GOODBYE_PHRASES:
                print("Bye!")
                break

            history = AgentHistory(max_steps=12)
            history.add("user", task)

            prev_task = task
            step_count = 0

            while True:
                prompt = history.build_prompt(prev_task)

                while True:
                    try:
                        response = ask_llm(prompt, model, system_prompt)
                        break
                    except LLMServerUnavailable:
                        choice = input("LLM server is unavailable. Retry? (y to retry, q to quit): ")
                        if choice.lower() == "y":
                            continue
                        print("Task aborted.")
                        return
                log_interaction(prompt, response)

                commands = extract_commands(response)

                if not commands:
                    print("\nLLM answer:", response)
                    history.add("assistant", response)
                    break

                for idx, cmd in enumerate(commands, 1):
                    step_count += 1
                    print(f"\n[Step {step_count}]\nCommand {idx}: {cmd}")

                    is_safe = is_command_safe(cmd)
                    if is_safe and auto_confirm:
                        confirm = "y"
                    else:
                        confirm = input("Execute? (y/n/q): ")

                    if confirm.lower() == "q":
                        print("Task aborted.")
                        return
                    if confirm.lower() != "y":
                        print("Skipped.")
                        continue

                    if not is_safe:
                        print("\u26a0\ufe0f  Potentially dangerous command is being executed.")

                    out, err = run_command(cmd)
                    log_step(cmd, out, err)

                    result_text = f"stdout:\n{out}\nstderr:\n{err}"
                    status = "error" if err and check_command_error(err) else "ok"
                    history.add("assistant", f"My suggested command: {cmd}")
                    history.add("system", "", result=result_text, status=status)

                    output_text = f"stdout:\n{out}\nstderr:\n{err}"
                    history.append({"role": "assistant", "content": f"My suggested command: {cmd}"})
                    history.append({"role": "system", "content": output_text})

                    if status == "error":
                        prev_task = f"Команда '{cmd}' вернула ошибку: {err}. Что делать дальше, чтобы решить задачу?"
                    else:
                        prev_task = "Что делать дальше?"
    except KeyboardInterrupt:
        print("Interrupted")
        return

if __name__ == "__main__":
    main()

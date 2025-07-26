import subprocess
import requests
import re
import json


def ask_llm(model, prompt):
    res = requests.post('http://localhost:11434/api/generate', json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    return res.json()["response"]

def build_prompt(system_prompt, examples, task):
    lines = [system_prompt]
    for ex in examples:
        lines.append(f"User: {ex['user']}\nAssistant: {ex['assistant']}")
    lines.append(f"Task: {task}\nAssistant:")
    return "\n".join(lines)

def main():
    with open("prompt.json", "r", encoding="utf-8") as f:
        prompt_data = json.load(f)
    system_prompt = prompt_data["system"]
    model = prompt_data["model"]
    examples = prompt_data.get("examples", [])

    task = input("What should I do?\n")
    prompt = build_prompt(system_prompt, examples, task)
    response = ask_llm(model, prompt)

    commands = re.findall(r"COMMAND:\s*(.+)", response)
    if commands:
        for idx, cmd in enumerate(commands, 1):
            print(f"Command {idx}: {cmd}")

            confirm = input("Execute? (y/n): ")
            if confirm.lower() == 'y':
                subprocess.run(cmd, shell=True)
            else:
                print("Cancelled")
    else:
        print("LLM answer:", response)

if __name__ == "__main__":
    while(True):
        main()

import subprocess

def run_bash_command(command: str) -> str:
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout.strip() or result.stderr.strip()
        return output if output else "(Пустой вывод)"
    except Exception as e:
        return f"Ошибка запуска команды: {e}"

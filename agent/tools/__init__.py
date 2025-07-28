from langchain.agents import Tool
from .bash_tool import run_bash_command

tools = [
    Tool(
        name="RunBashCommand",
        func=run_bash_command,
        description="Выполняет системную bash-команду и возвращает результат. Используй для поиска файлов, управления системой и других задач по терминалу."
    ),
    # ...
]

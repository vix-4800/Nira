import json
import os
from datetime import datetime

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_ollama import ChatOllama

from ..core.nira_memory import NiraMemory
from ..core.prompt import ConfigError, load_prompt
from ..tools import tools as default_tools

# fmt: off
# isort: off
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
# isort: on
# fmt: on


class BaseAgent:
    def __init__(
        self,
        model_name=None,
        base_url=None,
        llm=None,
        log_file="chat.json",
        memory: NiraMemory | None = None,
        *,
        system_prompt: str | None = None,
        tool_list: list | None = None,
        max_iterations=15,
        max_bytes=1 * 1024 * 1024,
        backup_count=5,
    ) -> None:
        self.llm = llm or ChatOllama(
            model=model_name,
            base_url=base_url,
            reasoning=False,
            # temperature=0.3,
        )

        self.max_iterations = max_iterations
        self.agent_executor: AgentExecutor | None

        self.log_file = log_file
        self.max_bytes = max_bytes
        self.backup_count = backup_count

        self.memory = memory or NiraMemory(
            memory_key="chat_history", return_messages=True
        )

        try:
            config = load_prompt()
        except ConfigError:
            raise
        system_prompt = system_prompt or config.get(
            "system", "You are Nira - an AI assistant."
        )

        tools = tool_list or default_tools
        self.tool_list = tools

        if hasattr(self.llm, "bind_tools"):
            self.prompt = ChatPromptTemplate.from_messages(
                [
                    SystemMessagePromptTemplate.from_template(system_prompt),
                    MessagesPlaceholder("chat_history"),
                    HumanMessagePromptTemplate.from_template("{input}"),
                    MessagesPlaceholder("agent_scratchpad"),
                ]
            )

            agent = create_tool_calling_agent(self.llm, tools, self.prompt)
            self.agent_executor = AgentExecutor(
                agent=agent,
                tools=tools,
                memory=self.memory,
                verbose=False,
                handle_parsing_errors=True,
                max_iterations=max_iterations,
            )
        else:
            self.agent_executor = None

    def _rotate_logs(self) -> None:
        """Rotate chat logs according to backup_count."""
        try:
            if self.backup_count > 0:
                for i in range(self.backup_count - 1, 0, -1):
                    src = f"{self.log_file}.{i}"
                    dst = f"{self.log_file}.{i + 1}"
                    if os.path.exists(src):
                        os.replace(src, dst)
                if os.path.exists(self.log_file):
                    os.replace(self.log_file, f"{self.log_file}.1")
            else:
                if os.path.exists(self.log_file):
                    os.remove(self.log_file)
        except Exception:
            pass

    def log_chat(self, question: str, response: str) -> None:
        """Log a chat interaction to the log file."""
        timestamp = datetime.now().isoformat()
        log_entry = {"t": timestamp, "q": question, "a": response}
        try:
            data: list = []
            if os.path.exists(self.log_file):
                try:
                    with open(self.log_file, "r", encoding="utf-8") as fh:
                        data = json.load(fh)
                        if not isinstance(data, list):
                            data = []
                except json.JSONDecodeError:
                    data = []
            data.append(log_entry)
            encoded = json.dumps(data, ensure_ascii=False)
            size = len(encoded.encode("utf-8"))
            if self.max_bytes > 0 and size > self.max_bytes:
                self._rotate_logs()
                with open(self.log_file, "w", encoding="utf-8") as fh:
                    json.dump([log_entry], fh, ensure_ascii=False)
            else:
                with open(self.log_file, "w", encoding="utf-8") as fh:
                    fh.write(encoded)
        except Exception:
            pass

    def ask(self, question: str) -> str:
        if self.agent_executor is not None:
            result = self.agent_executor.invoke({"input": question})
            response = result["output"] if isinstance(result, dict) else str(result)
        else:
            try:
                raw = self.llm.invoke(question)
                response = raw.content if hasattr(raw, "content") else str(raw)
            except AttributeError:
                response = self.llm.predict(question)
            self.memory.save_context(
                {self.memory.input_key: question},
                {self.memory.output_key: response},
            )

        self.log_chat(question, response)
        return response

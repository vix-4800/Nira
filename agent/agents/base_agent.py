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

    def log_chat(self, question: str, response: str) -> None:
        """Log a chat interaction to the log file."""
        timestamp = datetime.now().isoformat()
        log_entry = {"t": timestamp, "q": question, "a": response}
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, "r+", encoding="utf-8") as fh:
                    try:
                        data = json.load(fh)
                        if not isinstance(data, list):
                            data = []
                    except json.JSONDecodeError:
                        data = []
                    data.append(log_entry)
                    fh.seek(0)
                    json.dump(data, fh, ensure_ascii=False)
                    fh.truncate()
            else:
                with open(self.log_file, "w", encoding="utf-8") as fh:
                    json.dump([log_entry], fh, ensure_ascii=False)
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

    def ask_stream(self, question: str):
        """Yield the response token by token."""
        response = ""
        if self.agent_executor is not None:
            for chunk in self.agent_executor.stream({"input": question}):
                messages = chunk.get("messages", []) if isinstance(chunk, dict) else []
                for msg in messages:
                    content = getattr(msg, "content", "")
                    if content:
                        response += content
                        yield content
        else:
            try:
                for chunk in self.llm.stream(question):
                    content = chunk.content if hasattr(chunk, "content") else str(chunk)
                    response += content
                    yield content
            except AttributeError:
                resp = self.llm.predict(question)
                response += resp
                yield resp

        self.memory.save_context(
            {self.memory.input_key: question},
            {self.memory.output_key: response},
        )
        self.log_chat(question, response)

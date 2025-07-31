import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_ollama import ChatOllama

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

from .nira_memory import NiraMemory
from .prompt import ConfigError, load_prompt
from .tools import tools


class NiraAgent:
    def __init__(
        self,
        model_name=None,
        base_url=None,
        llm=None,
        log_file="chat.log",
        *,
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

        self.logger = logging.getLogger(self.__class__.__name__)
        for h in list(self.logger.handlers):
            self.logger.removeHandler(h)
        handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count
        )
        handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        self.memory = NiraMemory(memory_key="chat_history", return_messages=True)

        try:
            config = load_prompt()
        except ConfigError as exc:
            print(exc)
            exit(1)
        system_prompt = config.get("system", "You are Nira - an AI assistant.")

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
        self.logger.info(f"{timestamp}\tQ: {question}\tA: {response}")

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

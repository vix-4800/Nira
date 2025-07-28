import json
import logging
from datetime import datetime
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain.agents import create_tool_calling_agent, AgentExecutor
from agent.tools import tools
from langchain_ollama import ChatOllama
from langchain.chains import LLMChain

class NiraAgent:
    def __init__(self, model_name=None, base_url=None, llm=None, log_file="chat.log") -> None:
        self.llm = llm or ChatOllama(
            model=model_name,
            base_url=base_url,
            reasoning=False,
            temperature=0.3,
        )

        self.logger = logging.getLogger(self.__class__.__name__)
        for h in list(self.logger.handlers):
            self.logger.removeHandler(h)
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        config = self.load_config()
        system_prompt = config.get("system", "You are Nira - an AI assistant.")

        if hasattr(self.llm, "bind_tools"):
            self.prompt = ChatPromptTemplate.from_messages([
                SystemMessagePromptTemplate.from_template(system_prompt),
                MessagesPlaceholder("chat_history"),
                HumanMessagePromptTemplate.from_template("{input}"),
                MessagesPlaceholder("agent_scratchpad"),
            ])

            agent = create_tool_calling_agent(self.llm, tools, self.prompt)
            self.agent_executor = AgentExecutor(
                agent=agent,
                tools=tools,
                memory=self.memory,
                verbose=False,
                handle_parsing_errors=True,
                max_iterations=3,
            )
        else:
            self.agent_executor = None

    def log_chat(self, question: str, response: str) -> None:
        """Log a chat interaction to the log file."""
        timestamp = datetime.now().isoformat()
        self.logger.info(f"{timestamp}\tQ: {question}\tA: {response}")

    def load_config(self):
        try:
            with open("prompt.json", "r") as f:
                config = json.load(f)
            return config
        except FileNotFoundError:
            print("prompt.json not found. Exiting.")
            exit(1)
        except json.JSONDecodeError:
            print("prompt.json is not valid JSON. Exiting.")
            exit(1)

    def ask(self, question: str) -> str:
        if self.agent_executor is not None:
            result = self.agent_executor.invoke({"input": question})
            response = result.get("output", "") if isinstance(result, dict) else str(result)
        else:
            self.memory.chat_memory.add_user_message(question)
            response = self.llm.invoke(question)
            self.memory.chat_memory.add_ai_message(response)

        self.log_chat(question, response)
        return response

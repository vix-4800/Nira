import json
import logging
from datetime import datetime
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain_ollama.llms import OllamaLLM

class NiraAgent:
    """Simple conversational agent backed by LangChain."""

    def __init__(self, model_name=None, base_url=None, llm=None, log_file="chat.log") -> None:
        """Create a new agent.

        Parameters
        ----------
        model_name : str, optional
            Name of the Ollama model.
        base_url : str, optional
            Ollama server URL.
        llm : BaseLLM, optional
            Custom LLM instance (used mainly for testing).
        """

        self.llm = llm or OllamaLLM(model=model_name, base_url=base_url)
        self.log_file = log_file

        self.logger = logging.getLogger(self.__class__.__name__)
        for h in list(self.logger.handlers):
            self.logger.removeHandler(h)
        handler = logging.FileHandler(self.log_file)
        handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        config = self.load_config()
        system_prompt = config.get("system", "")

        self.prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(system_prompt),
                MessagesPlaceholder(variable_name="history"),
                HumanMessagePromptTemplate.from_template("{user_input}"),
            ]
        )

        self.memory = ConversationBufferMemory(
            memory_key="history", input_key="user_input", return_messages=True
        )
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory,
        )

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
        """Ask the agent a question and return the response."""
        response = self.chain.predict(user_input=question)
        self.log_chat(question, response)
        return response

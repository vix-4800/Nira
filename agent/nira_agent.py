from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import json

class NiraAgent:
    def __init__(self, model_name, base_url) -> None:
        self.llm = OllamaLLM(
            model=model_name,
            base_url=base_url,
        )

        config = self.load_config()
        system_prompt = config.get("system", "")
        self.template = system_prompt + "\nQuestion: {question}\nAnswer:"

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
        prompt = ChatPromptTemplate.from_template(self.template)
        msg = prompt.format_messages(question=question)

        return self.llm.invoke(msg)

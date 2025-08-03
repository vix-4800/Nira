from pathlib import Path

from langchain_ollama import ChatOllama

from ..core.config import NiraConfig, load_config
from ..core.nira_memory import NiraMemory
from ..core.persistent_memory import PersistentMemory
from ..core.prompt import load_prompt
from .base_agent import BaseAgent
from .coder_agent import CoderAgent
from .researcher_agent import ResearcherAgent
from .sysops_agent import SysOpsAgent


class RouterAgent:
    """Route tasks to specialized agents using an LLM classifier."""

    def __init__(
        self,
        classifier_llm: ChatOllama | None = None,
        coder: CoderAgent | None = None,
        researcher: ResearcherAgent | None = None,
        sysops: SysOpsAgent | None = None,
        memory: NiraMemory | None = None,
        model_name: str | None = None,
        base_url: str | None = None,
        config: NiraConfig | None = None,
        memory_db_path: str | Path = "memory.db",
    ) -> None:
        cfg = config or load_config()
        model = model_name or cfg.model
        server = base_url or cfg.server
        self.classifier_llm = classifier_llm or ChatOllama(
            model=model,
            base_url=server,
            reasoning=False,
        )
        self.memory = memory or NiraMemory(
            memory_key="chat_history", return_messages=True
        )
        self.coder = coder or CoderAgent(
            model_name=model, base_url=server, memory=self.memory
        )
        self.researcher = researcher or ResearcherAgent(
            model_name=model, base_url=server, memory=self.memory
        )
        self.sysops = sysops or SysOpsAgent(
            model_name=model, base_url=server, memory=self.memory
        )

        self.memory_db_path = Path(memory_db_path)

        prompt_config = load_prompt()
        self.classify_template = prompt_config.get(
            "classify",
            "Classify the user request into one of: coder, researcher, sysops. Respond with only the label.\nRequest: {task}",
        )

    def _classify(self, task: str) -> str:
        prompt = self.classify_template.replace("{task}", task)
        try:
            raw = self.classifier_llm.invoke(prompt)
            label = raw.content if hasattr(raw, "content") else str(raw)
        except AttributeError:
            label = self.classifier_llm.predict(prompt)
        label_str = str(label)
        return label_str.strip().lower()

    def ask(self, question: str) -> str:
        lower = question.lower().strip()

        if lower.startswith("remember "):
            statement = question[len("remember "):].strip()
            key: str | None = None
            value: str | None = None
            if " is " in statement:
                key, value = statement.split(" is ", 1)
            elif "=" in statement:
                key, value = statement.split("=", 1)
            if key and value is not None:
                with PersistentMemory(self.memory_db_path) as mem:
                    mem.set(key.strip(), value.strip())
                return f"Remembered {key.strip()}"
            return "Please specify what to remember in the form 'remember X is Y'"

        with PersistentMemory(self.memory_db_path) as mem:
            data = mem.all()
        for k, v in data.items():
            if k.lower() in lower or lower in k.lower():
                return v

        label = self._classify(question)
        if label.startswith("coder"):
            agent: BaseAgent = self.coder
        elif label.startswith("sysops"):
            agent = self.sysops
        else:
            agent = self.researcher
        response = agent.ask(question)
        return response

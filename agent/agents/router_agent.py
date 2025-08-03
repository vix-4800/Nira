from pathlib import Path
import warnings

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
        memory_llm: ChatOllama | None = None,
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
        self.memory_llm = memory_llm or self.classifier_llm
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
        self.memory_template = prompt_config.get(
            "memory",
            (
                "If the user asks the assistant to remember information, respond with "
                "'remember|<key>|<value>'. Otherwise respond with 'none'. Request: {task}"
            ),
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

        memory = self._parse_memory_request(question)
        if memory:
            key, value = memory
            with PersistentMemory(self.memory_db_path) as mem:
                mem.set(key, value)
            return f"Remembered {key}"

        with PersistentMemory(self.memory_db_path) as mem:
            data = mem.all()
        for k, v in data.items():
            if k.lower() in lower or lower in k.lower():
                return v

        label = self._classify(question)
        if label.startswith("coder"):
            agent: BaseAgent = self.coder
        elif label.startswith("researcher"):
            agent = self.researcher
        elif label.startswith("sysops"):
            agent = self.sysops
        else:
            warnings.warn(
                f"Unknown agent label '{label}', defaulting to ResearcherAgent",
                stacklevel=1,
            )
            agent = self.researcher
        response = agent.ask(question)
        return response

    def _parse_memory_request(self, task: str) -> tuple[str, str] | None:
        prompt = self.memory_template.replace("{task}", task)
        try:
            raw = self.memory_llm.invoke(prompt)
            result = raw.content if hasattr(raw, "content") else str(raw)
        except AttributeError:
            result = self.memory_llm.predict(prompt)
        text = str(result).strip()
        if text.lower() == "none":
            return None
        if text.startswith("remember|"):
            parts = text.split("|", 2)
            if len(parts) == 3:
                return parts[1].strip(), parts[2].strip()
        return None

from langchain_ollama import ChatOllama

from ..core.config import NiraConfig, load_config
from ..core.logger_utils import setup_logger
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
        model_name: str | None = None,
        base_url: str | None = None,
        config: NiraConfig | None = None,
        *,
        log_file: str = "chat.json",
        max_bytes: int = 1 * 1024 * 1024,
        backup_count: int = 5,
    ) -> None:
        cfg = config or load_config()
        model = model_name or cfg.model
        server = base_url or cfg.server
        self.classifier_llm = classifier_llm or ChatOllama(
            model=model,
            base_url=server,
            reasoning=False,
        )
        self.coder = coder or CoderAgent(model_name=model, base_url=server)
        self.researcher = researcher or ResearcherAgent(
            model_name=model, base_url=server
        )
        self.sysops = sysops or SysOpsAgent(model_name=model, base_url=server)

        self.logger = setup_logger(
            self.__class__.__name__, log_file, max_bytes, backup_count
        )

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
        label = self._classify(question)
        if label.startswith("coder"):
            agent: BaseAgent = self.coder
        elif label.startswith("sysops"):
            agent = self.sysops
        else:
            agent = self.researcher
        response = agent.ask(question)
        self.logger.info(response)
        return response
